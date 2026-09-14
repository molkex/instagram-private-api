"""Follow, unfollow, and social graph endpoints."""
from __future__ import annotations

class FriendshipModule:
    def __init__(self, client):
        self._client = client

    def follow(self, user_id: str | int) -> dict:
        """Follow a user by ID."""
        return self._client._post(f"/api/v1/friendships/create/{user_id}/")

    def unfollow(self, user_id: str | int) -> dict:
        """Unfollow a user by ID."""
        return self._client._post(f"/api/v1/friendships/destroy/{user_id}/")

    def block(self, user_id: str | int) -> dict:
        """Block a user."""
        return self._client._post(f"/api/v1/friendships/block/{user_id}/")

    def show(self, user_id: str | int) -> dict:
        """Get relationship status with target user (following, followed_by, blocking, etc.)."""
        return self._client._get(f"/api/v1/friendships/show/{user_id}/")
