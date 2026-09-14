"""Direct messaging and inbox management endpoints."""
from __future__ import annotations
import uuid
import time

class DirectModule:
    def __init__(self, client):
        self._client = client

    def inbox(self, limit: int = 20) -> dict:
        """Fetch primary direct message threads."""
        return self._client._get("/api/v1/direct_v2/inbox/", params={"limit": limit})

    def send_message(
        self,
        username: str | None = None,
        recipient_id: str | int | None = None,
        thread_id: str | None = None,
        text: str = "",
        link_preview: str | None = None,
    ) -> dict:
        """Dispatch a 1-on-1 direct message with optional rich link preview card."""
        client_context = str(uuid.uuid4())
        data = {
            "text": text,
            "client_context": client_context,
            "action": "send_item",
        }
        if link_preview:
            data["link_text"] = text
            data["link_urls"] = [link_preview]
        if thread_id:
            data["thread_id"] = thread_id
            return self._client._post("/api/v1/direct_v2/threads/broadcast/text/", data=data)
        elif recipient_id:
            data["recipient_users"] = f"[[{recipient_id}]]"
            return self._client._post("/api/v1/direct_v2/threads/broadcast/text/", data=data)
        elif username:
            data["recipient_users"] = f"[[{username}]]"
            return self._client._post("/api/v1/direct_v2/threads/broadcast/text/", data=data)
        raise ValueError("Must supply recipient_id, username, or thread_id")

    def mark_seen(self, thread_id: str, item_id: str) -> dict:
        """Simulate read receipt for a direct message thread item."""
        return self._client._post(f"/api/v1/direct_v2/threads/{thread_id}/items/{item_id}/seen/")

    def send_like(self, thread_id: str) -> dict:
        """Send quick heart like to a conversation thread."""
        return self._client._post("/api/v1/direct_v2/threads/broadcast/like/", data={"thread_ids": f"[{thread_id}]", "action": "send_item"})

    def send_reaction(self, thread_id: str, item_id: str, emoji_code: str = "like") -> dict:
        """Send emoji reaction (like, ❤️, 😂, 🔥, 😮, 👏) to a specific message item."""
        data = {
            "thread_ids": f"[{thread_id}]",
            "item_id": item_id,
            "reaction_type": emoji_code,
            "action": "send_item",
        }
        return self._client._post("/api/v1/direct_v2/threads/broadcast/reaction/", data=data)

    def delete_reaction(self, thread_id: str, item_id: str) -> dict:
        """Remove an emoji reaction from a message item."""
        data = {
            "thread_ids": f"[{thread_id}]",
            "item_id": item_id,
            "action": "send_item",
        }
        return self._client._post("/api/v1/direct_v2/threads/broadcast/delete_reaction/", data=data)

    def reply_to_message(self, thread_id: str, item_id: str, text: str) -> dict:
        """Reply directly to a specific message in thread (quoted reply)."""
        data = {
            "thread_ids": f"[{thread_id}]",
            "replied_to_item_id": item_id,
            "text": text,
            "action": "send_item",
        }
        return self._client._post("/api/v1/direct_v2/threads/broadcast/text/", data=data)

    def reply_to_story(self, reel_id: str, text: str, recipient_id: str) -> dict:
        """Send a Direct Message reply to an active Story."""
        data = {
            "recipient_users": f"[[{recipient_id}]]",
            "reel_id": reel_id,
            "text": text,
            "action": "send_item",
        }
        return self._client._post("/api/v1/direct_v2/threads/broadcast/reel_share/", data=data)

    def react_to_story(self, reel_id: str, emoji_code: str, recipient_id: str) -> dict:
        """Send an emoji reaction to an active Story via Direct."""
        data = {
            "recipient_users": f"[[{recipient_id}]]",
            "reel_id": reel_id,
            "reaction_name": emoji_code,
            "action": "send_item",
        }
        return self._client._post("/api/v1/direct_v2/threads/broadcast/reel_reaction/", data=data)

    def delete_message(self, thread_id: str, item_id: str) -> dict:
        """Unsend / delete a previously sent direct message."""
        return self._client._post(f"/api/v1/direct_v2/threads/{thread_id}/items/{item_id}/delete/")
