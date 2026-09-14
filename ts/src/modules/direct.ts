/** Direct messaging, rich reactions, and thread management endpoints */
import { DirectMessageOptions } from "../types";

export class DirectModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async inbox(limit: number = 20): Promise<any> {
    return this.client.get("/api/v1/direct_v2/inbox/", { persistentBadging: "true", limit: String(limit) });
  }

  public async thread(threadId: string): Promise<any> {
    return this.client.get(`/api/v1/direct_v2/threads/${threadId}/`);
  }

  public async sendMessage(options: DirectMessageOptions): Promise<any> {
    const action = options.linkPreview ? "broadcast/link/" : "broadcast/text/";
    const data: Record<string, string> = {
      text: options.text,
      client_context: String(Date.now())
    };

    if (options.linkPreview) {
      data.link_text = options.text;
      data.link_urls = JSON.stringify([options.linkPreview]);
    }

    if (options.threadId) {
      data.thread_ids = `[${options.threadId}]`;
    } else if (options.recipientUsers) {
      data.recipient_users = JSON.stringify(options.recipientUsers);
    } else if (options.username) {
      data.recipient_users = JSON.stringify([options.username]);
    }

    return this.client.post(`/api/v1/direct_v2/threads/${action}`, data);
  }

  public async sendLike(threadId: string): Promise<any> {
    return this.client.post("/api/v1/direct_v2/threads/broadcast/like/", {
      thread_ids: `[${threadId}]`,
      client_context: String(Date.now())
    });
  }

  public async sendReaction(threadId: string, itemId: string, emoji: string): Promise<any> {
    return this.client.post("/api/v1/direct_v2/threads/broadcast/item_reaction/", {
      thread_id: threadId,
      item_id: itemId,
      reaction_type: "like",
      reaction_status: "created",
      emoji: emoji,
      client_context: String(Date.now())
    });
  }

  public async deleteReaction(threadId: string, itemId: string, emoji: string): Promise<any> {
    return this.client.post("/api/v1/direct_v2/threads/broadcast/item_reaction/", {
      thread_id: threadId,
      item_id: itemId,
      reaction_type: "like",
      reaction_status: "deleted",
      emoji: emoji,
      client_context: String(Date.now())
    });
  }

  public async replyToItem(threadId: string, targetItemId: string, text: string): Promise<any> {
    return this.client.post("/api/v1/direct_v2/threads/broadcast/text/", {
      thread_ids: `[${threadId}]`,
      replied_to_item_id: targetItemId,
      text: text,
      client_context: String(Date.now())
    });
  }

  public async replyToStory(storyId: string, text: string, recipientId: string): Promise<any> {
    return this.client.post("/api/v1/direct_v2/threads/broadcast/reel_share/", {
      recipient_users: `[${recipientId}]`,
      reel_id: storyId,
      media_id: storyId,
      text: text,
      client_context: String(Date.now())
    });
  }

  public async reactToStory(storyId: string, emoji: string, recipientId: string): Promise<any> {
    return this.client.post("/api/v1/direct_v2/threads/broadcast/reel_react/", {
      recipient_users: `[${recipientId}]`,
      reel_id: storyId,
      media_id: storyId,
      reaction_emoji: emoji,
      client_context: String(Date.now())
    });
  }

  public async pinThread(threadId: string): Promise<any> {
    return this.client.post(`/api/v1/direct_v2/threads/${threadId}/pin/`);
  }

  public async unpinThread(threadId: string): Promise<any> {
    return this.client.post(`/api/v1/direct_v2/threads/${threadId}/unpin/`);
  }

  public async deleteItem(threadId: string, itemId: string): Promise<any> {
    return this.client.post(`/api/v1/direct_v2/threads/${threadId}/items/${itemId}/delete/`);
  }

  public async getPresence(): Promise<any> {
    return this.client.get("/api/v1/direct_v2/get_presence/");
  }
}
