from datetime import datetime
from typing import Optional, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')


class Result(BaseModel, Generic[T]):
    request_id: str
    cached: bool
    cache_expires_at: Optional[datetime] = Field(default=None)
    cursor: Optional[str] = Field(default=None)
    result: T

    @property
    def has_next(self) -> bool:
        return isinstance(self.cursor, str) and len(self.cursor) > 0
