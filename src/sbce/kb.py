"""Knowledge base: Markdown notes split into sections, searched with hybrid retrieval.

Hybrid = BM25 keyword ranking + embedding cosine ranking, merged with reciprocal rank fusion (RRF).
Keyword search finds exact terms ("IP54", "-15 °C"); embeddings find paraphrases.
"""
from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

from .llm import LLM
from .schemas import Chunk

TOKEN = re.compile(r"[a-z0-9]+(?:[.,][0-9]+)?")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def load_chunks(folder: Path | str) -> list[Chunk]:
    """Every `## ` section of every Markdown file (except README.md) becomes one chunk."""
    chunks: list[Chunk] = []
    for path in sorted(Path(folder).glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text(encoding="utf8")
        doc_title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), path.stem)
        sections = re.split(r"^## +", text, flags=re.M)[1:]
        for i, sec in enumerate(sections):
            head, _, body = sec.partition("\n")
            body = " ".join(body.split())
            if body:
                chunks.append(Chunk(id=f"{path.stem}#{i}", source=path.stem,
                                    title=f"{doc_title} - {head.strip()}", text=body))
    return chunks


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.docs, self.k1, self.b = docs, k1, b
        self.avgdl = sum(map(len, docs)) / max(len(docs), 1)
        df = Counter(t for d in docs for t in set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in docs]

    def scores(self, query: list[str]) -> np.ndarray:
        out = np.zeros(len(self.docs))
        for i, (tf, d) in enumerate(zip(self.tf, self.docs)):
            norm = self.k1 * (1 - self.b + self.b * len(d) / self.avgdl)
            out[i] = sum(self.idf.get(t, 0) * tf[t] * (self.k1 + 1) / (tf[t] + norm) for t in query if t in tf)
        return out


def rrf(rankings: list[np.ndarray], k: int = 60) -> np.ndarray:
    """Reciprocal rank fusion of several score arrays (higher score = better)."""
    fused = np.zeros(len(rankings[0]))
    for s in rankings:
        order = np.argsort(-s, kind="stable")
        ranks = np.empty(len(s), dtype=int)
        ranks[order] = np.arange(len(s))
        fused += 1.0 / (k + ranks + 1)
    return fused


def normalize(m: np.ndarray) -> np.ndarray:
    return m / np.maximum(np.linalg.norm(m, axis=-1, keepdims=True), 1e-12)


class KnowledgeBase:
    def __init__(self, chunks: list[Chunk], llm: LLM, cache_dir: Path | None = None):
        if not chunks:
            raise ValueError("knowledge base is empty")
        self.chunks = chunks
        self.by_id = {c.id: c for c in chunks}
        self.llm = llm
        self.bm25 = BM25([tokenize(f"{c.title} {c.text}") for c in chunks])
        self.vectors = normalize(self._embed_cached([f"{c.title}. {c.text}" for c in chunks], cache_dir))

    def _embed_cached(self, texts: list[str], cache_dir: Path | None) -> np.ndarray:
        if cache_dir is None:
            return self.llm.embed(texts)
        key = hashlib.sha256(("\n".join(texts) + getattr(self.llm, "embed_model", "")).encode()).hexdigest()[:16]
        path = Path(cache_dir) / f"kb_{key}.npy"
        if path.exists():
            return np.load(path)
        vec = self.llm.embed(texts)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.save(path, vec)
        return vec

    def search(self, query: str, k: int = 5, exclude: set[str] | frozenset[str] = frozenset()) -> list[Chunk]:
        q = normalize(self.llm.embed([query]))[0]
        fused = rrf([self.bm25.scores(tokenize(query)), self.vectors @ q])
        order = [i for i in np.argsort(-fused, kind="stable") if self.chunks[i].id not in exclude]
        return [self.chunks[i] for i in order[:k]]

    def format(self, ids: list[str]) -> str:
        return "\n".join(f"[{i}] {self.by_id[i].title}: {self.by_id[i].text}" for i in ids if i in self.by_id)
