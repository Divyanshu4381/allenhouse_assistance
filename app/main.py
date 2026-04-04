from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routes.chat import router as chat_router
import os

app = FastAPI(title="College AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev ke liye ok
    allow_credentials=True,
    allow_methods=["*"],  # OPTIONS, POST, etc
    allow_headers=["*"],
)

app.include_router(chat_router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEW_DIR = os.path.join(BASE_DIR, "view")

# Serve public directory
app.mount(
    "/public", StaticFiles(directory=os.path.join(VIEW_DIR, "public")), name="public"
)


@app.get("/")
def serve_home():
    return FileResponse(os.path.join(VIEW_DIR, "index.html"))


@app.get("/speech-agent.js")
def serve_speech_agent():
    return FileResponse(os.path.join(VIEW_DIR, "speech-agent.js"))
