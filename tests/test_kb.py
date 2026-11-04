"""Knowledge base loading and hybrid retrieval."""
from __future__ import annotations

import numpy as np

from sbce.kb import BM25, load_chunks, rrf, tokenize


def test_every_section_becomes_a_chunk_and_readme_is_skipped(kb):
    ids = {c.id for c in kb.chunks}
    assert "steel_spring_isolators#0" in ids and "steel_spring_isolators#1" in ids
    assert not any(c.source.lower() == "readme" for c in kb.chunks)
    assert len(ids) == len(kb.chunks)                       # ids are unique


def test_chunk_titles_combine_document_and_section(kb):
    c = kb.by_id["cold_weather_field_report#1"]
    assert c.title == "Field report: handle isolators in Nordic winter - Fix"
    assert "silicone" in c.text.lower()


def test_load_chunks_reads_any_folder(tmp_path):
    (tmp_path / "note.md").write_text("# Doc\n\n## A\ntext a\n\n## B\ntext b\n", encoding="utf8")
    assert [c.id for c in load_chunks(tmp_path)] == ["note#0", "note#1"]


def test_tokenizer_keeps_numbers():
    assert tokenize("IP54 at -15 °C, 0.6 kg") == ["ip54", "at", "15", "c", "0.6", "kg"]


def test_bm25_prefers_documents_with_rare_query_terms():
    docs = [tokenize("rubber mount handle"), tokenize("steel spring handle"), tokenize("handle grip handle")]
    s = BM25(docs).scores(tokenize("spring"))
    assert s.argmax() == 1 and s[0] == 0


def test_rrf_rewards_agreement_between_rankings():
    a = np.array([3.0, 2.0, 1.0])
    b = np.array([1.0, 3.0, 2.0])
    assert rrf([a, b]).argmax() == 1                         # 2nd and 1st beats 1st and 3rd


def test_search_finds_the_relevant_note(kb):
    hits = kb.search("rubber stiffens in cold weather and cracks", k=3)
    assert any(h.source in ("cold_weather_field_report", "elastomer_isolators") for h in hits)


def test_search_can_exclude_seen_chunks(kb):
    first = kb.search("dust", k=2)
    again = kb.search("dust", k=2, exclude={c.id for c in first})
    assert not {c.id for c in first} & {c.id for c in again}


def test_format_lists_ids_in_brackets(kb):
    text = kb.format(["cost_data#0", "missing#0"])
    assert text.startswith("[cost_data#0] ") and "missing" not in text
