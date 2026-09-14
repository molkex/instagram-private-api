"""Media upload, Reels publishing, post interaction, bookmark, and media download endpoints."""
from __future__ import annotations
import os
import httpx

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"

class MediaModule:
    """Operations on feed media, reels, and video clips."""

    def __init__(self, client):
        self._client = client

    @staticmethod
    def pk_from_code(code: str) -> int:
        """Convert Instagram shortcode (e.g. 'CGgDsi7JQdS') to numeric media ID."""
        pk = 0
        for ch in code:
            pk = pk * 64 + _ALPHABET.index(ch)
        return pk

    @staticmethod
    def code_from_pk(pk: int | str) -> str:
        """Convert numeric media ID to Instagram shortcode."""
        pk = int(pk)
        out = ""
        while pk:
            pk, rem = divmod(pk, 64)
            out = _ALPHABET[rem] + out
        return out or "A"

    def info(self, media_id: str | int) -> dict:
        """Retrieve complete metadata and telemetry details for a media item."""
        return self._client._get(f"/api/v1/media/{media_id}/info/")

    def likers(self, media_id: str | int) -> dict:
        """Fetch list of accounts that liked this media item."""
        return self._client._get(f"/api/v1/media/{media_id}/likers/")

    def user_clips(self, user_id: str | int, max_id: str | None = None) -> dict:
        """Retrieve user's dedicated Reels/Clips tab."""
        data = {"target_user_id": str(user_id), "page_size": "12"}
        if max_id:
            data["max_id"] = max_id
        return self._client._post("/api/v1/clips/user/", data=data)

    def like(self, media_id: str | int) -> dict:
        """Like a media item with companion telemetry."""
        return self._client._post(f"/api/v1/media/{media_id}/like/")

    def unlike(self, media_id: str | int) -> dict:
        """Unlike a media item."""
        return self._client._post(f"/api/v1/media/{media_id}/unlike/")

    def save(self, media_id: str | int, collection_id: str | None = None) -> dict:
        """Save media post or Reel to saved bookmarks / collection."""
        data = {}
        if collection_id:
            data["added_collection_ids"] = f"[{collection_id}]"
        return self._client._post(f"/api/v1/media/{media_id}/save/", data=data or None)

    def unsave(self, media_id: str | int) -> dict:
        """Remove media item from saved bookmarks."""
        return self._client._post(f"/api/v1/media/{media_id}/unsave/")

    def comment(self, media_id: str | int, text: str) -> dict:
        """Post a comment on a media item."""
        data = {"comment_text": text}
        return self._client._post(f"/api/v1/media/{media_id}/comment/", data=data)

    def download(self, media_id_or_code: str | int, output_path: str | None = None) -> dict:
        """
        Download photo, carousel item, or Reel in highest available CDN resolution.
        Accepts numeric media ID or shortcode URL segment (e.g. 'CGgDsi7JQdS').
        """
        if isinstance(media_id_or_code, str) and not media_id_or_code.isdigit():
            clean_code = media_id_or_code.rstrip("/").split("/")[-1]
            media_id = self.pk_from_code(clean_code)
        else:
            media_id = int(media_id_or_code)

        info = self.info(media_id)
        items = info.get("items", [])
        if not items:
            return {"error": "Media item not found or unavailable"}

        item = items[0]
        media_type = item.get("media_type", 1)  # 1 = photo, 2 = video, 8 = carousel

        cdn_url = None
        ext = "jpg"
        if media_type == 2 or "video_versions" in item:
            video_versions = item.get("video_versions", [])
            if video_versions:
                cdn_url = video_versions[0].get("url")
                ext = "mp4"

        if not cdn_url:
            image_candidates = item.get("image_versions2", {}).get("candidates", [])
            if image_candidates:
                cdn_url = image_candidates[0].get("url")
                ext = "jpg"

        if not cdn_url:
            return {"error": "No media CDN stream available"}

        result = {
            "media_id": str(media_id),
            "media_type": "video" if ext == "mp4" else "photo",
            "url": cdn_url,
            "ext": ext,
        }

        if output_path:
            target_path = output_path
            if os.path.isdir(target_path):
                target_path = os.path.join(target_path, f"{media_id}.{ext}")
            resp = httpx.get(cdn_url, timeout=30.0)
            if resp.status_code == 200:
                with open(target_path, "wb") as f:
                    f.write(resp.content)
                result["output_path"] = target_path
                result["bytes_downloaded"] = len(resp.content)

        return result

    def delete(self, media_id: str | int, media_type: str = "PHOTO") -> dict:
        """Delete an owned media post or clip."""
        data = {"media_id": str(media_id), "media_type": media_type}
        return self._client._post(f"/api/v1/media/{media_id}/delete/", data=data)

    def edit(self, media_id: str | int, caption: str) -> dict:
        """Update caption of an existing media item."""
        data = {"caption_text": caption}
        return self._client._post(f"/api/v1/media/{media_id}/edit_media/", data=data)

    def archive(self, media_id: str | int) -> dict:
        """Archive a media post (hide from profile)."""
        data = {"media_id": str(media_id)}
        return self._client._post(f"/api/v1/media/{media_id}/only_me/", data=data)

    def unarchive(self, media_id: str | int) -> dict:
        """Restore an archived media post back to profile."""
        data = {"media_id": str(media_id)}
        return self._client._post(f"/api/v1/media/{media_id}/undo_only_me/", data=data)

    def configure_timeline_photo(self, upload_id: str, caption: str = "") -> dict:
        """Publish uploaded photo to timeline."""
        data = {
            "upload_id": upload_id,
            "caption": caption,
            "source_type": "4",
        }
        return self._client._post("/api/v1/media/configure/", data=data)
