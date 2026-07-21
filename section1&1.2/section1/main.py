import asyncio
import logging

from dotenv import load_dotenv

from livekit.agents import (
    AgentServer,
    AgentSession,
    JobContext,
    cli,
)

from livekit.plugins import silero

from provider_factory import (
    create_stt,
    create_llm,
    create_tts,
)

from agent import FoodSupportAgent

from config import ROOM_NAME

load_dotenv()

logging.basicConfig(level=logging.INFO)

server = AgentServer()


@server.rtc_session(agent_name="food-support-agent")
async def entrypoint(ctx: JobContext):

    print("=" * 60)
    print("Worker received job")
    print("=" * 60)

    print("Expected room :", ROOM_NAME)
    print("Connected room:", ctx.room.name)

    print("\nWaiting for participant...")

    participant = await ctx.wait_for_participant()

    print(f"\nParticipant joined: {participant.identity}")

    print("\nRemote participants:")

    for p in ctx.room.remote_participants.values():
        print(f"Participant: {p.identity}")

        for pub in p.track_publications.values():
            print(f" SID        : {pub.sid}")
            print(f" Kind       : {pub.kind}")
            print(f" Subscribed : {pub.subscribed}")
            print(f" Muted      : {pub.muted}")

    print("\nCreating providers...")

    stt_provider = create_stt()
    llm_provider = create_llm()
    tts_provider = create_tts()

    print("STT :", type(stt_provider))
    print("LLM :", type(llm_provider))
    print("TTS :", type(tts_provider))

    session = AgentSession(
        stt=stt_provider,
        llm=llm_provider,
        tts=tts_provider,
        vad=silero.VAD.load(),
    )

    @session.on("user_input_transcribed")
    def _(ev):
        print(f"\nUSER: {ev.transcript}")

    @session.on("conversation_item_added")
    def _(ev):
        print(f"\nEVENT: {ev}")

    print("\nStarting session...")

    await session.start(
        room=ctx.room,
        agent=FoodSupportAgent(),
    )

    print("\nSession started successfully.")

    await asyncio.Event().wait()


if __name__ == "__main__":
    cli.run_app(server)