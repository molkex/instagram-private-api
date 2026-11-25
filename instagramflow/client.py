"""Main InstagramAPI client class."""
from __future__ import annotations

import httpx
try:
    from curl_cffi.requests import Session as _CurlSession
except ImportError:  # pragma: no cover - fallback when curl_cffi is not installed
    _CurlSession = None
from .remote_signer import DEFAULT_SIGN_URL, RemoteSigner
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
        signing_server: str = DEFAULT_SIGN_URL,
        device_preset: str = "pixel_8_pro",
        proxy: str | None = None,
        rate_limit: float | None = None,
        timeout: float = 15.0,
    ):
        self.api_key = api_key
        self.session_token = session_token
        self.device_preset = device_preset
        self.signer = RemoteSigner(signing_server, api_key, device_preset=device_preset)

        if _CurlSession is not None:
            curl_kwargs = {"impersonate": "chrome", "timeout": timeout}
            if proxy:
                curl_kwargs["proxies"] = {"http": proxy, "https": proxy}
            self._http = _CurlSession(**curl_kwargs)
        else:
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

    def _rupload_photo(self, photo_path_or_bytes) -> str:
        """Upload raw JPEG bytes to rupload_igphoto and return upload_id."""
        import json as _json
        import random as _random
        import time as _time
        import uuid as _uuid
        from pathlib import Path

        data = Path(photo_path_or_bytes).read_bytes() if isinstance(photo_path_or_bytes, (str, Path)) else photo_path_or_bytes
        upload_id = str(int(_time.time() * 1000))
        name = f"{upload_id}_0_{_random.randint(1000000000, 9999999999)}"
        path = f"/rupload_igphoto/{name}"
        signed = self.signer.sign_request(endpoint=path, method="POST", platform="instagram")
        headers = signed.get("headers", {})
        if self.session_token:
            headers["Authorization"] = f"Bearer {self.session_token}"
        headers.update({
            "X-Instagram-Rupload-Params": _json.dumps({
                "upload_id": upload_id,
                "media_type": "1",
                "retry_context": _json.dumps({"num_step_auto_retry": 0, "num_reupload": 0, "num_step_manual_retry": 0}),
                "image_compression": _json.dumps({"lib_name": "moz", "lib_version": "3.1.m", "quality": "80"}),
                "xsharing_user_ids": "[]",
            }),
            "X-Entity-Type": "image/jpeg",
            "X-Entity-Name": name,
            "X-Entity-Length": str(len(data)),
            "X_FB_PHOTO_WATERFALL_ID": str(_uuid.uuid4()),
            "Offset": "0",
            "Content-Type": "application/octet-stream",
        })
        kw = {"content": data} if isinstance(self._http, httpx.Client) else {"data": data}
        resp = self._http.post(f"{self.BASE_URL}{path}", headers=headers, **kw)
        self._handle_response(resp)
        return upload_id

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
