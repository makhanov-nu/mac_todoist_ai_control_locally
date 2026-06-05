import os
import base64
from pathlib import Path
from todoist_api_python.api import TodoistAPI

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage



# -------------------------
# CONFIG
# -------------------------

TODOIST_TOKEN = "your_todoist_token_here"  # replace with your Todoist API token

AUDIO_FILE    = "reminder.wav" # your audio file with instructions, e.g. "Remind me to call my wife after 3 hours"

todoist = TodoistAPI(TODOIST_TOKEN)



# -------------------------
# TOOL
# -------------------------

@tool
def create_todoist_task(
    content: str,
    due_date: str,
) -> str:
    """
    Create a Todoist task.

    Args:
        content: task description
        due_date: natural language due date such as
                  'tomorrow', 'next Tuesday', 'Friday 5pm'
    """

    task = todoist.add_task(
        content=content,
        due_string=due_date,
    )

    return (
        f"Created task '{task.content}' "
        f"with due date '{due_date}'"
    )


# -------------------------
# LLM
# -------------------------

llm = ChatOpenAI(
    model="gemma4:12b", 
    base_url="http://localhost:11434/v1", 
    api_key="not-needed"
)

# -------------------------
# AGENT
# -------------------------

agent = create_react_agent(
    llm,
    tools=[create_todoist_task],
)

# -------------------------
# AUDIO HELPER
# -------------------------

def load_audio_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("utf-8")

# -------------------------
# TEST for text input
# -------------------------

response = agent.invoke(
    {
        "messages": [
            (
                "user",
                "Remind me next Tuesday to cancel Spotify subscription"
            )
        ]
    }
)

print(response)


# -------------------------
# AUDIO TEST
# -------------------------

# audio_b64 = load_audio_b64(AUDIO_FILE)

# message = HumanMessage(
#     content=[
#         {
#             "type": "input_audio",          # content block type for audio
#             "input_audio": {
#                 "data": audio_b64,
#                 "format": "wav",            # or "mp3", "ogg", etc.
#             },
#         },
#         {
#             "type": "text",
#             "text": "Listen to this audio and create the appropriate Todoist task.",
#         },
#     ]
# )

# response = agent.invoke({"messages": [message]})
# print(response["messages"][-1].content)



