# Capabilities, Free Tier & Commercial Licensing

This SDK is engineered for professional developers, SaaS platforms, AI agent builders, and agencies requiring scalable Instagram and Threads automation.

---

## Tier Comparison Matrix

| Feature | Open Community Tier (Free) | Commercial / Enterprise Key |
|---|---|---|
| **Public Profile Inspection** | Full access (`user.info_by_username`, `pk_from_code`) | Full access |
| **Media & Reels Metadata** | Full access (`media.info`, shortcode conversions) | Full access |
| **Feed Browsing** | Public timeline and user feed | Full access with CDN prefetch |
| **Model Deserialization** | Pydantic & TypeScript types | Full access |
| **Hardware Presets** | Device catalog inspection | Full access |
| **Direct Messaging (DMs)** | Limited / Demo rate | **Unlimited cold outreach, links & reactions** |
| **Story Seen & Reactions** | Mock mode | **Live paired timestamp seen beacons & reactions** |
| **Reels & Feed Comments** | Mock mode | **Threaded replies, like comments, pin** |
| **Threads Search & Replies** | 10 searches / day | **Unlimited sub-80ms search & direct replies** |
| **JA4 TLS 1.3 BoringSSL Engine** | Standard fallback | **Authentic iPhone 15 Pro & Android 14 Handshakes** |
| **Anti-Checkpoint Telemetry** | Basic delays | **Pigeon / Scribe event batcher integration** |
| **Support & SLA** | Community issues | **Direct priority support on Telegram** |

---

## Why Mutation Endpoints Require Active Signing

Meta monitors edge network characteristics closely. While reading public endpoints is relatively lenient, **all write actions** (`direct.send_message`, `story.seen`, `media.comment`, `media.like`, `threads.reply`) trigger immediate automated inspection:

1. Requests lacking authentic BoringSSL GREASE cipher handshakes trigger `checkpoint_required` within 3–5 actions.
2. Requests missing cryptographically valid `signed_body` or mismatched device capabilities are dropped by Instagram's gateway.

Our signing engine bridges this gap by generating authentic signatures and running traffic through an authentic TLS 1.3 pipeline.

---

## Obtaining a Commercial License or Self-Hosted Daemon

For API keys, custom quotas, agency clusters, or self-hosted standalone signing daemon packages:

- **Contact**: [@mxmtkchk](https://t.me/mxmtkchk) on Telegram
- **Payment Methods**: USDT (TRC-20), Crypto, Wire
- **Response Time**: Usually under 1 hour

Included with enterprise access:
- Managed cloud signing endpoints or Dockerized local daemon (`http://127.0.0.1:8643`).
- 99.9% uptime SLA with automatic endpoint rotation upon Meta app updates.
- Private technical onboarding and integration assistance.
