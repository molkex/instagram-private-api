"""instagram-private-api — Unofficial Instagram & Threads Private API SDK for Python."""
from .client import InstagramAPI
from .threads import ThreadsAPI
from .session import SessionStorage
from .devices import DEVICE_CATALOG, get_device, list_presets, DevicePreset
from .types import UserSummary, MediaItem, CommentItem, DirectThread, StoryItem
from .errors import (
    InstagramError,
    AuthError,
    ChallengeRequiredError,
    RateLimitError,
    InvalidRequestError,
    ServerError,
)

__version__ = "2.0.0"

__all__ = [
    "InstagramAPI",
    "ThreadsAPI",
    "SessionStorage",
    "DevicePreset",
    "DEVICE_CATALOG",
    "get_device",
    "list_presets",
    "UserSummary",
    "MediaItem",
    "CommentItem",
    "DirectThread",
    "StoryItem",
    "InstagramError",
    "AuthError",
    "ChallengeRequiredError",
    "RateLimitError",
    "InvalidRequestError",
    "ServerError",
]
