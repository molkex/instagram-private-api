"""Follow, unfollow, Close Friends, and social graph endpoints."""
from __future__ import annotations
import json

class FriendshipModule:
    """Operations on followers, followings, blocking, and Close Friends lists."""

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

    def unblock(self, user_id: str | int) -> dict:
        """Unblock a previously blocked user."""
        return self._client._post(f"/api/v1/friendships/unblock/{user_id}/")

    def show(self, user_id: str | int) -> dict:
        """Get relationship status with target user (following, followed_by, blocking, etc.)."""
        return self._client._get(f"/api/v1/friendships/show/{user_id}/")

    def followers(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Paginate account followers list."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get(f"/api/v1/friendships/{user_id}/followers/", params=params or None)

    def following(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Paginate accounts followed by this user."""
        params = {}
        if max_id:
            params["max_id"] = max_id
        return self._client._get(f"/api/v1/friendships/{user_id}/following/", params=params or None)

    def close_friend_add(self, user_id: str | int) -> dict:
        """Add target user to Close Friends (Besties) list."""
        data = {
            "source": "audience_manager",
            "module": "favorites_home_list",
            "add": json.dumps([int(user_id)]),
            "remove": json.dumps([]),
        }
        return self._client._post("/api/v1/friendships/set_besties/", data=data)

    def close_friend_remove(self, user_id: str | int) -> dict:
        """Remove target user from Close Friends (Besties) list."""
        data = {
            "source": "audience_manager",
            "module": "favorites_home_list",
            "add": json.dumps([]),
            "remove": json.dumps([int(user_id)]),
        }
        return self._client._post("/api/v1/friendships/set_besties/", data=data)

    def mute_posts(self, user_id: str | int) -> dict:
        """Mute feed posts from a followed account."""
        data = {"target_posts_author_id": str(user_id)}
        return self._client._post("/api/v1/friendships/mute_posts_or_story_from_follow/", data=data)

    def unmute_posts(self, user_id: str | int) -> dict:
        """Unmute feed posts from a followed account."""
        data = {"target_posts_author_id": str(user_id)}
        return self._client._post("/api/v1/friendships/unmute_posts_or_story_from_follow/", data=data)

    def mute_stories(self, user_id: str | int) -> dict:
        """Mute active stories from a followed account."""
        data = {"target_reel_author_id": str(user_id)}
        return self._client._post("/api/v1/friendships/mute_posts_or_story_from_follow/", data=data)

    def unmute_stories(self, user_id: str | int) -> dict:
        """Unmute active stories from a followed account."""
        data = {"target_reel_author_id": str(user_id)}
        return self._client._post("/api/v1/friendships/unmute_posts_or_story_from_follow/", data=data)
