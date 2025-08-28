import subprocess, shlex
from pathlib import Path

def run_project(root: Path):
    if (root / "requirements.txt").exists() and "uvicorn" in (root / "requirements.txt").read_text():
        return spawn("python -m app", root)
    if (root / "app").exists():
        return spawn("python -m app", root)
    if (root / "main.py").exists():
        return spawn("python main.py", root)
    raise RuntimeError("No runnable entry found. Create a FastAPI service first.")

def spawn(cmd: str, cwd: Path):
    out = (cwd / "logs" / "process.out")
    err = (cwd / "logs" / "process.err")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "ab") as fo, open(err, "ab") as fe:
        proc = subprocess.Popen(shlex.split(cmd), cwd=str(cwd), stdout=fo, stderr=fe)
    return {"pid": proc.pid, "cmd": cmd, "cwd": str(cwd), "stdout": str(out), "stderr": str(err)}
