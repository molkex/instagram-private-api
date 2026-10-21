# Status — what works

Honest capability matrix for **instagram-private-api** (Instagram + Threads).
Updated 2026-10-21.

**Legend**
- ✅ **Headless** — works over pure HTTP with just a session, no phone, no emulator.
- 🟡 **Caveat** — works, but with the limits noted.
- ⚠️ **Fragile** — possible, but survival depends on your setup.

> The honest boundary: **the limit is fresh-account survival (anti-abuse), not
> the operations.** On an existing account you only need a valid session — and
> both reads *and* writes (follow, like, comment, post, DM) go through headless
> and persist. There is no device requirement for operating an account you
> already have.

## Reads — ✅ headless (session)

| Area | Methods | Status |
|---|---|---|
| Feed | timeline, user feed, reels, hashtag | ✅ |
| User | profile, info, followers, following, search | ✅ |
| Media | detail, comments (read), insights | ✅ |
| Direct | inbox, thread, messages (read) | ✅ |
| Threads | profile, keyword search, replies (read) | ✅ |

## Writes — ✅ headless on an existing session

| Action | Status | Note |
|---|---|---|
| Follow / Unfollow | ✅ | persists (verified via independent mobile proxy) |
| Like / Comment | ✅ | on your session |
| Post / media & reels upload | ✅ | |
| Direct message (1-on-1 & threads) | ✅ | send, typing, read receipts |
| Threads reply | ✅ | |

Unlike device-bound stacks, Instagram operations on a logged-in account do not
need a real device — a valid `sessionid` / `Authorization: Bearer` is enough and
the writes stick.

## Account lifecycle

| Action | Status | Note |
|---|---|---|
| Login (existing account) | ✅ | your credentials; mints a session |
| Session reuse | ✅ | cookies / Bearer from a prior login |
| Register a new account | ⚠️ | the flow completes pure-HTTP, but fresh accounts frequently hit anti-abuse **suspension** (`challenge_required`) on datacenter IPs or disposable email |

**The real wall is new-account survival.** Registration is not blocked by signing
or attestation — it is blocked by anti-abuse. Residential/mobile proxies and a
real inbox improve survival; even then, suspensions on brand-new accounts are
common. Operating *existing* accounts (reads, writes, DMs) is the reliable path.

## Platforms & transport

| | Status |
|---|---|
| Android device fingerprint (Pixel-class) | ✅ |
| iOS device fingerprint | ✅ |
| Dual platform (Instagram + Threads, one session) | ✅ |
| Managed remote signer or local daemon | ✅ (API key) |
| Proxy support (residential/mobile recommended for writes & reg) | ✅ |

---

**Access:** free key via [@ig_private_api_bot](https://t.me/ig_private_api_bot)
(`/key`) · contact [@mxmtkchk](https://t.me/mxmtkchk).

*Not affiliated with Instagram, Threads or Meta. Use responsibly.*
