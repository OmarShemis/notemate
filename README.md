# NoteMate - Local AI Notes Assistant

A command-line assistant built with Pydantic AI and Ollama. It can save/read local notes, tell the current time and perform bounded arithmetic through tools. Conversation history is kept for the current session.

## Setup

Requires Python 3.11+, uv, and a running Ollama server with a tool-capable model.

```powershell
uv sync
ollama pull qwen3.5:4b
uv run notemate
```

Alternatively use `python -m pip install -r requirements.txt`, then `notemate`.
Copy `.env.example` to `.env` if you want to change the model, endpoint or notes location. Defaults: `qwen3.5:4b`, `http://localhost:11434/v1`, and `./data/notes.txt`. Run from the project directory for a consistent default notes location. The original `scr/notemate/agent.py` launcher works after installation.

Examples: `Save a note: revise linear algebra on Friday`, `Read my notes`, `Calculate (23 * 7) + 1`.

## Development

```powershell
uv run python -m unittest discover -s tests -v
uv build
```

`src/notemate/agent.py` contains the agent factory and CLI; `tools.py` handles arithmetic and notes. Arithmetic is parsed with an allowlisted AST, never evaluated as Python code. Offline tests use a test model and temporary notes files.

## Data and limitations

Notes and `.env` files are excluded from version control. Existing notes in an older location are not moved automatically; set `NOTEMATE_NOTES_FILE` to that file to keep using them. With the default endpoint inference stays local; changing the endpoint can send prompts/notes to that provider. Model downloads require network access. This is a learning project; model tool selection and answer quality depend on the chosen model. Each request is capped at 15 model requests.
