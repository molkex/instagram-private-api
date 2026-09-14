#!/usr/bin/env python3
"""
Example: Scrape comments and engaged leads from viral Reels or posts.
"""
import os
import json
from instagramflow import InstagramAPI

API_KEY = os.getenv("INSTAGRAM_API_KEY", "your_api_key_here")
SESSION_TOKEN = os.getenv("INSTAGRAM_SESSION_TOKEN", "your_session_token")

def scrape_leads_from_post(media_url_or_code: str):
    ig = InstagramAPI(
        api_key=API_KEY,
        session_token=SESSION_TOKEN,
        device_preset="pixel_8_pro",
    )

    # Convert shortcode to numeric ID if needed
    if "/" in media_url_or_code:
        code = media_url_or_code.rstrip("/").split("/")[-1]
    else:
        code = media_url_or_code

    media_pk = ig.media.pk_from_code(code)
    print(f"Fetching metadata for media PK: {media_pk} (code: {code})...")

    # Fetch post info
    info = ig.media.info(media_pk)
    caption = info.get("items", [{}])[0].get("caption", {}).get("text", "")
    print(f"Caption: {caption[:60]}...")

    # Fetch top comments
    comments_resp = ig.comment.list(media_pk)
    comments = comments_resp.get("comments", [])

    leads = []
    for c in comments:
        user = c.get("user", {})
        leads.append({
            "username": user.get("username"),
            "full_name": user.get("full_name"),
            "comment": c.get("text"),
            "like_count": c.get("comment_like_count", 0),
        })

    print(f"Extracted {len(leads)} comments/leads:")
    print(json.dumps(leads[:5], indent=2))

    ig.close()

if __name__ == "__main__":
    scrape_leads_from_post("CGgDsi7JQdS")
