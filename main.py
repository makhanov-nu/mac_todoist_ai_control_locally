import os
from todoist_api_python.api import TodoistAPI

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# developer tools
TODOIST_TOKEN = "your_todoist_token_here"

todoist = TodoistAPI(TODOIST_TOKEN)

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

llm = ChatOpenAI(
    model="gemma4:12b",
    base_url="http://localhost:11434/v1",
    api_key="not-needed",
)

agent = create_agent(        
    llm,
    tools=[create_todoist_task],
)


# -------------------------
# TEST
# -------------------------

response = agent.invoke(
    {
        "messages": [
            ("user", "Remind me next Tuesday to cancel Spotify subscription")
        ]
    }
)

print(response["messages"][-1].content)
