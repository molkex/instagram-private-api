"""Quickstart: Instagram mobile automation using instagramflow.

Requires:
    IG_API_KEY       — free key from @ig_private_api_bot (/key)
    IG_SESSION_TOKEN — your logged-in Instagram mobile session token (IGT:2:...)

Optional:
    SIGN_URL         — remote signer URL (defaults to https://sign.54-38-243-162.nip.io)
    IG_PROXY         — sticky residential/4G proxy URL (e.g. http://user:pass@host:port)
    IG_TARGET_USER   — username to send a test DM to (skipped if unset)
"""
import os
import sys

from instagramflow import InstagramAPI


def main() -> None:
    api_key = os.environ.get("IG_API_KEY", "").strip()
    session_token = os.environ.get("IG_SESSION_TOKEN", "").strip()
    if not api_key or not session_token:
        print("Set IG_API_KEY (from @ig_private_api_bot /key) and IG_SESSION_TOKEN (IGT:2:...) first.")
        sys.exit(1)

    with InstagramAPI(
        api_key=api_key,
        session_token=session_token,
        signing_server=os.environ.get("SIGN_URL", "https://sign.54-38-243-162.nip.io"),
        device_preset="pixel_8_pro",
        proxy=os.environ.get("IG_PROXY") or None,
    ) as ig:
        me = ig.user.profile_self()
        print("Profile self:", me)

        feed = ig.feed.timeline(count=5)
        print("Timeline items:", len(feed.get("feed_items", [])))

        target = os.environ.get("IG_TARGET_USER", "").strip()
        if target:
            dm = ig.direct.send_message(username=target, text="Hello from instagramflow!")
            print("DM result:", dm)


if __name__ == "__main__":
    main()
