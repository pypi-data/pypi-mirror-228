from datetime import datetime, timezone

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    expires_in: datetime

    @property
    def is_valid(self) -> bool:
        return self.expires_in.timestamp() > datetime.now(tz=timezone.utc).timestamp()
