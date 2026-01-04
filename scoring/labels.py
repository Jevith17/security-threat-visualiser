def risk_label(score: float) -> str:
    if score >= 0.75:
        return "HIGH"
    elif score >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"
