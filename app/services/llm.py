import requests
from app.config import API_KEY, API_URL, MODEL_NAME
from app.services.token_manager import get_max_tokens


def ask_llm(context: str, question: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
    {
        "role": "system",
        "content": (
            "You are an official college information assistant.\n\n"

            "STRICT RULES:\n"
            "1. Use ONLY the information provided in the Context.\n"
            "2. Do NOT add assumptions, opinions, or external facts.\n"
            "3. If the Context does not contain the answer, say exactly:\n"
            "   'Please contact the college office for this information.'\n"
            "4. Never leave a sentence incomplete.\n"
            "5. Do not cut off answers mid-paragraph.\n"
            "6. Ensure the answer is complete and readable for students and parents.\n\n"

            "ANSWER FORMAT RULES:\n"
            "- If the question is about the institute, programs, or overview:\n"
            "  Respond in clearly separated paragraphs.\n"
            "- If the query involves multiple data points (like Fees, Course Lists, or Placement packages):\n"
            "  ALWAYS use Markdown Tables to organize the data for readability.\n"
            "- If the question is about students, training, or placements:\n"
            "  Explain in full sentences with clarity.\n"
            "- Do not write unnecessary introductions or conclusions.\n\n"

            "LANGUAGE RULES:\n"
            "- Use simple, clear English.\n"
            "- Avoid marketing language and exaggeration.\n"
            "- Maintain a neutral, factual, and professional tone.\n"
        )
    },
        {
        "role": "user",
        "content": (
            f"Context:\n{context}\n\n"
            f"Question:\n{question}"
        )
    }
    ]

    full_answer = ""

    for _ in range(3):  # max 3 continuations (safety)
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "max_tokens": get_max_tokens(question)
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        answer_part = response.json()["choices"][0]["message"]["content"]
        full_answer += " " + answer_part.strip()

        # If answer looks complete, stop
        if full_answer.strip().endswith((".", "!", "?")):
            break

        # Ask model to continue
        messages.append({
            "role": "assistant",
            "content": answer_part
        })
        messages.append({
            "role": "user",
            "content": "Please continue."
        })

    return full_answer.strip()