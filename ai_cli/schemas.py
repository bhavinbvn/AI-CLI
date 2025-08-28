from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class LogRecord(BaseModel):
    test_name: str = Field(default="ad-hoc")
    description: str
    status: str
    error: Optional[str] = None
    screenshot_link: Optional[str] = None
    meta: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)
