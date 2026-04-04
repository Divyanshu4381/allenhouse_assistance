from app.data.college_data import COLLEGE_DATA
from app.services.normalizer import normalize
from app.services.textifier import dict_to_text


def retrieve_context(question: str) -> str:
    normalized_question = normalize(question)
    q_words = set(normalized_question.split())

    matches = []

    for item in COLLEGE_DATA:
        content = item["content"]

        # 🔥 FIX: dict → text
        if isinstance(content, dict):
            content_text = dict_to_text(content)
        else:
            content_text = content

        normalized_content = normalize(content_text)
        content_words = set(normalized_content.split())

        score = len(q_words & content_words)

        if score > 0:
            matches.append((score, content_text))

    matches.sort(key=lambda x: x[0], reverse=True)

    return "\n".join([m[1] for m in matches[:3]])
