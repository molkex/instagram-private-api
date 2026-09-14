# Sessions, Proxies, and Security Best Practices

## Session Persistence

To avoid repeated logins and keep trust scores high, persist session states across runs using `SessionStorage`:

### Python

```python
from instagramflow import InstagramAPI, SessionStorage

# 1. Restore an existing session
try:
    session = SessionStorage.load_from_file("data/session_user.json")
    ig = InstagramAPI(
        api_key="ig_...",
        session_token=session.session_token,
        device_preset=session.device_preset
    )
except FileNotFoundError:
    # 2. First-time initialization
    ig = InstagramAPI(api_key="ig_...", device_preset="iphone_15_pro")
    # ... after logging in ...
    storage = SessionStorage(
        session_token=ig.session_token,
        device_preset=ig.device_preset
    )
    storage.save_to_file("data/session_user.json")
```

### TypeScript / Node.js

```typescript
import { InstagramAPI } from "@molkex/instagram-private-api";
import * as fs from "fs";

// Load serialized session
const sessionData = JSON.parse(fs.readFileSync("session.json", "utf-8"));
const ig = new InstagramAPI({
  apiKey: "ig_...",
  sessionToken: sessionData.session_token,
  devicePreset: sessionData.device_preset
});
```

---

## Proxy Configuration

Proxy quality is the single most common cause of automated checkpoints.

### Recommendations
1. **Residential Mobile Proxies (4G/5G)**: Highest trust score. Match the proxy country with your target account's registration locale.
2. **Dedicated Static Residential**: Excellent for 24/7 long-running daemons.
3. **Avoid Datacenter IPs**: AWS, DigitalOcean, Hetzner, and OVH IP ranges are pre-flagged by Meta's firewall.

### Using Proxies with the SDK

```python
ig = InstagramAPI(
    api_key="ig_...",
    proxy="http://username:password@proxy-node.provider.com:8000",
    rate_limit=1.5  # Seconds between mutations
)
```
