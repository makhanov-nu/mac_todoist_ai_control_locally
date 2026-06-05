# Local AI Agent for Mac — Powered by Gemma4:12B

Control your Mac apps with a fully local AI model. No cloud. No API keys leaving your machine.

## How it works

A locally running Gemma4:12B processes your voice input and interacts with your apps via tool calls.
This example creates a Todoist task from a voice reminder.

**RAM usage:** ~10GB

## Setup

Pull the model:
```bash
ollama run gemma4:12b
```

Install dependencies:
```bash
pip install langchain langchain-openai todoist-api-python
```

Add your Todoist API token to `main.py`:
```python
TODOIST_TOKEN = "your_token_here"
```

## Run

```bash
python main.py
```

## Result

Check your Todoist — a new task will appear based on your audio input.
