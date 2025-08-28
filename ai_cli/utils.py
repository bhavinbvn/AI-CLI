from pathlib import Path

def ensure_within(base: Path, target: Path) -> Path:
    base = base.resolve()
    tgt = (base / target).resolve()
    if not str(tgt).startswith(str(base)):
        raise ValueError("Path escape attempt blocked.")
    return tgt
