from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Deal(BaseModel):
    id: str = Field(min_length=1)
    account: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    amount: float = Field(gt=0)
    discount_pct: float = Field(ge=0, le=100)
    gross_margin_pct: float = Field(ge=-100, le=100)
    days_in_stage: int = Field(ge=0)
    payment_terms_days: int = Field(ge=0)
    account_health: int = Field(ge=0, le=100)
    open_support_cases: int = Field(ge=0)
    product_fit_score: int = Field(ge=0, le=100)
    close_probability: int = Field(ge=0, le=100)


class RiskFactor(BaseModel):
    code: str
    label: str
    impact: int
    evidence: str


class Assessment(BaseModel):
    deal_id: str
    risk_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    recommendation: str
    approval_required: bool
    approval_reason: str | None = None
    factors: list[RiskFactor]


class DealView(BaseModel):
    deal: Deal
    assessment: Assessment

