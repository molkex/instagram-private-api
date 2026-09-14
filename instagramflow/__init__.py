"""instagram-private-api — Unofficial Instagram & Threads Private API SDK for Python."""
from .client import InstagramAPI
from .threads import ThreadsAPI
from .errors import (
    InstagramError,
    AuthError,
    ChallengeRequiredError,
    RateLimitError,
    InvalidRequestError,
    ServerError,
)

__version__ = "1.0.0"

__all__ = [
    "InstagramAPI",
    "ThreadsAPI",
    "InstagramError",
    "AuthError",
    "ChallengeRequiredError",
    "RateLimitError",
    "InvalidRequestError",
    "ServerError",
]
