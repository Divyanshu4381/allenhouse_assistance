import requests
from app.config import API_KEY, API_URL, MODEL_NAME
from app.services.token_manager import get_max_tokens


def ask_llm(context: str, question: str) -> str:
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    messages = [
        {
            "role": "system",
            "content": (
                "You are an official college information assistant.\n\n"
                "STRICT RULES:\n"
                "1. Be BRIEF, CONCISE, and DIRECT. Answer only what is asked.\n"
                "2. Use ONLY the information provided in the Context.\n"
                "3. Do NOT add assumptions or introductions (ex: 'Based on the context...', 'I hope this helps').\n"
                "4. If the Context does not contain the answer, say exactly:\n"
                "   'Please contact the college office for this information.'\n\n"
                "FORMATTING RULES:\n"
                "- **Clickable Links**: You MUST include any official URLs found in the Context as clickable Markdown links (e.g., [Click Here](URL)).\n"
                "- **Bold Important Terms**: Use **Bold** for major headings, key amounts (Rs.), and titles.\n"
                "- **Markdown Tables**: ALWAYS use Markdown Tables for any comparative data. You MUST use the exact Year labels found in the Context (e.g., 'First Year', 'II, III & IV Year', 'II Year').\n"
                "- **Bullet Points**: Use simple, indented bullet points for short lists.\n"
                "- **Paragraphs**: Keep plain text to 1-2 short, readable paragraphs.\n"
                "- **Spacing**: Add a double newline between distinct sections.\n"
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "max_tokens": get_max_tokens(question),
        "temperature": 0.2,  # Low temp for factual/direct answers
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    answer = response.json()["choices"][0]["message"]["content"]
    return answer.strip()
