# instagram-private-api

[![Release](https://img.shields.io/badge/Release-v2.0.0-2563eb.svg)](https://github.com/molkex/instagram-private-api/releases)
[![CI](https://github.com/molkex/instagram-private-api/actions/workflows/ci.yml/badge.svg)](https://github.com/molkex/instagram-private-api/actions)
[![Architecture: Pure HTTP/2 Zero-Device](https://img.shields.io/badge/Architecture-Pure--HTTP%2F2%20Zero--Device-0f172a.svg)](#)
[![Transport: Mobile TLS 1.3 BoringSSL](https://img.shields.io/badge/Transport-Mobile%20TLS%201.3%20BoringSSL-10b981.svg)](#)
[![Python: >=3.10](https://img.shields.io/badge/Python->=3.10-3776ab.svg)](#)
[![TypeScript / Node.js](https://img.shields.io/badge/TypeScript%20%2F%20Node.js-v2.0.0-3178c6.svg)](#)
[![Telegram Contact](https://img.shields.io/badge/Telegram-@mxmtkchk-229ED9.svg)](https://t.me/mxmtkchk)

**Unofficial Instagram & Threads mobile API SDK for Python & TypeScript / Node.js.** Talks to the same private
endpoints the real Android/iOS app uses — feed, profiles, direct messages, media/reels upload,
friendships, warmup exploration loops, and Threads keyword search/replies — with full request
signing (X-IG-Capabilities, X-IG-App-ID, Pigeon/Scribe telemetry, JA4 TLS 1.3 BoringSSL).
**No Meta for Developers account, no OAuth, no app review, no 24-hour messaging window.** You drive
a real logged-in session, not the throttled official API.

> This is a reverse-engineering / automation toolkit. Use it on accounts and
> data you are authorized to access.

---

## Why this instead of the official API

| | Official Meta Graph API | **instagram-private-api** |
|---|---|---|
| Developer account / app review | required | **not needed** |
| Access token permissions | scoped, strict review | **full mobile permissions** |
| Reading feed, explore, other users | ❌ not exposed | ✅ |
| Cold direct messaging & outreach | ❌ 24h window for approved pages | ✅ unlimited 1-on-1 & threads |
| Likes / comments / follows / blocks | ❌ | ✅ |
| Reels & Carousel publishing | restricted formats & web upload | ✅ native segmented chunked upload |
| Threads public search & replies | ❌ restricted (Tech Provider only) | ✅ sub-80ms real-time search & reply |
| Rate limits | tight, per-app | per-account, mobile-grade |

The official Content Publishing / Graph API only lets you touch *your own* business
connected account in a restricted sandbox. This SDK speaks the native mobile protocol,
so it does what the real mobile app does.

---

## Features

- **Full mobile signing & anti-fraud** — Authentic Android 14 (Pixel 8 Pro) and iOS 17 hardware presets, JA4 TLS 1.3 BoringSSL cipher suites, and companion Pigeon/Scribe telemetry batching.
- **Dual Platform (Instagram + Threads)** — Drive both Instagram and Threads (`com.instagram.barcelona`) using a single unified Meta session or API key.
- **60+ endpoints across 7 modules** — feed, user, direct, media/reels, friendship, warmup, and threads.
- **Reliable direct messaging** — 1-on-1 and group threads, typing indicators, read receipts, rich OpenGraph link preview cards, and media attachments.
- **Human-like Warmup engine** — Natural dwell intervals, feed scroll exploration, and story viewing routines to eliminate automated checkpoint flags.
- **Session-based auth & 2FA** — Encrypted password challenge, 2FA TOTP seed handling, and instant session serialization/recovery across proxy shifts.
- **Managed remote signer or local daemon** — Request signing runs on our managed infrastructure or local daemon. You get a clean API and never touch raw reverse-engineered crypto internals.

---

## Quick start

Request signing runs on our hosted service or high-throughput signing daemon — you just need an API key. No emulators, no Android ADB bridges, no local signing setup to maintain.

```python
from instagramflow import InstagramAPI, ThreadsAPI

# Initialize Instagram client
ig = InstagramAPI(api_key="ig_...")      # get a key — see "Get access" below

# Inspect account profile
me = ig.user.profile_self()
print(f"Logged in as @{me['username']} ({me['pk']})")

# Browse timeline feed
feed = ig.feed.timeline(count=12)

# Send direct message with rich link preview card
ig.direct.send_message(
    username="target_founder",
    text="Hey! Loved your recent breakdown on infrastructure.",
    link_preview="https://example.com/demo"
)

# Run an organic warmup exploration session
ig.warmup.run_session(feed_scrolls=10, story_views=5)
```

### Threads Integration (Sub-80ms Ingestion & Replies)

```python
# Threads client uses the same Meta session or API key
threads = ThreadsAPI(api_key="ig_...")

# Search real-time discussions for keywords
results = threads.search("ai agents", limit=15)
for post in results.posts:
    print(f"[{post.author}] ({post.like_count} likes): {post.text[:80]}...")

# Reply directly to any external thread post
threads.reply(
    parent_post_id="3141592653589793238",
    text="Great perspective! Native HTTP/2 makes a huge difference."
)
```

### TypeScript / Node.js Quick Start (Modern Dilame Alternative)

Looking for a maintained, production-grade TypeScript / Node.js alternative to `dilame/instagram-private-api`? While Dilame's public library was frozen in early 2024, our SDK provides first-class TypeScript bindings with authentic iOS 17 / Android 14 JA4 TLS 1.3 fingerprints:

```typescript
import { InstagramAPI, ThreadsAPI } from "@molkex/instagram-private-api";

// Initialize client with iPhone 15 Pro hardware preset
const ig = new InstagramAPI({
  apiKey: "ig_...",
  devicePreset: "iphone_15_pro"
});

// Watch active story with paired timestamp beacons
await ig.story.seen("3141592653589793238_12345");

// Send DM with reaction and link preview card
await ig.direct.sendMessage({
  username: "target_founder",
  text: "Loved your latest breakdown on infrastructure!",
  linkPreview: "https://example.com/demo"
});

// Fast Threads keyword search (<80ms)
const threads = new ThreadsAPI({ apiKey: "ig_..." });
const { posts } = await threads.search("ai agents", 10);
for (const p of posts) {
  console.log(`[${p.author}] (${p.like_count} likes): ${p.text.slice(0, 60)}...`);
}
```

---

## AI Agents & Model Context Protocol (MCP)

This SDK is **Agent-Ready** and ships with native MCP server support for autonomous AI workflows (Claude Desktop, Cursor, Windsurf, Devin):

```bash
# Launch the MCP server via stdio
python -m instagramflow.mcp_server
```

Claude Desktop / Cursor config (`mcp.json`):
```json
{
  "mcpServers": {
    "instagram": {
      "command": "python3",
      "args": ["-m", "instagramflow.mcp_server"],
      "env": {
        "INSTAGRAM_API_KEY": "ig_live_key"
      }
    }
  }
}
```

Available agent tools:
- `instagram_send_direct_message(username, text, link_preview)`
- `instagram_run_warmup(feed_scrolls, story_views)`
- `threads_search_posts(query, limit)`
- `threads_reply_post(parent_post_id, text)`

See [`AGENT_GUIDE.md`](AGENT_GUIDE.md) and [`llms.txt`](llms.txt) for detailed agent prompting specifications.

---

## Documentation & Specifications

Comprehensive deep-dives into mobile protocols, fingerprinting, and session management:

- **[Architecture & Anti-Fraud Engine](docs/ARCHITECTURE.md)** — JA4 TLS 1.3 BoringSSL vs OpenSSL, HTTP/2 pseudo-header sequencing, `signed_body` HMAC-SHA256, and Pigeon/Scribe telemetry.
- **[Free Tier vs Commercial Licensing](docs/LICENSING_AND_LIMITS.md)** — Capabilities matrix, why write actions require signing, and enterprise daemon licensing.
- **[Sessions, Proxies & Best Practices](docs/SESSIONS_AND_PROXIES.md)** — Cookie serialization, residential 4G/5G mobile proxies, and avoiding checkpoint flags.
- **[AI Agents & MCP Guide](AGENT_GUIDE.md)** — Model Context Protocol (MCP) server setup for Claude Desktop, Cursor, and autonomous agents.
- **[Machine-Readable Manifest](llms.txt)** — Index specification for LLM crawlers.

---

## Endpoint modules


| Module | What it covers |
|---|---|
| `user` | profile self, user info by username/id, bio/avatar update, privacy toggles, external links |
| `feed` | timeline feed, user feed, explore grid, saved items, location tags, hashtag feed |
| `direct` | inbox threads, pending requests, send text, typing cadence, link previews, reactions, media |
| `media` | Reels tab (`user_clips`), shortcode conversion, metadata info, bookmark saves/collections, archive, delete |
| `comment` | comment lists, child replies thread, post comment, reply to comment, like/unlike, pin/unpin |
| `story` | active stories tray, timestamped seen beacons, story like/unlike, emoji reactions, direct replies, highlights |
| `note` | 24-hour direct status notes, mutual/close friends audience, create and delete |
| `friendship` | follow, unfollow, block, mute, follower/following pagination, relationship status |
| `warmup` | organic feed scrolling, randomized dwell delays, story viewing, human-like pacing |
| `threads` | real-time keyword search, nested discussion trees, thread replies, likes, reposts, quotes |

---

## Install
 
### Python
```bash
pip install instagram-private-api
```

### TypeScript / Node.js
```bash
npm install @molkex/instagram-private-api
```

---

## How it works

Mobile request signing (`X-IG-Capabilities`, `X-IG-App-ID`, signed body payload encryption, and JA4 TLS 1.3 BoringSSL handshake replication) is the critical layer that breaks in legacy scrapers.

We run this as a managed network service or standalone private daemon: your Python code dispatches high-level actions, our signing engine applies cryptographically valid headers and anti-fraud telemetry beacons, and Instagram / Threads accepts the traffic as authentic mobile app requests.

---

## Comparison with Browser Automation

| Metric | Headless Browser (Playwright / Puppeteer) | instagram-private-api SDK |
|---|---|---|
| **RAM per 100 Accounts** | 25 - 40 GB | **< 280 MB** |
| **CPU Overhead** | High (Chromium WebKit rendering) | **Near Zero (Pure HTTP/2)** |
| **TLS Fingerprint** | Desktop Chrome/Safari mismatch | **Authentic Android 14 JA4 TLS 1.3** |
| **Ban Longevity** | High risk (Heuristic DOM traps) | **Enterprise Longevity (Mobile Match)** |
| **Threads Search Latency** | 3,000 - 7,000 ms | **35 - 80 ms** |

---

## Frequently Asked Questions (FAQ)

### Why switch from Instagrapi or legacy HTTP/1.1 libraries?
Legacy libraries like Instagrapi rely on outdated mobile app endpoints and generic Python OpenSSL TLS handshakes. Meta's anti-fraud system instantly detects generic cipher ordering, resulting in immediate `challenge_required` or account suspension. Our SDK connects via authentic Android 14 (Pixel 8 Pro) and iOS 17 JA4 TLS 1.3 BoringSSL fingerprints and automatically dispatches native Pigeon/Scribe analytics batches alongside write requests.

### Can I search and reply to Threads discussions without Meta App Review?
Yes. The official Meta Graph API (`graph.threads.net`) strictly prohibits replying to external threads and requires verified Tech Provider status for search. This SDK connects via native mobile Barcelona endpoints (`x-ig-app-id: 3419628305025917`), enabling wire-speed sub-80ms keyword discovery and direct replies to any public discussion thread.

### What server resources are required to scale to 100+ accounts?
Under 280 MB of RAM. Unlike browser automation tools (Selenium, Playwright, Puppeteer) that demand 20–40 GB of RAM and dedicated GPUs for 100 accounts, our pure HTTP/2 zero-device architecture runs hundreds of concurrent accounts smoothly on a standard $10/month cloud VPS.

### How does the Warmup engine eliminate checkpoint flags?
The built-in warmup pipeline executes human-like algorithmic exploration: variable dwell times on posts, randomized story view sessions, and progressive action pacing that mimics authentic human touch input, preserving high trust scores for aged and newly registered accounts.

### Can I deploy the signing daemon on my own private infrastructure?
Yes. We offer standalone self-hosted signing daemon packages for high-throughput enterprise platforms and agency clusters who require zero third-party data transmission.

---

## Get access

API keys, private signing daemon deployment, pricing plans, and custom high-volume setups:
**[@mxmtkchk](https://t.me/mxmtkchk)** on Telegram.

---

## Disclaimer

Not affiliated with, authorized, or endorsed by Instagram, Threads, or Meta Platforms, Inc. Provided for educational, research, and automation purposes on authorized accounts. You are responsible for complying with Meta's terms of service and applicable local laws.

