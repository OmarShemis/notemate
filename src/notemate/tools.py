"""Local notes, time and bounded arithmetic tools."""

import ast
from datetime import datetime
import math
import operator
import os
from pathlib import Path

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def get_current_time() -> str:
    """Get the current local date and time."""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


def calculate(expression: str) -> str:
    """Calculate arithmetic using numbers, +, -, *, / and parentheses."""
    if len(expression) > 256:
        return "Error: expression is too long."

    def evaluate(node, depth=0):
        if depth > 20:
            raise ValueError("expression is too deeply nested")
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            result = node.value
        elif isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            result = OPERATORS[type(node.op)](
                evaluate(node.left, depth + 1), evaluate(node.right, depth + 1)
            )
        elif isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            result = evaluate(node.operand, depth + 1)
            if isinstance(node.op, ast.USub):
                result = -result
        else:
            raise ValueError("only numbers and + - * / ( ) are allowed")
        if not math.isfinite(result) or abs(result) > 1e100:
            raise ValueError("result is out of range")
        return result

    try:
        return str(evaluate(ast.parse(expression.strip(), mode="eval").body))
    except (
        SyntaxError,
        ValueError,
        ZeroDivisionError,
        OverflowError,
        RecursionError,
    ) as error:
        return f"Error: {error}"


def notes_path() -> Path:
    return Path(
        os.environ.get("NOTEMATE_NOTES_FILE", str(Path.cwd() / "data" / "notes.txt"))
    ).expanduser()


def save_note(note: str) -> str:
    """Append a nonempty note to the local notes file."""
    note = note.strip()
    if not note or len(note) > 10000:
        return "Error: note must contain between 1 and 10000 characters."
    try:
        path = notes_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(f"- {note}\n")
    except OSError:
        return "Error: could not save the note. Check the notes folder permissions."
    return "Note saved."


def read_notes() -> str:
    """Read saved local notes; return a friendly message if none exist."""
    try:
        text = notes_path().read_text(encoding="utf-8")
        return text if text.strip() else "No notes saved yet."
    except FileNotFoundError:
        return "No notes saved yet."
    except (OSError, UnicodeError):
        return "Error: could not read the notes file."
