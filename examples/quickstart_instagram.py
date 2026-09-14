"""Quickstart: Instagram mobile automation using instagramflow."""
from instagramflow import InstagramAPI

def main():
    # Initialize client with signing API key
    ig = InstagramAPI(
        api_key="ig_demo_key",
        device_preset="pixel_8_pro"
    )

    print("InstagramAPI initialized.")
    # Warmup cycle simulation
    warmup_res = ig.warmup.run_session(feed_scrolls=3, story_views=2)
    print(f"Warmup status: {warmup_res['status']}")

    # Direct message demo
    print("Ready to dispatch direct message...")

if __name__ == "__main__":
    main()
