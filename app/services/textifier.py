def dict_to_text(data: dict) -> str:
    parts = []

    for key, value in data.items():
        if isinstance(value, (str, int)):
            parts.append(f"{key}: {value}")

    return ". ".join(parts)
