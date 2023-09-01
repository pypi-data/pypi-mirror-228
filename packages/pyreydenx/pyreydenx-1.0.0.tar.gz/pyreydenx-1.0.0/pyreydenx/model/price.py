from pydantic import BaseModel


class MinMaxStep(BaseModel):
    min: int
    max: int
    step: int


class Price(BaseModel):
    id: int
    name: str
    format: str
    price: float
    description: str
    views: MinMaxStep
    online_viewers: MinMaxStep
