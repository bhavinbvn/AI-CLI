import subprocess, shlex
from pathlib import Path

def run(cmd: str, cwd: Path):
    return subprocess.run(shlex.split(cmd), cwd=str(cwd), capture_output=True, text=True)

def git_init(root: Path):
    r1 = run("git init", root)
    if r1.returncode != 0:
        raise RuntimeError(r1.stderr or r1.stdout)
    run("git add -A", root)
    run('git commit -m "chore: initial commit" --allow-empty', root)
    return "initialized"

def git_commit(root: Path, message: str):
    r1 = run("git add -A", root)
    if r1.returncode != 0:
        raise RuntimeError(r1.stderr or r1.stdout)
    r2 = run(f'git commit -m "{message}"', root)
    if r2.returncode != 0:
        r2 = run(f'git commit -m "{message}" --allow-empty', root)
        if r2.returncode != 0:
            raise RuntimeError(r2.stderr or r2.stdout)
    return "committed"
