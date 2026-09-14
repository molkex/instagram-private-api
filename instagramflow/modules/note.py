"""Direct-tray 24-hour status notes endpoints."""
from __future__ import annotations

class NoteModule:
    """Operations on Instagram Notes appearing in Direct tray."""

    def __init__(self, client):
        self._client = client

    def get_notes(self) -> dict:
        """Fetch active notes published by followed contacts."""
        return self._client._get("/api/v1/notes/get_notes/")

    def create(self, text: str, audience: int = 0) -> dict:
        """
        Publish a 24-hour status note.
        audience: 0 = mutual followers (standard), 1 = close friends.
        """
        data = {
            "text": text,
            "audience": str(audience),
        }
        return self._client._post("/api/v1/notes/create_note/", data=data)

    def delete(self, note_id: str | int) -> dict:
        """Delete an active status note."""
        data = {"id": str(note_id)}
        return self._client._post("/api/v1/notes/delete_note/", data=data)
