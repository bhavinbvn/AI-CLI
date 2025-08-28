from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
from ..schemas import LogRecord
from .logging import ResultLogger
from ..actions import project_templates, file_ops, git_ops, process_ops


class Executor:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.logger = ResultLogger(self.root)

    def _ok(self, description: str, meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
        rec = LogRecord(
            description=description,
            status="SUCCESS",
            meta=meta or {}
        ).model_dump()
        self.logger.log(rec)
        return rec

    def _fail(self, description: str, err: Exception) -> Dict[str, Any]:
        rec = LogRecord(
            description=description,
            status="FAILED",
            error=str(err)
        ).model_dump()
        self.logger.log(rec)
        return rec

    def handle(self, intent: str, args: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # -----------------------------
            # FastAPI service scaffolding
            # -----------------------------
            if intent == "create_fastapi_service":
                name = args.get("name", "app")
                project_templates.scaffold_fastapi(self.root, name)
                return self._ok(f"Created FastAPI service '{name}'", {"package": name})

            if intent == "add_fastapi_endpoint":
                path = self.root / "app" / "app.py"
                method = args.get("method", "get").lower()
                route = args.get("path", "/")
                if not path.exists():
                    raise FileNotFoundError("FastAPI app not found. Create service first.")
                code = f"""
@app.{method}("{route}")
def _generated_{method}_{route.strip('/').replace('/','_') or 'root'}():
    return {{"path": "{route}", "method": "{method.upper()}"}}
"""
                with open(path, "a", encoding="utf-8") as f:
                    f.write(code)
                return self._ok(f"Added {method.upper()} {route} endpoint", {"file": str(path)})

            # -----------------------------
            # File operations
            # -----------------------------
            if intent == "create_file":
                # accept "path" or "name"
                filename = args.get("path") or args.get("name")
                if not filename:
                    raise ValueError("No file name or path provided")

                # default content based on type
                ftype = args.get("type", "txt")
                content = args.get("content")

                if not content:
                    if ftype == "html":
                        content = """<!DOCTYPE html>
<html>
<head>
    <title>New Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>"""
                    elif ftype == "py":
                        content = "#!/usr/bin/env python3\nprint('Hello World')\n"
                    else:
                        content = ""

                p = file_ops.create_file(self.root, filename, content)
                return self._ok(f"Created file {p}", {"file": str(p), "type": ftype})

            if intent == "delete_file":
                ok = file_ops.delete_file(self.root, args.get("path") or args.get("name"))
                if not ok:
                    raise FileNotFoundError(args.get("path") or args.get("name"))
                return self._ok(f"Deleted file {args.get('path') or args.get('name')}",
                                {"file": args.get("path") or args.get("name")})

            # -----------------------------
            # Git operations
            # -----------------------------
            if intent == "git_init":
                res = git_ops.git_init(self.root)
                return self._ok("Git initialized", {"result": res})

            if intent == "git_commit":
                res = git_ops.git_commit(self.root, args.get("message", "auto-commit"))
                return self._ok("Git commit", {"result": res, "message": args.get("message")})

            # -----------------------------
            # Process runner
            # -----------------------------
            if intent == "run_project":
                meta = process_ops.run_project(self.root)
                return self._ok("Spawned project process", meta)

            # -----------------------------
            # Unknown
            # -----------------------------
            return self._fail(f"Unknown intent: {intent}", Exception("unknown_intent"))

        except Exception as e:
            return self._fail(f"Execution error for intent={intent}", e)
