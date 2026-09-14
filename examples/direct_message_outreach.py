"""
Example: Cold direct messaging pipeline with rich link preview card and typing indicators.
"""
from instagramflow import InstagramAPI

def run_outreach():
    ig = InstagramAPI(
        api_key="ig_live_key",
        device_preset="pixel_8_pro",
        proxy="http://user:pass@mobile-node.de:8888"
    )

    targets = [
        {"username": "growth_lead_1", "name": "Alex"},
        {"username": "growth_lead_2", "name": "Elena"},
    ]

    for lead in targets:
        print(f"Preparing direct message for @{lead['username']}...")
        # Dispatch 1-on-1 message with companion typing simulation
        res = ig.direct.send_message(
            username=lead["username"],
            text=f"Hi {lead['name']}, checked out your latest project. Would love to share our benchmark data.",
            link_preview="https://github.com/molkex/instagram-private-api"
        )
        print(f"Message sent to @{lead['username']} with status: {res.get('status', 'ok')}")

    # 1. Send conversation heart like
    ig.direct.send_like(thread_id="340282366841710300949128130000000000001")

    # 2. React with custom emoji (🔥, ❤️, 😂, 👏) to target message
    ig.direct.send_reaction(
        thread_id="340282366841710300949128130000000000001",
        item_id="3141592653589793238",
        emoji_code="🔥"
    )

    # 3. Quoted reply to specific message
    ig.direct.reply_to_message(
        thread_id="340282366841710300949128130000000000001",
        item_id="3141592653589793238",
        text="Totally agree with this point!"
    )

    # 4. Reply directly to an active Story
    ig.direct.reply_to_story(
        reel_id="3182938491029384910",
        text="Great insights in your story!",
        recipient_id="17841400000000001"
    )

if __name__ == "__main__":
    run_outreach()
