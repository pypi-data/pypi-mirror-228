from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .content_type import ContentType
from .online_stat import OnlineStat
from .platform import Platform


class OrderParameters(BaseModel):
    delay: bool
    delay_time: int
    even_distribution: bool
    even_distribution_time: int
    launch_mode: str
    work_mode: str


class Avg(BaseModel):
    online: OnlineStat
    session_in_seconds: int


class OrderStats(BaseModel):
    active_time_in_seconds: int
    clicks: int
    views: int
    ctr: float
    average: Avg


class Order(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    status: str
    ordered_view_qty: int
    price_per_view: float
    is_autostart: bool
    online_users_limit: int
    platform: Platform
    content_type: ContentType
    parameters: OrderParameters
    extras: Optional[dict] = Field(default=None)
    statistics: Optional[OrderStats] = Field(default=None)
