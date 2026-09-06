from app.models import Assessment, Deal, RiskFactor, RiskLevel


def assess_deal(deal: Deal) -> Assessment:
    """Return a deterministic, explainable risk assessment for a deal."""
    factors: list[RiskFactor] = []

    def add(code: str, label: str, impact: int, evidence: str) -> None:
        factors.append(RiskFactor(code=code, label=label, impact=impact, evidence=evidence))

    if deal.discount_pct >= 30:
        add("deep_discount", "Deep discount", 24, f"{deal.discount_pct:.0f}% discount exceeds 30%")
    elif deal.discount_pct >= 20:
        add("discount", "Elevated discount", 12, f"{deal.discount_pct:.0f}% discount exceeds 20%")

    if deal.gross_margin_pct < 15:
        add("margin", "Low gross margin", 22, f"{deal.gross_margin_pct:.0f}% margin is below 15%")
    elif deal.gross_margin_pct < 25:
        add("margin", "Margin pressure", 10, f"{deal.gross_margin_pct:.0f}% margin is below 25%")

    if deal.days_in_stage > 45:
        add("stalled", "Stalled opportunity", 18, f"{deal.days_in_stage} days in the current stage")
    elif deal.days_in_stage > 25:
        add("aging", "Aging opportunity", 8, f"{deal.days_in_stage} days in the current stage")

    if deal.account_health < 40:
        add("account_health", "Weak account health", 18, f"Health score is {deal.account_health}/100")
    elif deal.account_health < 65:
        add("account_health", "Moderate account health", 8, f"Health score is {deal.account_health}/100")

    if deal.open_support_cases >= 5:
        add("support", "High support burden", 12, f"{deal.open_support_cases} unresolved cases")
    elif deal.open_support_cases >= 2:
        add("support", "Open support issues", 5, f"{deal.open_support_cases} unresolved cases")

    if deal.payment_terms_days > 60:
        add("terms", "Extended payment terms", 10, f"Requested terms are {deal.payment_terms_days} days")

    if deal.product_fit_score < 50:
        add("fit", "Low product fit", 16, f"Fit score is {deal.product_fit_score}/100")

    if deal.close_probability < 40:
        add("probability", "Low close confidence", 10, f"Close probability is {deal.close_probability}%")

    score = min(100, sum(f.impact for f in factors))
    level = RiskLevel.high if score >= 55 else RiskLevel.medium if score >= 25 else RiskLevel.low
    approval_required = deal.discount_pct >= 25 or deal.gross_margin_pct < 20 or deal.amount >= 500_000

    reasons = []
    if deal.discount_pct >= 25:
        reasons.append("discount threshold")
    if deal.gross_margin_pct < 20:
        reasons.append("margin threshold")
    if deal.amount >= 500_000:
        reasons.append("deal-value threshold")

    recommendation = {
        RiskLevel.high: "Pause and resolve the top risk factors before approval.",
        RiskLevel.medium: "Proceed with mitigation steps and manager review.",
        RiskLevel.low: "Proceed through the standard approval path.",
    }[level]

    return Assessment(
        deal_id=deal.id,
        risk_score=score,
        risk_level=level,
        recommendation=recommendation,
        approval_required=approval_required,
        approval_reason=", ".join(reasons) if reasons else None,
        factors=sorted(factors, key=lambda factor: factor.impact, reverse=True),
    )

