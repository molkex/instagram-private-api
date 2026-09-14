/** Dedicated high-performance Threads Mobile Protocol Client */
import { RemoteSigner } from "./remote-signer";
import { ThreadPostItem } from "./types";
import { AuthError, RateLimitError } from "./errors";

export class ThreadsAPI {
  public static readonly BASE_URL = "https://i.instagram.com";
  private apiKey: string;
  private sessionToken?: string;
  private signer: RemoteSigner;

  constructor(options: { apiKey: string; sessionToken?: string; signingServer?: string; devicePreset?: string }) {
    this.apiKey = options.apiKey;
    this.sessionToken = options.sessionToken;
    this.signer = new RemoteSigner(
      options.signingServer || "http://127.0.0.1:8643",
      this.apiKey,
      options.devicePreset || "iphone_15_pro"
    );
  }

  public async search(query: string, limit: number = 10): Promise<{ query: string; posts: ThreadPostItem[] }> {
    const path = `/api/v1/fbsearch/topsearch_flat/?query=${encodeURIComponent(query)}&count=${limit}&context=bloks_search`;
    const signed = await this.signer.signRequest(path, "GET", undefined, "threads");

    const headers = { ...signed.headers };
    if (this.sessionToken) {
      headers["Authorization"] = `Bearer ${this.sessionToken}`;
    }

    const res = await fetch(`${ThreadsAPI.BASE_URL}${path}`, { headers });
    if (res.status === 401) throw new AuthError();
    if (res.status === 429) throw new RateLimitError();

    const data = (await res.json()) as any;
    const posts: ThreadPostItem[] = (data.list || []).map((item: any) => {
      const thread = item.thread || item;
      return {
        id: String(thread.id || thread.pk || ""),
        author: String(thread.user?.username || "unknown"),
        text: String(thread.caption?.text || thread.text || ""),
        like_count: Number(thread.like_count || 0),
        reply_count: Number(thread.reply_count || 0),
        taken_at: thread.taken_at
      };
    });

    return { query, posts };
  }

  public async reply(parentPostId: string, text: string): Promise<any> {
    const path = "/api/v1/media/configure_text_post_app_feed/";
    const body = {
      text_post_app_info: JSON.stringify({ reply_to_post_id: parentPostId }),
      caption: text
    };

    const signed = await this.signer.signRequest(path, "POST", body, "threads");
    const headers = { ...signed.headers };
    if (this.sessionToken) {
      headers["Authorization"] = `Bearer ${this.sessionToken}`;
    }

    const res = await fetch(`${ThreadsAPI.BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: new URLSearchParams(signed.signed_body || body).toString()
    });

    if (res.status === 401) throw new AuthError();
    if (res.status === 429) throw new RateLimitError();

    return res.json();
  }

  public async like(postId: string): Promise<any> {
    const path = `/api/v1/media/${postId}/like/`;
    const signed = await this.signer.signRequest(path, "POST", { media_id: postId }, "threads");
    const headers = { ...signed.headers };
    if (this.sessionToken) headers["Authorization"] = `Bearer ${this.sessionToken}`;

    const res = await fetch(`${ThreadsAPI.BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: new URLSearchParams(signed.signed_body || { media_id: postId }).toString()
    });
    return res.json();
  }

  public async repost(postId: string): Promise<any> {
    const path = `/api/v1/media/${postId}/repost/`;
    const signed = await this.signer.signRequest(path, "POST", { media_id: postId }, "threads");
    const headers = { ...signed.headers };
    if (this.sessionToken) headers["Authorization"] = `Bearer ${this.sessionToken}`;

    const res = await fetch(`${ThreadsAPI.BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: new URLSearchParams(signed.signed_body || { media_id: postId }).toString()
    });
    return res.json();
  }
}
