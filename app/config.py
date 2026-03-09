import os

API_KEY = os.getenv("API_KEY")

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_NAME = "meta/llama-3.1-8b-instruct"

MAX_TOKENS = 150

if not API_KEY:
    raise RuntimeError("NVIDIA_API_KEY not set in environment")