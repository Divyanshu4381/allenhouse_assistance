from app.data.college_data import COLLEGE_DATA
from app.services.normalizer import normalize


def _name_hit(q_words: set, tags: list) -> int:
    """
    Boost score heavily if query contains a person's name or specific tag.
    Multi-word tags (e.g. 'bharat tripathi') get extra weight.
    """
    boost = 0
    q_text = " ".join(q_words)
    for tag in tags:
        tag_clean = tag.strip().lower()
        if " " in tag_clean:
            # Multi-word tag (name or phrase) — huge boost
            if tag_clean in q_text:
                boost += 6
        else:
            # Single-word tag
            if tag_clean in q_words:
                boost += 3
    return boost


def retrieve_context(question: str) -> str:
    normalized_question = normalize(question)
    q_words = set(normalized_question.split())
    q_text = " ".join(q_words)

    matches = []

    for item in COLLEGE_DATA:
        content = item.get("content", "")
        tags = item.get("tags", [])

        # Convert dict content to text (legacy safety)
        if isinstance(content, dict):
            content_text = " ".join(
                f"{k}: {v}" for k, v in content.items() if isinstance(v, (str, int))
            )
        else:
            content_text = content

        normalized_content = normalize(content_text)
        content_words = set(normalized_content.split())

        # Base score: word intersection between question and content
        base_score = len(q_words & content_words)

        # Tag boost: question words / phrases matching entry tags
        tag_boost = _name_hit(q_words, tags)

        # Source label bonus: if question mentions the source category
        source = item.get("source", "")
        source_bonus = 2 if source.replace("_", " ") in q_text else 0

        total_score = base_score + tag_boost + source_bonus

        if total_score > 0:
            matches.append((total_score, content_text))

    # Sort by score descending, return top 2 most relevant chunks
    matches.sort(key=lambda x: x[0], reverse=True)

    return "\n\n".join([m[1] for m in matches[:2]])
