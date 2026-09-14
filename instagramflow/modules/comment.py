"""Comment engagement and moderation endpoints."""
from __future__ import annotations

class CommentModule:
    """Operations on post and Reels comments."""

    def __init__(self, client):
        self._client = client

    def list(self, media_id: str | int, min_id: str | None = None) -> dict:
        """Fetch comments for a media post or reel."""
        params = {}
        if min_id:
            params["min_id"] = min_id
        return self._client._get(f"/api/v1/media/{media_id}/comments/", params=params or None)

    def replies(self, media_id: str | int, comment_id: str | int, min_id: str | None = None) -> dict:
        """Fetch child comment replies under a specific parent comment."""
        params = {}
        if min_id:
            params["min_id"] = min_id
        return self._client._get(
            f"/api/v1/media/{media_id}/comments/{comment_id}/child_comments/",
            params=params or None,
        )

    def add(
        self,
        media_id: str | int,
        text: str,
        replied_to_comment_id: str | int | None = None,
    ) -> dict:
        """Post a comment or reply to an existing comment on a media item."""
        data = {"comment_text": text}
        if replied_to_comment_id:
            data["replied_to_comment_id"] = str(replied_to_comment_id)
        return self._client._post(f"/api/v1/media/{media_id}/comment/", data=data)

    def like(self, comment_id: str | int) -> dict:
        """Like a specific comment."""
        return self._client._post(f"/api/v1/media/{comment_id}/comment_like/")

    def unlike(self, comment_id: str | int) -> dict:
        """Unlike a specific comment."""
        return self._client._post(f"/api/v1/media/{comment_id}/comment_unlike/")

    def delete(self, media_id: str | int, comment_id: str | int) -> dict:
        """Delete a comment posted by the current account."""
        return self._client._post(f"/api/v1/media/{media_id}/comment/{comment_id}/delete/")

    def pin(self, media_id: str | int, comment_id: str | int) -> dict:
        """Pin a comment to the top of the comments thread."""
        return self._client._post(f"/api/v1/media/{media_id}/comment/{comment_id}/pin/")

    def unpin(self, media_id: str | int, comment_id: str | int) -> dict:
        """Unpin a previously pinned comment."""
        return self._client._post(f"/api/v1/media/{media_id}/comment/{comment_id}/unpin/")
