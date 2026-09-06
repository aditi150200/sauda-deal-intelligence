from app.engine import assess_deal
from app.models import Deal, RiskLevel


def make_deal(**overrides):
    values = dict(id="D-1", account="Test Co", owner="Owner", amount=100000,
                  discount_pct=5, gross_margin_pct=40, days_in_stage=10,
                  payment_terms_days=30, account_health=90, open_support_cases=0,
                  product_fit_score=90, close_probability=80)
    values.update(overrides)
    return Deal(**values)


def test_low_risk_deal_has_standard_path():
    result = assess_deal(make_deal())
    assert result.risk_level == RiskLevel.low
    assert result.risk_score == 0
    assert result.approval_required is False


def test_risky_deal_is_explainable_and_capped():
    result = assess_deal(make_deal(discount_pct=35, gross_margin_pct=10,
        days_in_stage=60, payment_terms_days=90, account_health=30,
        open_support_cases=8, product_fit_score=30, close_probability=20))
    assert result.risk_level == RiskLevel.high
    assert result.risk_score == 100
    assert result.approval_required is True
    assert result.factors[0].impact >= result.factors[-1].impact


def test_large_deal_routes_to_approval_without_inflating_risk():
    result = assess_deal(make_deal(amount=600000))
    assert result.risk_score == 0
    assert result.approval_required is True
    assert "deal-value" in result.approval_reason

