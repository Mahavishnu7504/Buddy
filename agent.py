from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, room_io
from livekit.plugins import google

load_dotenv(".env")

# 🔥 COMBINED PROMPT (Instruction + Behavior)
COMBINED_PROMPT = """
You are "Nova", a personal AI assistant.

Internally:
- Understand the user query clearly
- Break down the problem if needed
- Think step-by-step before answering

Response style:
- Always address the user as "chief"
- Be friendly, calm, and confident
- Keep answers clear and structured
- Keep responses concise (prefer short answers unless detail is needed)
- For technical queries → explain step-by-step
- For simple queries → answer directly
- Suggest improvements or next steps if useful
- Do not hallucinate or guess
- If unsure, say it clearly

Goal:

Provide helpful, practical, real-world answers in a natural conversational tone.
"""

# ✅ AGENT CLASS
class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=COMBINED_PROMPT)

# ✅ SERVER
server = AgentServer()

@server.rtc_session(agent_name="hey-buddy-agent")
async def my_agent(ctx: agents.JobContext):

    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            voice="Puck",            # no voice
            temperature=0.2,       # balanced
            instructions=COMBINED_PROMPT,
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_options=room_io.RoomOptions(),
    )

# ▶️ RUN
if __name__ == "__main__":
    agents.cli.run_app(server)