#!/usr/bin/env python3
"""
Example: Watch active stories and send emoji reactions / views with human-like dwell times.
"""
import os
import time
import random
from instagramflow import InstagramAPI

API_KEY = os.getenv("INSTAGRAM_API_KEY", "your_api_key_here")
SESSION_TOKEN = os.getenv("INSTAGRAM_SESSION_TOKEN", "your_session_token")

def run_story_engagement():
    ig = InstagramAPI(
        api_key=API_KEY,
        session_token=SESSION_TOKEN,
        device_preset="iphone_15_pro",
    )

    target_usernames = ["tech_founder", "ai_researcher", "growth_lead"]

    for username in target_usernames:
        user_info = ig.user.info_by_username(username)
        user_id = user_info.get("user", {}).get("pk")
        if not user_id:
            continue

        print(f"Checking stories for @{username} (ID: {user_id})...")
        stories_tray = ig.story.user_stories(user_id)
        items = stories_tray.get("reels", {}).get(str(user_id), {}).get("items", [])

        if not items:
            print(f"No active stories for @{username}")
            continue

        for story in items:
            story_id = story.get("id")
            taken_at = story.get("taken_at")

            # Human-like viewing dwell time (2.5 to 5.0 seconds)
            view_time = random.uniform(2.5, 5.0)
            time.sleep(view_time)

            # Send authentic view beacon
            ig.story.seen(story_id, taken_at=taken_at)
            print(f"Watched story {story_id} ({view_time:.1f}s)")

            # Optionally like the story or react
            if random.random() < 0.4:
                ig.story.like(story_id)
                print(f"Liked story {story_id}")

            time.sleep(random.uniform(1.0, 2.5))

    ig.close()

if __name__ == "__main__":
    run_story_engagement()
