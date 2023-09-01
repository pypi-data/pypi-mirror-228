from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    id: str
    url: str
    expires_at: datetime
