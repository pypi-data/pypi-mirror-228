from pydantic import BaseModel


class SiteStat(BaseModel):
    domain: str
    views: int
    clicks: int
    ctr: float
