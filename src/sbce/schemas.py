"""Data models shared by the pipeline. The LLM must return JSON that validates against these."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Chunk(BaseModel):
    id: str                      # e.g. "steel_spring_isolators#1"
    source: str                  # file stem
    title: str
    text: str


class Concept(BaseModel):
    id: str = ""
    name: str
    principle: str = Field(description="the physical working principle in a few words")
    description: str
    evidence_ids: list[str] = Field(default_factory=list)


class ConceptList(BaseModel):
    concepts: list[Concept]


class CriterionScore(BaseModel):
    criterion: str
    low: float = Field(ge=1, le=5, description="pessimistic score")
    high: float = Field(ge=1, le=5, description="optimistic score")
    evidence_ids: list[str] = Field(default_factory=list)
    rationale: str

    @field_validator("high")
    @classmethod
    def high_not_below_low(cls, v: float, info) -> float:
        low = info.data.get("low")
        return max(v, low) if low is not None else v


class MustCheck(BaseModel):
    requirement: str
    status: str = Field(description="'met', 'violated' or 'unclear'")
    evidence_ids: list[str] = Field(default_factory=list)
    reason: str = ""


class Evaluation(BaseModel):
    concept_id: str = ""
    scores: list[CriterionScore]
    must: list[MustCheck] = Field(default_factory=list)


class StrictCriterionScore(CriterionScore):
    """Variant used when `sbce.require_citations` is on: every score must cite at least one chunk."""
    evidence_ids: list[str] = Field(min_length=1, description="at least one chunk id from the evidence")


class StrictEvaluation(Evaluation):
    scores: list[StrictCriterionScore]  # pyright: ignore[reportIncompatibleVariableOverride]


class MustAssessment(BaseModel):
    """One must requirement checked as a worked comparison, so number mistakes become visible."""
    requirement: str
    evidence_value: str = Field(description="what the evidence says for this concept, with numbers and units, "
                                            "or 'not covered'")
    limit: str = Field(description="the limit in the requirement, with number and unit")
    comparison: str = Field(description="explicit comparison, e.g. '0.25 kg is below the 0.6 kg limit'")
    status: Literal["met", "violated", "unclear"]
    evidence_ids: list[str] = Field(default_factory=list)


class MustReview(BaseModel):
    checks: list[MustAssessment]


class Elimination(BaseModel):
    concept_id: str
    round: int
    rule: str                    # "must_violation" or "dominated"
    reason: str
    dominated_by: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)


class Judgement(BaseModel):
    verdict: str = Field(description="'supported', 'partly' or 'unsupported'")
    reason: str = ""


class Queries(BaseModel):
    queries: list[str]


class BaselineAnswer(BaseModel):
    concepts: list[Concept]
    evaluations: list[Evaluation]
    recommended: list[str] = Field(description="ids of the recommended concepts, best first")
