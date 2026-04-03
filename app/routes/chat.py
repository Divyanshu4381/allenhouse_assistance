from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.retriever import retrieve_context
from app.services.llm import ask_llm

router = APIRouter(prefix="/api", tags=["Chat"])

import re

@router.post("/ask", response_model=ChatResponse)
def ask_college_ai(request: ChatRequest):
    q = re.sub(r'[^\w\s]', '', request.question.strip().lower())
    
    # Handle basic greetings
    greetings = [
        "hi", "hello", "hey", "hi there", "hello there", "namaste", "namaskar", "pranam", 
        "good morning", "good evening", "good afternoon", "hola", "heya", "yo", "sup", 
        "whats up", "how are you", "kaise ho", "hallo", "hii", "hiii", "helloo"
    ]
    if q in greetings:
        return {"answer": "Hello! I am the Allenhouse AI Assistant. I can help you with details about Courses, Fees, Placements, Events, and Scholarships. How can I help you today?"}

    context = retrieve_context(request.question)

    if not context:
        return {
            "answer": "Please contact the college office for this information."
        }

    answer = ask_llm(context, request.question)
    return {"answer": answer}

import requests
import io
from fastapi import Query
from fastapi.responses import StreamingResponse
from app.config import VOICE_API_KEY

@router.get("/tts")
def text_to_speech(text: str = Query(...)):
    url = "https://api.elevenlabs.io/v1/text-to-speech/8baRIHZEGj62eS9YHzC6/stream"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": VOICE_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    # We use stream=True to proxy the audio stream directly to the client
    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code != 200:
        return {"error": response.text}
        
    return StreamingResponse(response.iter_content(chunk_size=1024), media_type="audio/mpeg")