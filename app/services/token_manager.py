def get_max_tokens(question: str) -> int:
    q = question.lower()
    q_len = len(question)

    # Long descriptive or data-heavy intents
    if any(
        word in q for word in ["about", "overview", "describe", "institute", "college", "fee", "fees", "structure"]
    ):
        return 450

    if q_len <= 40:
        return 200
    elif q_len <= 100:
        return 300
    else:
        return 450
