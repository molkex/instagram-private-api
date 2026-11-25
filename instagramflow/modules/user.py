"""User profile and account management endpoints."""
from __future__ import annotations

class UserModule:
    def __init__(self, client):
        self._client = client

    def profile_self(self) -> dict:
        """Fetch current authenticated user profile details."""
        return self._client._get("/api/v1/accounts/current_user/?edit=true")

    def info(self, user_id: str | int) -> dict:
        """Fetch public profile metadata for a target user ID."""
        return self._client._get(f"/api/v1/users/{user_id}/info/")

    def info_by_username(self, username: str) -> dict:
        """Look up user profile by handle."""
        return self._client._get(f"/api/v1/users/{username}/usernameinfo/")

    def set_biography(self, biography: str, external_url: str | None = None) -> dict:
        """Update account bio and profile website link."""
        data = {"raw_text": biography}
        if external_url:
            data["external_url"] = external_url
        return self._client._post("/api/v1/accounts/set_biography/", data=data)

    def change_profile_picture(self, photo_path_or_bytes) -> dict:
        """Upload a JPEG photo and set it as the account profile picture."""
        upload_id = self._client._rupload_photo(photo_path_or_bytes)
        return self._client._post(
            "/api/v1/accounts/change_profile_picture/",
            data={"use_fbuploader": "true", "upload_id": upload_id},
        )

    def remove_profile_picture(self) -> dict:
        """Remove current profile picture."""
        return self._client._post("/api/v1/accounts/remove_profile_picture/", data={})
