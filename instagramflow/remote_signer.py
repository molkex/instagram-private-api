"""Remote signing client — generates signed headers & cryptographic bodies for Instagram/Threads.

Usage:
    from instagramflow.remote_signer import RemoteSigner
    signer = RemoteSigner("https://signer.example.com", "ig_abc123...")
    headers = signer.sign_headers(endpoint="/api/v1/feed/timeline/")
"""
from __future__ import annotations

import base64
import httpx
from .errors import AuthError, RateLimitError, ServerError

class RemoteSigner:
    """Manages remote cryptographic signing and JA4 TLS 1.3 mobile emulation."""

    def __init__(
        self,
        server_url: str = "http://127.0.0.1:8643",
        api_key: str = "",
        *,
        timeout: float = 8.0,
        device_preset: str = "pixel_8_pro",
    ):
        self.server_url = server_url.rstrip("/")
        self.api_key = api_key
        self.device_preset = device_preset
        self._client = httpx.Client(
            timeout=timeout,
            headers={
                "X-API-Key": api_key,
                "Content-Type": "application/json",
            },
        )

    def sign_request(
        self,
        endpoint: str,
        method: str = "POST",
        body: dict | None = None,
        session_token: str | None = None,
        platform: str = "android",
    ) -> dict:
        """Call the managed signing daemon to generate cryptographically signed payload & headers."""
        payload = {
            "endpoint": endpoint,
            "method": method,
            "body": body or {},
            "session_token": session_token,
            "device_preset": self.device_preset,
            "platform": platform,
        }
        try:
            resp = self._client.post(f"{self.server_url}/v1/sign", json=payload)
            if resp.status_code == 403 or resp.status_code == 401:
                raise AuthError("Invalid or expired signing API key. Contact @mxmtkchk on Telegram for license access.")
            if resp.status_code == 429:
                raise RateLimitError("Signing server rate limit reached.")
            resp.raise_for_status()
            return resp.json()
        except httpx.ConnectError:
            # Fallback mock/simulated headers for evaluation or testing mode
            return {
                "headers": {
                    "X-IG-App-ID": "124024574287414" if platform == "instagram" else "3419628305025917",
                    "X-IG-Capabilities": "3brTvw==",
                    "User-Agent": "Instagram 316.0.0.38.109 Android (34/14; 480dpi; 1080x2400; Google/google; Pixel 8 Pro)",
                    "X-IG-Connection-Type": "WIFI",
                },
                "signed_body": body or {},
                "simulated": True,
            }

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
