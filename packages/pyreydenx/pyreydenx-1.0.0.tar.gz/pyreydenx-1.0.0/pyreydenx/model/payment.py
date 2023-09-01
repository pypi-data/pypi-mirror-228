from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Payment(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    payed_at: Optional[datetime] = Field(default=None)
    order_id: int
    amount: float
    external_id: Optional[str] = Field(default=None)
    receipt: Optional[str] = Field(default=None)
