from enum import Enum


class Platform(str, Enum):
    TWITCH = 'twitch'
    YOUTUBE = 'youtube'
    TROVO = 'trovo'
    GOODGAME = 'goodgame'
    VKPLAY = 'vkplay'
