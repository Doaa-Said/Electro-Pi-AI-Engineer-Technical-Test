Extending the Voice Agent for Barge-In and a Second Tool

A useful extension to the voice agent is barge-in (interruption) handling, allowing the user to interrupt the assistant while it is speaking. This creates a more natural conversational experience similar to commercial voice assistants. To implement this, the agent should continuously listen for voice activity (using Voice Activity Detection) even while Text-to-Speech (TTS) is playing. When new speech is detected, the current TTS stream should be immediately cancelled, any queued audio should be discarded, and the new user utterance should be sent to the Speech-to-Text (STT) pipeline. The conversation state should be preserved so the LLM receives the interrupted dialogue as context instead of starting a new conversation. To avoid accidental interruptions caused by noise, a short speech threshold (e.g., 200–300 ms of continuous speech) can be required before stopping playback.

To make the assistant more capable, a second tool could be added alongside the existing order-related tools. For example, a find_nearest_restaurant(location) tool could return nearby restaurant locations or operating hours. The tool should expose a well-defined schema so the LLM knows exactly how to call it. An example schema is:

def find_nearest_restaurant(location: str) -> dict:
    """
    Args:
        location: User's city or GPS location.

    Returns:
        {
            "restaurant": str,
            "address": str,
            "distance_km": float
        }
    """

The implementation should validate all inputs before executing the tool. For example, empty or invalid locations should immediately return a validation error instead of querying the backend.

Robust error handling is equally important. Every tool call should be wrapped in a try/except block to catch API failures, network timeouts, or unexpected exceptions. Instead of exposing internal errors to the user, the assistant should return a friendly response such as, "I'm sorry, I couldn't retrieve nearby restaurants at the moment. Please try again in a few moments." The error should also be logged for debugging, and optional retry logic with a timeout can be added for transient failures. This approach ensures that tool failures do not crash the conversation and that the user continues to receive a helpful response even when backend services are temporarily unavailable.