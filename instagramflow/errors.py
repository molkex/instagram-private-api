"""Exceptions for instagramflow SDK."""

class InstagramError(Exception):
    """Base exception for all Instagram SDK errors."""
    pass

class AuthError(InstagramError):
    """Authentication or token verification failed."""
    pass

class ChallengeRequiredError(AuthError):
    """Account triggered a checkpoint or verification challenge (SMS/Email/Selfie)."""
    def __init__(self, message: str, challenge_url: str | None = None):
        super().__init__(message)
        self.challenge_url = challenge_url

class RateLimitError(InstagramError):
    """Action blocked or rate limited by Instagram."""
    def __init__(self, message: str, retry_after: int | None = None):
        super().__init__(message)
        self.retry_after = retry_after

class InvalidRequestError(InstagramError):
    """Malformed request or invalid arguments."""
    pass

class ServerError(InstagramError):
    """Signing server or upstream Instagram server error."""
    pass
