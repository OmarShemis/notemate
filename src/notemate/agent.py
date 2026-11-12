"""Ollama agent factory and interactive command-line entry point."""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.usage import UsageLimits
from .tools import calculate, get_current_time, read_notes, save_note


def build_agent(model=None):
    if model is None:
        model = OllamaModel(
            os.environ.get("OLLAMA_MODEL", "qwen3.5:4b"),
            provider=OllamaProvider(
                base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            ),
        )
    return Agent(
        model,
        tools=[get_current_time, calculate, save_note, read_notes],
        instructions="You are NoteMate, a local notes assistant. Use tools when useful. Save notes only when the user requests it. Keep answers concise.",
    )


async def chat():
    load_dotenv(Path.cwd() / ".env")
    agent = build_agent()
    print("NoteMate ready. Type 'quit' to exit.")
    history = []
    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in {"quit", "exit"}:
            break
        if not prompt:
            continue
        try:
            result = await agent.run(
                prompt,
                message_history=history,
                usage_limits=UsageLimits(request_limit=15),
            )
            history = result.all_messages()
            print(f"Agent: {result.output}\n")
        except Exception as error:
            print(
                f"Request failed ({type(error).__name__}). Check Ollama is running and the configured model is installed."
            )


def main():
    try:
        asyncio.run(chat())
    except KeyboardInterrupt:
        pass
    return 0
