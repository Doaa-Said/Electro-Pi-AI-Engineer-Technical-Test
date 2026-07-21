from dotenv import load_dotenv
import os

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

AGENT_NAME = "Food Delivery Assistant"

ROOM_NAME = os.getenv("ROOM_NAME", "food-support")

STT_PROVIDER = os.getenv("STT_PROVIDER", "deepgram")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
TTS_PROVIDER = os.getenv("TTS_PROVIDER", "cartesia")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b",
)

