/** Story viewer, highlight discovery, and authentic view beacons */

export class StoryModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async userStories(userId: string | number): Promise<any> {
    return this.client.get("/api/v1/feed/reels_media/", { reel_ids: String(userId) });
  }

  public async highlights(userId: string | number): Promise<any> {
    return this.client.get(`/api/v1/highlights/${userId}/highlights_tray/`);
  }

  public async seen(storyMediaId: string, takenAt?: number): Promise<any> {
    const now = Math.floor(Date.now() / 1000);
    const ts = takenAt || now - 30;
    const data = {
      reels: { [storyMediaId]: [`${ts}_${now}`] },
      reel: "1",
      live_vod: "0"
    };
    return this.client.post("/api/v2/media/seen/", data);
  }

  public async like(storyId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${storyId}/like/`, { media_id: String(storyId) });
  }

  public async unlike(storyId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${storyId}/unlike/`, { media_id: String(storyId) });
  }

  public async reply(storyId: string | number, text: string, recipientId: string | number): Promise<any> {
    return this.client.direct.replyToStory(String(storyId), text, String(recipientId));
  }

  public async react(storyId: string | number, emoji: string, recipientId: string | number): Promise<any> {
    return this.client.direct.reactToStory(String(storyId), emoji, String(recipientId));
  }
}
