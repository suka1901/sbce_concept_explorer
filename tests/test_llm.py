"""The Ollama client, with the HTTP layer replaced: structured output, retries on bad JSON, statistics."""
from __future__ import annotations

import json

import numpy as np
import pytest

from sbce import llm as llm_mod
from sbce.llm import Ollama, task_of
from sbce.schemas import Queries


class FakeResponse:
    def __init__(self, payload: dict | None = None, lines: list[bytes] | None = None):
        self.payload = payload or {}
        self.lines = lines or []

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return self.payload

    def iter_lines(self):
        yield from self.lines

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def chat_reply(content: str) -> FakeResponse:
    """A streamed reply: the content arrives in two pieces, then a final 'done' message with token counts."""
    half = len(content) // 2
    parts = [{"message": {"content": content[:half]}}, {"message": {"content": content[half:]}},
             {"message": {"content": ""}, "done": True, "prompt_eval_count": 10, "eval_count": 5}]
    return FakeResponse(lines=[json.dumps(p).encode() for p in parts] + [b""])


def test_task_name_is_read_from_the_prompt():
    assert task_of("TASK: evaluate\nRound: 1") == "evaluate"
    assert task_of("no task line") == "no task line" and task_of("") == "unknown"


def test_chat_json_sends_schema_and_parses(monkeypatch):
    sent = []

    def post(url, json=None, timeout=None, stream=False):
        sent.append((url, json, stream))
        return chat_reply('{"queries": ["a", "b"]}')

    monkeypatch.setattr(llm_mod.requests, "post", post)
    client = Ollama("http://h:1/", "m", "e", seed=3)
    out = client.chat_json("sys", "TASK: scout\n...", Queries)
    assert out.queries == ["a", "b"]
    url, body, stream = sent[0]
    assert url == "http://h:1/api/chat" and stream and body["stream"] is True
    assert body["format"]["title"] == "Queries" and body["options"]["seed"] == 3 and body["options"]["num_ctx"] == 8192
    assert client.stats.calls == 1 and client.stats.by_task == {"scout": 1} and client.stats.output_tokens == 5


def test_invalid_json_is_retried_with_the_error_message(monkeypatch):
    replies = iter([chat_reply("not json"), chat_reply('{"wrong": 1}'), chat_reply('{"queries": []}')])
    bodies = []
    monkeypatch.setattr(llm_mod.requests, "post", lambda url, json=None, timeout=None, stream=False: (bodies.append(json), next(replies))[1])
    client = Ollama("http://h", "m", "e")
    assert client.chat_json("s", "TASK: scout", Queries).queries == []
    assert client.stats.calls == 1 and client.stats.retries == 2
    assert "invalid" in bodies[-1]["messages"][-1]["content"]


def test_gives_up_after_max_retries(monkeypatch):
    monkeypatch.setattr(llm_mod.requests, "post", lambda *a, **k: chat_reply("{}"))
    with pytest.raises(RuntimeError, match="Queries"):
        Ollama("http://h", "m", "e", max_retries=2).chat_json("s", "TASK: x", Queries)


def test_embed(monkeypatch):
    monkeypatch.setattr(llm_mod.requests, "post",
                        lambda url, json=None, timeout=None: FakeResponse({"embeddings": [[1, 0], [0, 1]]}))
    v = Ollama("http://h", "m", "e").embed(["a", "b"])
    assert isinstance(v, np.ndarray) and v.shape == (2, 2)
    assert json.dumps(v.tolist()) == "[[1.0, 0.0], [0.0, 1.0]]"
