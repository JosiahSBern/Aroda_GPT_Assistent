import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContent().append_message(
        role="system",
        text=(
            "You are a voice assistant under the name Aurora that responds to the user using voice and text. "
            "You use concise responses. "
            "You are able to add events to Google Calendar and Trello."
        ),
    )

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
    )
    await assistant.start(ctx.room)

    await asyncio.sleep(1)
    await assistant.say("Hello, how can I help today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


    