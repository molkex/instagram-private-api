/** Configuration and API payload types */

export interface InstagramClientOptions {
  apiKey: string;
  sessionToken?: string;
  signingServer?: string;
  devicePreset?: "iphone_15_pro" | "iphone_15_pro_max" | "pixel_8_pro" | "galaxy_s24" | string;
  proxy?: string;
  rateLimit?: number;
  timeout?: number;
}

export interface DirectMessageOptions {
  threadId?: string;
  recipientUsers?: string[];
  username?: string;
  text: string;
  linkPreview?: string;
}

export interface SignedRequestResponse {
  headers: Record<string, string>;
  signed_body?: Record<string, any>;
  signature?: string;
  device?: Record<string, any>;
}

export interface ThreadPostItem {
  id: string;
  author: string;
  text: string;
  like_count: number;
  reply_count: number;
  taken_at?: number;
}
