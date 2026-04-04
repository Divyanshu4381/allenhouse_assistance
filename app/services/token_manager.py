def get_max_tokens(question: str) -> int:
    q = question.lower()
    q_len = len(question)

    # Long descriptive intents
    if any(
        word in q for word in ["about", "overview", "describe", "institute", "college"]
    ):
        return 350

    if q_len <= 40:
        return 150
    elif q_len <= 100:
        return 220
    else:
        return 300
