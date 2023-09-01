from pydantic import BaseModel

from .platform import Platform


class SmoothGain(BaseModel):
    enabled: bool
    minutes: int


class NewOrderParameters(BaseModel):
    price_id: int
    number_of_views: int
    number_of_viewers: int
    launch_mode: str
    delay_time: int
    smooth_gain: SmoothGain

    @property
    def platform(self) -> str:
        return ''


class TwitchOrder(NewOrderParameters):
    twitch_id: int

    @property
    def platform(self) -> str:
        return Platform.TWITCH.value


class YouTubeOrder(NewOrderParameters):
    channel_url: str

    @property
    def platform(self) -> str:
        return Platform.YOUTUBE.value
