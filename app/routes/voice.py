from fastapi import APIRouter, Query
import requests
import io
from fastapi.responses import StreamingResponse
from app.config import VOICE_API_KEY

router = APIRouter(prefix="/api", tags=["Voice"])

@router.get("/tts")
def text_to_speech(text: str = Query(...)):
    """
    Text-to-Speech using ElevenLabs Multilingual V2.
    Optimized for natural, human-like voice.
    """
    url = "https://api.elevenlabs.io/v1/text-to-speech/8baRIHZEGj62eS9YHzC6/stream"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": VOICE_API_KEY,
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8},
    }

    # We use stream=True to proxy the audio stream directly to the client
    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code != 200:
        return {"error": response.text}

    return StreamingResponse(
        response.iter_content(chunk_size=1024), media_type="audio/mpeg"
    )
