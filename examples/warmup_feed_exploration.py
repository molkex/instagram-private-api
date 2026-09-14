"""
Example: Automated humanized warmup session with feed scrolls and story viewing.
"""
from instagramflow import InstagramAPI

def run_warmup():
    ig = InstagramAPI(
        api_key="ig_live_key",
        device_preset="pixel_8_pro"
    )

    print("Initiating organic account warmup sequence...")
    # Simulates genuine user exploration: feed dwell times, story views, and companion beacons
    report = ig.warmup.run_session(
        feed_scrolls=12,
        story_views=6,
        dwell_delay_range=(2.0, 5.5)
    )

    print(f"Warmup status: {report['status']}")
    print(f"Completed {report['feed_scrolls']} scrolls and {report['story_views']} story views.")
    for action in report["actions"][:5]:
        print(f"  -> {action}")

if __name__ == "__main__":
    run_warmup()
