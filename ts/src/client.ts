/** Headless Instagram Mobile Protocol Client for TypeScript / Node.js */
import { InstagramClientOptions } from "./types";
import { RemoteSigner } from "./remote-signer";
import { AuthError, RateLimitError, ServerError } from "./errors";
import { UserModule } from "./modules/user";
import { FeedModule } from "./modules/feed";
import { DirectModule } from "./modules/direct";
import { MediaModule } from "./modules/media";
import { CommentModule } from "./modules/comment";
import { StoryModule } from "./modules/story";
import { NoteModule } from "./modules/note";
import { FriendshipModule } from "./modules/friendship";
import { WarmupModule } from "./modules/warmup";

export class InstagramAPI {
  public static readonly BASE_URL = "https://i.instagram.com";

  public readonly user: UserModule;
  public readonly feed: FeedModule;
  public readonly direct: DirectModule;
  public readonly media: MediaModule;
  public readonly comment: CommentModule;
  public readonly story: StoryModule;
  public readonly note: NoteModule;
  public readonly friendship: FriendshipModule;
  public readonly warmup: WarmupModule;

  private apiKey: string;
  private sessionToken?: string;
  private signer: RemoteSigner;

  constructor(options: InstagramClientOptions) {
    this.apiKey = options.apiKey;
    this.sessionToken = options.sessionToken;
    this.signer = new RemoteSigner(
      options.signingServer || "http://127.0.0.1:8643",
      this.apiKey,
      options.devicePreset || "iphone_15_pro"
    );

    this.user = new UserModule(this);
    this.feed = new FeedModule(this);
    this.direct = new DirectModule(this);
    this.media = new MediaModule(this);
    this.comment = new CommentModule(this);
    this.story = new StoryModule(this);
    this.note = new NoteModule(this);
    this.friendship = new FriendshipModule(this);
    this.warmup = new WarmupModule(this);
  }

  public async get(path: string, params?: Record<string, string>): Promise<any> {
    const signed = await this.signer.signRequest(path, "GET", undefined, "instagram");
    const headers = { ...signed.headers };
    if (this.sessionToken) {
      headers["Authorization"] = `Bearer ${this.sessionToken}`;
    }

    let url = `${InstagramAPI.BASE_URL}${path}`;
    if (params && Object.keys(params).length > 0) {
      const qs = new URLSearchParams(params).toString();
      url += (url.includes("?") ? "&" : "?") + qs;
    }

    const res = await fetch(url, { method: "GET", headers });
    return this.handleResponse(res);
  }

  public async post(path: string, data?: Record<string, any>): Promise<any> {
    const signed = await this.signer.signRequest(path, "POST", data, "instagram");
    const headers = { ...signed.headers };
    if (this.sessionToken) {
      headers["Authorization"] = `Bearer ${this.sessionToken}`;
    }

    const payload = signed.signed_body || data || {};
    const res = await fetch(`${InstagramAPI.BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: new URLSearchParams(payload).toString()
    });

    return this.handleResponse(res);
  }

  private async handleResponse(res: Response): Promise<any> {
    if (res.status === 401) throw new AuthError();
    if (res.status === 429) throw new RateLimitError();
    if (res.status >= 500) throw new ServerError(`Server error HTTP ${res.status}`, res.status);

    try {
      return await res.json();
    } catch {
      return { status: "ok", statusCode: res.status };
    }
  }
}
