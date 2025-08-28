from __future__ import annotations
import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.json import JSON
from .nlu import parse_instruction
from .core.executor import Executor
import json
from ai_cli.core import timeutil
from datetime import datetime

from .nlu import parse_instruction
from .ai_nlu import parse_instruction_ai


app = typer.Typer(help="AI-Native CLI – Natural Language to dev actions")
console = Console()

@app.command()
def chat(
    instruction: Optional[list[str]] = typer.Argument(
        None,
        help="Natural language instruction (free text)",
    ),
    root: str = typer.Option(".", help="Project root directory"),
):
    """Parse the given instruction and execute."""
    if instruction:
        instruction = " ".join(instruction)  # merge into one string

    if not instruction:
        console.print("[bold]Interactive mode[/bold]. Type 'exit' to quit.")
        while True:
            text = typer.prompt("> ")
            if text.strip().lower() in {"exit", "quit"}:
                break
            _run(text, root)
    else:
        _run(instruction, root)

def _json_safe(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# def _run(text: str, root: str):
#     console.rule("[bold cyan]NLU Parse[/]")
#     payload = parse_instruction(text)
#     console.print(JSON.from_data(payload))
#     console.rule("[bold cyan]Execute[/]")
#     ex = Executor(Path(root))
#     res = ex.handle(payload["intent"], payload.get("args", {}))
#     console.print(JSON.from_data(json.loads(json.dumps(res, default=timeutil.json_default))))
#     console.rule()

def _run(text: str, root: str):
    console.rule("[bold cyan]NLU Parse[/]")
    payload = parse_instruction(text)

    # 🔥 fallback to AI if unknown
    if payload["intent"] == "unknown":
        console.print("[yellow]Fallback: Using AI parser[/yellow]")
        payload = parse_instruction_ai(text)

    console.print(JSON.from_data(payload))
    console.rule("[bold cyan]Execute[/]")
    ex = Executor(Path(root))
    res = ex.handle(payload["intent"], payload.get("args", {}))
    console.print(JSON.from_data(json.loads(json.dumps(res, default=_json_safe))))
    console.rule()




if __name__ == "__main__":
    app()
