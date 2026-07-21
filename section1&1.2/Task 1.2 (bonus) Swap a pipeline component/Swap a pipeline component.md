# Provider Abstraction and Vendor Independence

## Overview

The voice assistant was designed using a provider abstraction layer that separates the application logic from vendor-specific implementations. Instead of directly instantiating STT, LLM, or TTS providers throughout the project, all provider selection is centralized in `provider_factory.py`.

This architecture allows the application to switch between different speech or language providers by changing configuration values rather than modifying the business logic.

The remainder of the application—including:

- `main.py`
- `agent.py`
- `tools.py`
- `prompts.py`
- `client.py`

remains completely unchanged regardless of which provider is selected.

---

# Current Voice Pipeline

The current implementation uses the following providers:

| Component | Provider | Model |
|-----------|----------|-------|
| Speech-to-Text (STT) | Deepgram | Nova-3 |
| Large Language Model (LLM) | Groq | Llama 3.3 70B Versatile |
| Text-to-Speech (TTS) | Cartesia | Sonic-3 |

These providers are configured through environment variables.

```env
STT_PROVIDER=deepgram
LLM_PROVIDER=groq
TTS_PROVIDER=cartesia
```

---

# Provider Factory Design

The application creates providers using dedicated factory methods.

```python
session = AgentSession(
    stt=create_stt(),
    llm=create_llm(),
    tts=create_tts(),
    vad=silero.VAD.load(),
)
```

`main.py` never imports Deepgram, Groq, Cartesia, or any vendor-specific SDK.

Instead, it relies on the abstraction layer.

---

# Current STT Implementation

```python
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
```

Only one function determines which provider will be used.

---

# Current LLM Implementation

```python
def create_llm():

    if LLM_PROVIDER == "groq":
        return groq.LLM(
            api_key=GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
        )
```

The application communicates only with the generic LLM interface returned by the factory.

---

# Current TTS Implementation

```python
def create_tts():

    if TTS_PROVIDER == "cartesia":
        return inference.TTS.from_model_string(
            "cartesia/sonic-3"
        )
```

Again, the application has no dependency on Cartesia outside the factory.

---

# Swapping the STT Provider

Suppose we want to replace Deepgram with Groq Whisper.

The only required modification is the environment variable:

```env
STT_PROVIDER=groq
```

The factory automatically selects the Groq implementation.

```python
if STT_PROVIDER == "groq":
    return groq.STT(
        api_key=GROQ_API_KEY,
        model="whisper-large-v3-turbo",
    )
```

No other source file requires modification.

---

# Swapping the TTS Provider

If another provider such as OpenAI TTS is preferred, only the factory changes.

```python
from livekit.plugins import openai

def create_tts():

    if TTS_PROVIDER == "cartesia":
        return inference.TTS.from_model_string(
            "cartesia/sonic-3"
        )

    if TTS_PROVIDER == "openai":
        return openai.TTS(
            api_key=OPENAI_API_KEY,
            model="gpt-4o-mini-tts",
        )
```

The configuration becomes

```env
TTS_PROVIDER=openai
```

No changes are required in:

- `main.py`
- `tools.py`
- `prompts.py`
- `agent.py`
- `client.py`

---

# Advantages of the Design

## 1. Vendor Independence

The application does not depend on a specific speech or language provider.

Changing vendors requires only configuration updates.

---

## 2. Maintainability

All provider-specific code is isolated in one file.

Future maintenance is simpler because modifications are localized.

---

## 3. Extensibility

Adding another provider requires implementing only a new branch inside the factory.

For example:

```python
if STT_PROVIDER == "azure":
    ...
```

or

```python
if TTS_PROVIDER == "elevenlabs":
    ...
```

No application logic changes are necessary.

---

## 4. Scalability

Different deployments can use different providers depending on:

- Pricing
- Latency
- Regional availability
- Model quality

without changing the voice agent implementation.

---

# Design Summary

The project follows a modular architecture:

```text
AgentSession
      │
      ▼
create_stt()
create_llm()
create_tts()
      │
      ▼
Selected Provider
(Deepgram / Groq / Cartesia / OpenAI / Azure / ...)
```

The application communicates only with the factory functions rather than directly interacting with vendor SDKs.

---

# Conclusion

The implemented provider abstraction successfully decouples the voice pipeline from any individual vendor.

The application currently operates using:

- Deepgram STT
- Groq LLM
- Cartesia TTS

Replacing any provider requires only updating the configuration and, if necessary, adding a corresponding implementation in `provider_factory.py`.

This design minimizes code changes, improves maintainability, and enables seamless migration between speech and language service providers while preserving the rest of the application's architecture.