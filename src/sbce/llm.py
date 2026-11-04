"""LLM access. `Ollama` talks to a local Ollama server; tests use a fake with the same interface."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Protocol, TypeVar

import numpy as np
import requests
from pydantic import BaseModel, ValidationError

M = TypeVar("M", bound=BaseModel)


class LLM(Protocol):
    stats: "CallStats"

    def chat_json(self, system: str, user: str, model: type[M]) -> M: ...

    def embed(self, texts: list[str]) -> np.ndarray: ...


@dataclass
class CallStats:
    calls: int = 0
    retries: int = 0
    prompt_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    by_task: dict[str, int] = field(default_factory=dict)

    def count(self, task: str) -> None:
        self.calls += 1
        self.by_task[task] = self.by_task.get(task, 0) + 1


def task_of(user: str) -> str:
    """Prompts start with 'TASK: <name>' so calls can be counted per step."""
    first = user.strip().splitlines()[0] if user.strip() else ""
    return first.removeprefix("TASK:").strip() or "unknown"


class Ollama:
    """Minimal client for the Ollama REST API with JSON-schema structured output and retries."""

    def __init__(self, host: str, model: str, embed_model: str, temperature: float = 0.7,
                 timeout_s: float = 300, max_retries: int = 3, seed: int | None = None, num_ctx: int = 8192,
                 progress: bool = False):
        self.host = host.rstrip("/")
        self.num_ctx = num_ctx
        self.progress = progress
        self.model = model
        self.embed_model = embed_model
        self.temperature = temperature
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.seed = seed
        self.stats = CallStats()

    def _post(self, path: str, payload: dict) -> dict:
        r = requests.post(f"{self.host}{path}", json=payload, timeout=self.timeout_s)
        r.raise_for_status()
        return r.json()

    def _chat_stream(self, payload: dict) -> dict:
        """Stream the reply token by token. The timeout then only applies to silence between tokens,
        so a slow CPU-only machine does not time out on long answers."""
        content, last = [], {}
        with requests.post(f"{self.host}/api/chat", json={**payload, "stream": True}, stream=True,
                           timeout=(10, self.timeout_s)) as r:
            r.raise_for_status()
            for n, line in enumerate(r.iter_lines()):
                if not line:
                    continue
                part = json.loads(line)
                content.append(part.get("message", {}).get("content", ""))
                if self.progress and n % 50 == 0:
                    print(".", end="", flush=True)
                if part.get("done"):
                    last = part
        if self.progress:
            print("", flush=True)
        return {**last, "message": {"content": "".join(content)}}

    def chat_json(self, system: str, user: str, model: type[M]) -> M:
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        options: dict = {"temperature": self.temperature, "num_ctx": self.num_ctx}
        if self.seed is not None:
            options["seed"] = self.seed
        last_error = ""
        for attempt in range(self.max_retries):
            t0 = time.perf_counter()
            out = self._chat_stream({"model": self.model, "messages": messages,
                                     "format": model.model_json_schema(), "options": options})
            self.stats.seconds += time.perf_counter() - t0
            self.stats.prompt_tokens += out.get("prompt_eval_count", 0)
            self.stats.output_tokens += out.get("eval_count", 0)
            if attempt == 0:
                self.stats.count(task_of(user))
            else:
                self.stats.retries += 1
            content = out["message"]["content"]
            try:
                return model.model_validate(json.loads(content))
            except (json.JSONDecodeError, ValidationError) as e:
                last_error = str(e)[:500]
                messages += [{"role": "assistant", "content": content},
                             {"role": "user", "content": f"That JSON was invalid: {last_error}\nReturn corrected JSON only."}]
        raise RuntimeError(f"LLM did not return valid {model.__name__} after {self.max_retries} tries: {last_error}")

    def embed(self, texts: list[str]) -> np.ndarray:
        t0 = time.perf_counter()
        out = self._post("/api/embed", {"model": self.embed_model, "input": texts})
        self.stats.seconds += time.perf_counter() - t0
        return np.asarray(out["embeddings"], dtype=float)
