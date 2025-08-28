from pathlib import Path
from ..utils import ensure_within

FASTAPI_MAIN = """from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
"""

UVICORN_RUN = """import uvicorn
from app import app
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
"""

REQ = """fastapi
uvicorn
"""

def scaffold_fastapi(root: Path, name: str = "app") -> None:
    root = Path(root)
    pkg = ensure_within(root, Path(name))
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "__main__.py").write_text(UVICORN_RUN, encoding="utf-8")
    (pkg / "app.py").write_text(FASTAPI_MAIN, encoding="utf-8")
    (root / "requirements.txt").write_text(REQ, encoding="utf-8")
    (root / ".gitignore").write_text(".venv\n__pycache__\nlogs\n", encoding="utf-8")
