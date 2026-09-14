/** Remote signing client communicating with the local or cloud signing daemon */
import { SignedRequestResponse } from "./types";
import { ServerError, AuthError } from "./errors";

export class RemoteSigner {
  private signingServer: string;
  private apiKey: string;
  private devicePreset: string;

  constructor(signingServer: string = "http://127.0.0.1:8643", apiKey: string = "", devicePreset: string = "iphone_15_pro") {
    this.signingServer = signingServer.replace(/\/$/, "");
    this.apiKey = apiKey;
    this.devicePreset = devicePreset;
  }

  public async signRequest(
    endpoint: string,
    method: string = "POST",
    body?: Record<string, any>,
    platform: "instagram" | "threads" = "instagram"
  ): Promise<SignedRequestResponse> {
    const payload = {
      api_key: this.apiKey,
      device_preset: this.devicePreset,
      endpoint,
      method: method.toUpperCase(),
      platform,
      body: body || {}
    };

    try {
      const res = await fetch(`${this.signingServer}/v1/sign`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        if (res.status === 401 || res.status === 403) {
          throw new AuthError(`Signing daemon authorization failed: HTTP ${res.status}`);
        }
        throw new ServerError(`Signing daemon error: HTTP ${res.status}`, res.status);
      }

      return (await res.json()) as SignedRequestResponse;
    } catch (err: any) {
      if (err instanceof AuthError || err instanceof ServerError) {
        throw err;
      }
      // Fallback local signature mock for standalone development
      return this.fallbackLocalSign(endpoint, method, body, platform);
    }
  }

  private fallbackLocalSign(
    endpoint: string,
    method: string,
    body?: Record<string, any>,
    platform: string = "instagram"
  ): SignedRequestResponse {
    const isIos = this.devicePreset.includes("iphone");
    const ua = isIos
      ? "Instagram 446.0.0.32.78 (iPhone16,1; iOS 17_6_1; en_US; en-US; scale=3.00; 1179x2556; 634891234)"
      : "Instagram 446.0.0.32.78 Android (34/14; 450dpi; 1080x2400; samsung; SM-A346B; a34x; mt6877; en_US; 634891234)";

    const appId = platform === "threads" ? "3419628305025917" : "1268686196647209";

    const headers: Record<string, string> = {
      "User-Agent": ua,
      "X-IG-App-ID": appId,
      "X-IG-Capabilities": "3brTv10=",
      "X-IG-Connection-Type": "WIFI",
      "Accept-Language": "en-US,en;q=0.9",
      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    };

    return {
      headers,
      signed_body: body || {}
    };
  }
}
