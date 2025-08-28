from __future__ import annotations
from typing import Dict, Any

def parse_instruction(text: str) -> Dict[str, Any]:
    t = text.strip().lower()
    payload: Dict[str, Any] = {"intent": "unknown", "args": {}}

    if "fastapi" in t and ("create" in t or "new" in t or "scaffold" in t):
        name = "app"
        for token in t.split():
            if token.endswith("_api") or token.endswith("-api") or token.endswith("api"):
                name = token.replace("-", "_")
        payload["intent"] = "create_fastapi_service"
        payload["args"] = {"name": name}
        return payload

    if t.startswith("run ") or "run the project" in t or "start the server" in t:
        payload["intent"] = "run_project"; return payload

    if "initialize git" in t or "init git" in t or "git init" in t:
        payload["intent"] = "git_init"; return payload

    if ("commit" in t and "git" in t) or t.startswith("commit "):
        msg = "auto-commit"
        if "'" in t:
            try:
                msg = t.split("'",1)[1].rsplit("'",1)[0]
            except Exception:
                pass
        payload["intent"] = "git_commit"; payload["args"]={"message": msg}; return payload

    if ("open a new file" in t or "create file" in t or "new file" in t) and "with content:" in t:
        path = t
        for key in ["open a new file", "create file", "new file"]:
            if key in path:
                path = path.split(key,1)[1]
        path = path.split("with content:")[0].strip().strip(":")
        content = t.split("with content:",1)[1]
        payload["intent"] = "create_file"; payload["args"]={"path": path, "content": content}; return payload

    if t.startswith("delete file") or t.startswith("remove file"):
        path = t.split("file",1)[1].strip()
        payload["intent"] = "delete_file"; payload["args"]={"path": path}; return payload

    if "add endpoint" in t and "fastapi" in t:
        method = "get"
        if "post" in t: method = "post"
        if "put" in t: method = "put"
        if "delete" in t: method = "delete"
        path = "/"
        for token in t.split():
            if token.startswith("/"):
                path = token
                break
        payload["intent"] = "add_fastapi_endpoint"; payload["args"]={"method": method, "path": path}; return payload

    return payload
