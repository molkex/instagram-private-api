"""Media upload, Reels publishing, and feed post endpoints."""
from __future__ import annotations
import time

class MediaModule:
    def __init__(self, client):
        self._client = client

    def like(self, media_id: str | int) -> dict:
        """Like a media item with companion telemetry."""
        return self._client._post(f"/api/v1/media/{media_id}/like/")

    def unlike(self, media_id: str | int) -> dict:
        """Unlike a media item."""
        return self._client._post(f"/api/v1/media/{media_id}/unlike/")

    def comment(self, media_id: str | int, text: str) -> dict:
        """Post a comment on a media item."""
        data = {"comment_text": text}
        return self._client._post(f"/api/v1/media/{media_id}/comment/", data=data)

    def configure_timeline_photo(self, upload_id: str, caption: str = "") -> dict:
        """Publish uploaded photo to timeline."""
        data = {
            "upload_id": upload_id,
            "caption": caption,
            "source_type": "4",
        }
        return self._client._post("/api/v1/media/configure/", data=data)
