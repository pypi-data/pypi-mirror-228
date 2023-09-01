from pydantic import BaseModel


class IdQty(BaseModel):
    id: int
    quantity: int
