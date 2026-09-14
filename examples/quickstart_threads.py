"""Quickstart: Threads real-time search & reply using instagramflow."""
from instagramflow import ThreadsAPI

def main():
    # Initialize Threads client
    threads = ThreadsAPI(api_key="ig_demo_key")

    # Real-time search
    print("Searching Threads for 'social automation'...")
    results = threads.search("social automation", limit=5)
    for post in results.posts:
        print(f"[{post.author}] ({post.like_count} likes): {post.text}")

    # Reply
    print("Replying to target thread...")
    reply_res = threads.reply(parent_post_id="3141592653589793238", text="Native HTTP/2 protocol engine.")
    print(f"Reply dispatched: {reply_res['reply_id']}")

if __name__ == "__main__":
    main()
