from config import (
    STT_PROVIDER,
    LLM_PROVIDER,
    TTS_PROVIDER,
    GROQ_API_KEY,
)

# Import plugins ONLY once on the main thread
from livekit.plugins import groq
from livekit.agents import inference


# --------------------------
# STT
# --------------------------
def create_stt():

    if STT_PROVIDER == "deepgram":
        return inference.STT.from_model_string(
            "deepgram/nova-3"
        )

    if STT_PROVIDER == "groq":
        return groq.STT(
            api_key=GROQ_API_KEY,
            model="whisper-large-v3-turbo",
        )

    raise ValueError(
        f"Unsupported STT provider: {STT_PROVIDER}"
    )


# --------------------------
# LLM
# --------------------------
def create_llm():

    if LLM_PROVIDER == "groq":
        return groq.LLM(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
        )

    raise ValueError(
        f"Unsupported LLM provider: {LLM_PROVIDER}"
    )


# --------------------------
# TTS
# --------------------------
def create_tts():

    if TTS_PROVIDER == "cartesia":
        return inference.TTS.from_model_string(
            "cartesia/sonic-3"
        )

    raise ValueError(
        f"Unsupported TTS provider: {TTS_PROVIDER}"
    )