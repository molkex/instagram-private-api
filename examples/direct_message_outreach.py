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

if __name__ == "__main__":
    run_outreach()
