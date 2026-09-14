/** Media, Reels, shortcodes, and bookmark collection endpoints */

const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";

export class MediaModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public static pkFromCode(code: string): string {
    let pk = BigInt(0);
    const base = BigInt(64);
    for (const ch of code) {
      pk = pk * base + BigInt(ALPHABET.indexOf(ch));
    }
    return pk.toString();
  }

  public static codeFromPk(pk: number | string | bigint): string {
    let num = BigInt(pk);
    const base = BigInt(64);
    let out = "";
    while (num > BigInt(0)) {
      const rem = Number(num % base);
      num = num / base;
      out = ALPHABET[rem] + out;
    }
    return out || "A";
  }

  public async info(mediaId: string | number): Promise<any> {
    return this.client.get(`/api/v1/media/${mediaId}/info/`);
  }

  public async likers(mediaId: string | number): Promise<any> {
    return this.client.get(`/api/v1/media/${mediaId}/likers/`);
  }

  public async userClips(userId: string | number, maxId?: string): Promise<any> {
    const data: Record<string, string> = {
      target_user_id: String(userId),
      page_size: "12"
    };
    if (maxId) data.max_id = maxId;
    return this.client.post("/api/v1/clips/user/", data);
  }

  public async like(mediaId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/like/`);
  }

  public async unlike(mediaId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/unlike/`);
  }

  public async save(mediaId: string | number, collectionId?: string): Promise<any> {
    const data: Record<string, string> = {};
    if (collectionId) data.added_collection_ids = `[${collectionId}]`;
    return this.client.post(`/api/v1/media/${mediaId}/save/`, Object.keys(data).length ? data : undefined);
  }

  public async unsave(mediaId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/unsave/`);
  }

  public async comment(mediaId: string | number, text: string): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/comment/`, { comment_text: text });
  }

  public async delete(mediaId: string | number, mediaType: string = "PHOTO"): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/delete/`, {
      media_id: String(mediaId),
      media_type: mediaType
    });
  }

  public async edit(mediaId: string | number, caption: string): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/edit_media/`, { caption_text: caption });
  }

  public async archive(mediaId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/only_me/`, { media_id: String(mediaId) });
  }

  public async unarchive(mediaId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/undo_only_me/`, { media_id: String(mediaId) });
  }
}
