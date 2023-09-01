import datetime

from pydantic import BaseModel


class DateQty(BaseModel):
    date: datetime.date
    quantity: int
