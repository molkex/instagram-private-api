"""Story viewer, highlight discovery, and story interaction endpoints."""
from __future__ import annotations
import time

class StoryModule:
    """Operations on Instagram Stories and Highlights."""

    def __init__(self, client):
        self._client = client

    def user_stories(self, user_id: str | int) -> dict:
        """Retrieve active stories tray for a target user."""
        return self._client._get("/api/v1/feed/reels_media/", params={"reel_ids": str(user_id)})

    def highlights(self, user_id: str | int) -> dict:
        """Retrieve highlights tray for a target user profile."""
        return self._client._get(f"/api/v1/highlights/{user_id}/highlights_tray/")

    def seen(self, story_media_id: str, taken_at: int | None = None) -> dict:
        """Send authentic story seen/view beacon with paired timestamps."""
        now = int(time.time())
        ts = taken_at or (now - 30)
        data = {
            "reels": {story_media_id: [f"{ts}_{now}"]},
            "reel": "1",
            "live_vod": "0",
        }
        return self._client._post("/api/v2/media/seen/", data=data)

    def like(self, story_id: str | int) -> dict:
        """Like an active story item."""
        data = {"media_id": str(story_id)}
        return self._client._post(f"/api/v1/media/{story_id}/like/", data=data)

    def unlike(self, story_id: str | int) -> dict:
        """Unlike an active story item."""
        data = {"media_id": str(story_id)}
        return self._client._post(f"/api/v1/media/{story_id}/unlike/", data=data)

    def reply(self, story_id: str | int, text: str, recipient_id: str | int) -> dict:
        """Send a Direct message text reply to an active Story."""
        return self._client.direct.reply_to_story(
            story_id=str(story_id),
            text=text,
            recipient_id=str(recipient_id),
        )

    def react(self, story_id: str | int, emoji: str, recipient_id: str | int) -> dict:
        """Send a quick emoji reaction to an active Story."""
        return self._client.direct.react_to_story(
            story_id=str(story_id),
            emoji=emoji,
            recipient_id=str(recipient_id),
        )
