from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT / "src", ROOT / "tests"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from fake_llm import FakeLLM  # noqa: E402
from sbce.kb import KnowledgeBase, load_chunks  # noqa: E402


@pytest.fixture(scope="session")
def cfg() -> dict:
    return yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf8"))


@pytest.fixture(scope="session")
def brief(cfg) -> str:
    return (ROOT / cfg["brief"]).read_text(encoding="utf8")


@pytest.fixture(scope="session")
def lessons() -> list[dict]:
    return yaml.safe_load((ROOT / "eval" / "known_lessons.yaml").read_text(encoding="utf8"))


@pytest.fixture
def llm() -> FakeLLM:
    return FakeLLM()


@pytest.fixture
def kb(cfg, llm) -> KnowledgeBase:
    return KnowledgeBase(load_chunks(ROOT / cfg["knowledge_dir"]), llm)
