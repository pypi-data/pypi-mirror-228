from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OnlineStat(BaseModel):
    created_at: Optional[datetime] = Field(default=None)
    in_settings: int
    in_fact: int
