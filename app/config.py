import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
VOICE_API_KEY = os.getenv("VOICE_API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_NAME = "meta/llama-3.1-8b-instruct"

MAX_TOKENS = 150

if not API_KEY:
    raise RuntimeError("NVIDIA_API_KEY not set in environment")
if not VOICE_API_KEY:
    raise RuntimeError("VOICE_API_KEY not set in environment")
