
def rule_based_ddos_score(event) -> float:
   

    score = 0.0

    # Rule 1: High confidence abuse
    if event.max_confidence >= 90:
        score += 0.4
    elif event.max_confidence >= 70:
        score += 0.25

    # Rule 2: High report volume
    if event.total_reports >= 500:
        score += 0.4
    elif event.total_reports >= 200:
        score += 0.25

    # Rule 3: Repeated activity in window
    if event.signal_count >= 3:
        score += 0.2

    # Cap score at 1.0
    return min(score, 1.0)
