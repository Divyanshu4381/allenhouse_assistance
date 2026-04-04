from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.retriever import retrieve_context
from app.services.llm import ask_llm

router = APIRouter(prefix="/api", tags=["Chat"])

import re


@router.post("/ask", response_model=ChatResponse)
def ask_college_ai(request: ChatRequest):
    q = re.sub(r"[^\w\s]", "", request.question.strip().lower())

    # Handle basic greetings
    greetings = [
        "hi",
        "hello",
        "hey",
        "hi there",
        "hello there",
        "namaste",
        "namaskar",
        "pranam",
        "good morning",
        "good evening",
        "good afternoon",
        "hola",
        "heya",
        "yo",
        "sup",
        "whats up",
        "how are you",
        "kaise ho",
        "hallo",
        "hii",
        "hiii",
        "helloo",
    ]
    if q in greetings:
        return {
            "answer": "Hello! I am the Allenhouse AI Assistant. I can help you with details about Courses, Fees, Placements, Events, and Scholarships. How can I help you today?"
        }

    context = retrieve_context(request.question)

    if not context:
        return {"answer": "Please contact the college office for this information."}

    answer = ask_llm(context, request.question)
    return {"answer": answer}
