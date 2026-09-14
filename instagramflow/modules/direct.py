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
