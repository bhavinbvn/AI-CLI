from __future__ import annotations
from pathlib import Path
from typing import List
import json
import pandas as pd
from . import timeutil  # local helper

class ResultLogger:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.log_dir = self.root / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl = self.log_dir / "session.jsonl"
        self.xlsx = self.log_dir / "results.xlsx"

    def write_jsonl(self, record: dict) -> None:
        with open(self.jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=timeutil.json_default) + "\n")

    def write_xlsx(self, rows: List[dict]) -> None:
        df = pd.DataFrame(rows)
        if self.xlsx.exists():
            try:
                existing = pd.read_excel(self.xlsx)
                df = pd.concat([existing, df], ignore_index=True)
            except Exception:
                pass
        df.to_excel(self.xlsx, index=False)

    def log(self, record: dict) -> None:
        self.write_jsonl(record)
        self.write_xlsx([record])
