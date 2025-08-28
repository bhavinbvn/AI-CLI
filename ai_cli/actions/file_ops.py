from pathlib import Path
from ..utils import ensure_within

def create_file(root: Path, relpath: str, content: str) -> Path:
    root = Path(root)
    path = ensure_within(root, Path(relpath))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path

def delete_file(root: Path, relpath: str) -> bool:
    root = Path(root)
    path = ensure_within(root, Path(relpath))
    if path.exists():
        path.unlink()
        return True
    return False
