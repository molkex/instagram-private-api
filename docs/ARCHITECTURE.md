# Architecture & Protocol Specification

## High-Level Overview

`instagram-private-api` is structured as a two-tier decoupled architecture:
1. **Client Layer (Python & TypeScript SDK)**: Provides clean, typed object-oriented interfaces (`user`, `feed`, `direct`, `media`, `story`, `comment`, `note`, `threads`). It abstracts endpoints, response parsing, and error normalization.
2. **Signing & Transport Engine (BoringSSL & JA4 Daemon)**: Emulates authentic mobile hardware TLS handshakes, computes cryptographically valid `signed_body` HMAC-SHA256 signatures, injects device-specific `X-IG-*` headers, and dispatches companion analytics telemetry.

```
┌────────────────────────────────────────────────────────┐
│             Application / Bot / AI Agent              │
│       (Python SDK / TypeScript SDK / MCP Server)       │
└───────────────────────────┬────────────────────────────┘
                            │ High-Level API Calls
                            ▼
┌────────────────────────────────────────────────────────┐
│            instagram-private-api Client SDK            │
│  - Endpoint Routing     - Session Storage              │
│  - Object Deserializer  - Warmup Explorations          │
└───────────────────────────┬────────────────────────────┘
                            │ Sign Request (REST / IPC)
                            ▼
┌────────────────────────────────────────────────────────┐
│         Mobile Signing Daemon & Sidecar Engine         │
│  - BoringSSL TLS 1.3 JA4 Handshake (GREASE, ALPN h2)   │
│  - HTTP/2 SETTINGS & Pseudo-Header Sequencing          │
│  - HMAC-SHA256 Request Payload Encryption              │
│  - Pigeon / Scribe Telemetry Batcher (client_events)   │
└───────────────────────────┬────────────────────────────┘
                            │ Authentic Mobile Requests
                            ▼
┌────────────────────────────────────────────────────────┐
│         Meta Mobile Infrastructure (Instagram/Threads) │
│       i.instagram.com / graph.threads.net              │
└────────────────────────────────────────────────────────┘
```

---

## Why Legacy Scrapers Fail (The Meta Anti-Fraud Engine)

Traditional libraries (e.g. `requests`, `axios`, `urllib`, standard Python `ssl`) are immediately detected by Meta's edge proxies (FBDN / Proxygen) due to three architectural discrepancies:

### 1. TLS 1.3 Handshake & JA4 Fingerprint Mismatch
Real mobile apps running on iOS (SecureTransport / BoringSSL) or Android (Conscrypt / BoringSSL) produce specific Client Hello packets:
- **GREASE Ciphers**: Real mobile stacks inject random reserved cipher values (e.g. `0x0a0a`, `0x1a1a`).
- **Cipher Suite Order**: Standard OpenSSL lists ciphers in a server-preference order that never occurs on iPhone 15 or Samsung Galaxy.
- **Extension Ordering & ALPN**: Meta verifies the order of supported groups, signature algorithms, and key share entries.

Our signing engine negotiates authentic **JA4 TLS 1.3** handshakes identical to an authentic device on cellular or Wi-Fi.

### 2. HTTP/2 Pseudo-Header Ordering
In HTTP/2, RFC 7540 allows pseudo-headers (`:method`, `:authority`, `:scheme`, `:path`) in any order, but real mobile OS network stacks order them deterministically:
- **iOS 17**: `:method`, `:scheme`, `:path`, `:authority`
- **Android 14**: `:method`, `:authority`, `:scheme`, `:path`
- **SETTINGS Frames**: Window update frame sizes and MAX_CONCURRENT_STREAMS match official Meta Android/iOS client configurations.

### 3. Payload Signing (`signed_body`)
Critical write endpoints (login, password reset, direct messages, comments, reactions) require signed body encryption:
$$\text{Signature} = \text{HMAC-SHA256}(K_{\text{ig}}, \text{Payload})$$
$$\text{Body} = \text{signed\_body}=\text{Signature}.\text{URL-encoded JSON Payload}$$

The SDK offloads this calculation to the signing daemon, ensuring cryptographic authenticity without exposing secret keys in source files.

### 4. Telemetry Batching (`api/v1/logging/client_events/`)
Authentic Instagram users never dispatch a mutation (like or comment) in isolation. Every action in the mobile app is preceded by:
- Background prefetch (`feed/timeline/` or `feed/reels_media/`)
- Screen dwell time (1.5 to 4.5 seconds)
- Scribe analytics batches logging scroll speed, impression timestamp, and viewport dwell.

Our warmup engine (`ig.warmup`) automatically replicates these patterns.
