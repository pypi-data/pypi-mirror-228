from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    username: str
    date_joined: datetime
    email: str
    is_active: bool
    is_blocked: bool
    is_reseller: bool
    image_url: Optional[str] = Field(default=None)
    currency_id: int
    discount: int = Field(alias='discount_value')
    twitch_id: int
    twitch_login: Optional[str] = Field(default=None)

    @property
    def has_image(self) -> bool:
        return self.image_url is not None and len(self.image_url) > 0


class Balance(BaseModel):
    id: int
    amount: int
    currency_id: int
    user_id: int
    formatted_amount: float
    currency: str
