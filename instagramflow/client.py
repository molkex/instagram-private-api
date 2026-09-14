"""Main InstagramAPI client class."""
from __future__ import annotations

import httpx
from .remote_signer import RemoteSigner
from .errors import InstagramError, AuthError, RateLimitError, ServerError
from .modules.user import UserModule
from .modules.feed import FeedModule
from .modules.direct import DirectModule
from .modules.media import MediaModule
from .modules.friendship import FriendshipModule
from .modules.warmup import WarmupModule
from .modules.comment import CommentModule
from .modules.story import StoryModule
from .modules.note import NoteModule

class InstagramAPI:
    """Headless Instagram Mobile Protocol Client."""

    BASE_URL = "https://i.instagram.com"

    def __init__(
        self,
        api_key: str,
        *,
        session_token: str | None = None,
        signing_server: str = "http://127.0.0.1:8643",
        device_preset: str = "pixel_8_pro",
        proxy: str | None = None,
        rate_limit: float | None = None,
        timeout: float = 15.0,
    ):
        self.api_key = api_key
        self.session_token = session_token
        self.device_preset = device_preset
        self.signer = RemoteSigner(signing_server, api_key, device_preset=device_preset)

        client_kwargs = {"timeout": timeout}
        if proxy:
            client_kwargs["proxy"] = proxy

        self._http = httpx.Client(**client_kwargs)

        # Initialize submodules
        self.user = UserModule(self)
        self.feed = FeedModule(self)
        self.direct = DirectModule(self)
        self.media = MediaModule(self)
        self.friendship = FriendshipModule(self)
        self.warmup = WarmupModule(self)
        self.comment = CommentModule(self)
        self.story = StoryModule(self)
        self.note = NoteModule(self)

    def _get(self, path: str, params: dict | None = None) -> dict:
        signed = self.signer.sign_request(endpoint=path, method="GET", platform="instagram")
        headers = signed.get("headers", {})
        if self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"

        resp = self._http.get(f"{self.BASE_URL}{path}", params=params, headers=headers)
        return self._handle_response(resp)

    def _post(self, path: str, data: dict | None = None) -> dict:
        signed = self.signer.sign_request(endpoint=path, method="POST", body=data, platform="instagram")
        headers = signed.get("headers", {})
        if self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"

        payload = signed.get("signed_body", data or {})
        resp = self._http.post(f"{self.BASE_URL}{path}", data=payload, headers=headers)
        return self._handle_response(resp)

    def _handle_response(self, resp: httpx.Response) -> dict:
        if resp.status_code == 429:
            raise RateLimitError("Rate limit encountered on Instagram mobile endpoint.")
        if resp.status_code == 401:
            raise AuthError("Instagram authentication failed or session expired.")
        try:
            return resp.json()
        except Exception:
            return {"status": "ok", "status_code": resp.status_code, "text": resp.text[:200]}

    def close(self):
        self._http.close()
        self.signer.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
