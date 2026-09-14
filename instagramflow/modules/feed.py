"""Feed, timeline, and explore discovery endpoints."""
from __future__ import annotations

class FeedModule:
    def __init__(self, client):
        self._client = client

    def timeline(self, count: int = 15, max_id: str | None = None) -> dict:
        """Fetch timeline feed items with automatic companion CDN prefetch."""
        params = {"count": count}
        if max_id:
            params["max_id"] = max_id
        return self._client._get("/api/v1/feed/timeline/", params=params)

    def user(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Retrieve user media grid posts."""
        url = f"/api/v1/feed/user/{user_id}/"
        params = {"max_id": max_id} if max_id else None
        return self._client._get(url, params=params)

    def explore(self, is_prefetch: bool = False) -> dict:
        """Fetch recommended posts from the Explore tab."""
        params = {"is_prefetch": "true" if is_prefetch else "false"}
        return self._client._get("/api/v1/discover/topical_explore/", params=params)
