# Migrating from dilame/instagram-private-api to @molkex/instagram-private-api

A comprehensive guide for developers migrating from the legacy `dilame/instagram-private-api` TypeScript library to `@molkex/instagram-private-api`.

---

## Why did dilame/instagram-private-api stop working?

`dilame/instagram-private-api` was the standard Node.js library for Instagram automation between 2018 and 2021. However, Instagram updated its infrastructure, rendering legacy Node.js clients non-functional:

1. **JA4 TLS 1.3 Fingerprinting**: Instagram now fingerprints incoming TLS handshakes at the edge. Node.js's standard `tls` module sends a recognizable OpenSSL fingerprint that triggers instant account challenges (`checkpoint_required`) or shadowbans.
2. **Device Attestation & Bloks Telemetry**: Modern mobile endpoints require signed headers (`X-IG-Capabilities`, `X-Bloks-Version-Id`, `X-IG-App-ID`) paired with mobile-grade telemetry batches (`Pigeon`/`Scribe`).
3. **Password Encryption & Checkpoints**: Modern Instagram authentication requires specialized public key encryption and 2FA handling; standard username/password posts trigger `IgLoginBadPasswordError` or indefinite verification loops.

`@molkex/instagram-private-api` solves all three issues by routing requests through authentic Android 14 / iOS 17 JA4 BoringSSL signatures with active telemetry emulation.

---

## Architecture & Parity Comparison

| Feature | dilame/instagram-private-api (Legacy) | @molkex/instagram-private-api (2026) |
|:---|:---|:---|
| **Maintenance** | Abandoned (Last commit 2021) | **Actively Maintained (2026)** |
| **Language Support** | TypeScript / JavaScript only | **TypeScript + Python Parity** |
| **Threads (Barcelona)** | No support | **Full Threads SDK & Sub-80ms Radar** |
| **TLS Fingerprint** | Generic Node.js OpenSSL (Blocked) | **Mobile BoringSSL JA4 TLS 1.3** |
| **Automated Behavior Warnings** | Frequent (due to missing telemetry) | **Zero Warnings with Warmup Engine** |
| **Story Reactions & Polls** | Broken in recent Meta updates | **Native Mobile Protocol Supported** |
| **Media & Story Download** | Manual buffer parsing | **Built-in high-speed Downloader** |
| **Close Friends Management** | Unstable | **Native add/remove endpoints** |

---

## Quick Migration (Side-by-Side)

### 1. Installation

```bash
# Remove abandoned package
npm uninstall instagram-private-api

# Install modern SDK
npm install @molkex/instagram-private-api
```

### 2. Client Initialization

#### Legacy Dilame Code:
```typescript
import { IgApiClient } from 'instagram-private-api';

const ig = new IgApiClient();
ig.state.generateDevice(process.env.IG_USERNAME);
await ig.account.login(process.env.IG_USERNAME, process.env.IG_PASSWORD);
// Often threw: IgLoginBadPasswordError or checkpoint_required
```

#### Modern @molkex Code:
```typescript
import { InstagramAPI, InstagramSession } from '@molkex/instagram-private-api';

// Option A: Using managed signing key (Zero device overhead)
const ig = new InstagramAPI({
  apiKey: process.env.INSTAGRAM_API_KEY,
  devicePreset: 'android_pixel8'
});

// Option B: Restoring saved session
const session = InstagramSession.loadFromFile('session.json');
const ig = new InstagramAPI({ session });
```

---

## Method Mapping Reference

| Action | Legacy Dilame Method | @molkex Method |
|:---|:---|:---|
| **Self Profile** | `ig.account.currentUser()` | `ig.user.profileSelf()` |
| **User Profile by ID** | `ig.user.info(userId)` | `ig.user.info(userId)` |
| **User Profile by Username** | `ig.user.searchExact(username)` | `ig.user.infoByUsername(username)` |
| **Timeline Feed** | `ig.feed.timeline().items()` | `ig.feed.timeline({ count: 15 })` |
| **Send Direct Message** | `ig.entity.directThread([id]).broadcastText(text)` | `ig.direct.sendMessage({ username, text })` |
| **Send Link Card** | Not natively supported | `ig.direct.sendMessage({ username, text, linkPreview: url })` |
| **React to Story** | `ig.media.like(...)` (Complex payload) | `ig.story.react({ storyId, emoji, recipientId })` |
| **Organic Warmup** | Custom scripts required | `ig.warmup.runSession({ feedScrolls: 8, storyViews: 4 })` |
| **Download Media** | Manual CDN fetch | `ig.download(mediaIdOrUrl, './downloads')` |
| **Download Stories** | Manual parse | `ig.story.download(username, './downloads')` |
| **Close Friends** | `ig.friendship.setBesties(...)` | `ig.friendship.closeFriendAdd(userId)` |
| **Threads Integration** | Unavailable | `ig.threads.searchPosts(query)` / `threads.reply(...)` |

---

## Resolving Top Dilame Issues

### 1. Fixing `IgLoginBadPasswordError`
In modern Instagram, sending plaintext passwords via legacy protocols results in a bad password response even when credentials are valid.
**Fix**: Use serialized mobile session cookies or sign via our mobile signing gateway which performs authentic RSA-PKCS1 OAEP password encryption against Meta public keys.

### 2. Fixing `checkpoint_required` and `feedback_required`
Meta blocks requests whose TLS fingerprints do not match real mobile apps.
**Fix**: `@molkex` matches official Android 14 OkHttp and iOS 17 Network.framework TLS cipher orders and ALPN negotiations.

### 3. Avoiding "Automated Behavior" Warnings
Sending repetitive API calls without UI context triggers heuristic bot detection.
**Fix**: Run `ig.warmup.runSession()` before executing outreach campaigns to simulate human timeline dwell times and background telemetry.

---

## Need Support or Commercial Access?
For custom migration assistance, high-throughput clusters, or dedicated proxies:
- Telegram: [@mxmtkchk](https://t.me/mxmtkchk)
