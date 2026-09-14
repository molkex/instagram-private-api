# Migrating from instagrapi to instagramflow (Python)

A migration guide for Python developers moving from `instagrapi` to `instagramflow`.

---

## Why Migrate from instagrapi?

While `instagrapi` was a popular Python solution, many production teams experience:
1. **Frequent Challenge / Login Loops**: Standard Python `requests` or `urllib3` does not support authentic mobile TLS 1.3 BoringSSL handshakes, causing Instagram to repeatedly challenge accounts.
2. **Heavyweight Local Reverse-Engineering Maintenance**: Changes to Meta's Bloks version IDs or signing algorithms break local scripts until upstream patches are released.
3. **Absence of Threads Support**: `instagrapi` does not support Threads (`com.instagram.barcelona`).
4. **Proxy Burn Rate**: Datacenter proxies get burned rapidly due to fingerprint mismatches.

`instagramflow` solves this with pure HTTP/2 zero-device architecture, JA4 TLS 1.3 signatures, built-in warmup loops, and full Threads support.

---

## Method Mapping Reference

| Operation | instagrapi Code | instagramflow Code |
|:---|:---|:---|
| **Initialize** | `cl = Client()` | `cl = InstagramAPI(api_key="...")` |
| **Login with Session** | `cl.load_settings("session.json")` | `session = InstagramSession.load_from_file("session.json"); cl = InstagramAPI(session=session)` |
| **Get User Profile** | `cl.user_info_by_username("user")` | `cl.user.info_by_username("user")` |
| **Timeline Feed** | `cl.get_timeline_feed()` | `cl.feed.timeline(count=15)` |
| **Send Direct Message** | `cl.direct_send("hello", [user_id])` | `cl.direct.send_message(username="user", text="hello")` |
| **Direct Message with Link** | Not supported cleanly | `cl.direct.send_message(username="user", text="check this", link_preview="https://...")` |
| **Story Reaction** | `cl.story_like(story_id)` | `cl.story.react(story_id=..., emoji="🔥", recipient_id=...)` |
| **Close Friends Add** | Not directly exposed | `cl.friendship.close_friend_add(user_id)` |
| **Organic Warmup** | Custom implementation | `cl.warmup.run_session(feed_scrolls=8, story_views=4)` |
| **Threads Search** | Not supported | `threads = ThreadsAPI(); threads.search_posts("topic")` |
| **Threads Reply** | Not supported | `threads.reply(parent_post_id=..., text="...")` |

---

## Session Format Compatibility

`instagramflow` can import existing sessions or use native JSON format:

```python
from instagramflow import InstagramAPI, InstagramSession

# Load session
session = InstagramSession.load_from_file("session.json")
ig = InstagramAPI(session=session)

# Check login status
me = ig.user.profile_self()
print("Authenticated as:", me["username"])
```

---

## Commercial Licensing & Inquiries
- Telegram: [@mxmtkchk](https://t.me/mxmtkchk)
