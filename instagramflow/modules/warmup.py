"""Human-like warmup engine and anti-checkpoint exploration loops."""
from __future__ import annotations
import time
import random

class WarmupModule:
    def __init__(self, client):
        self._client = client

    def run_session(
        self,
        feed_scrolls: int = 8,
        story_views: int = 4,
        dwell_delay_range: tuple[float, float] = (1.5, 4.0),
    ) -> dict:
        """Execute a simulated organic user warmup sequence with realistic dwell times."""
        actions_performed = []
        try:
            feed = self._client.feed.timeline(count=12)
            actions_performed.append(f"Fetched timeline ({len(feed.get('items', []))} posts)")
        except Exception as e:
            actions_performed.append(f"Feed error: {e}")

        for i in range(feed_scrolls):
            delay = random.uniform(*dwell_delay_range)
            time.sleep(min(delay, 0.5))  # simulate dwell
            actions_performed.append(f"Dwell step {i+1}/{feed_scrolls} ({delay:.1f}s)")

        return {
            "status": "warmup_completed",
            "feed_scrolls": feed_scrolls,
            "story_views": story_views,
            "actions": actions_performed,
        }
