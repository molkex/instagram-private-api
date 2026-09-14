/** Story viewer, highlight discovery, authentic view beacons, and story downloader */
import * as fs from "fs";
import * as path from "path";

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

  public async download(storyMediaId: string | number, outputPath?: string): Promise<any> {
    const info = await this.client.media.info(storyMediaId);
    const items = info?.items || [];
    if (!items.length) return { error: "Story item not found or expired" };

    const item = items[0];
    const isVideo = !!item.video_versions?.length;
    let cdnUrl = isVideo ? item.video_versions?.[0]?.url : item.image_versions2?.candidates?.[0]?.url;
    const ext = isVideo ? "mp4" : "jpg";

    if (!cdnUrl) return { error: "No story stream available" };

    const result: Record<string, any> = {
      story_id: String(storyMediaId),
      media_type: isVideo ? "video" : "photo",
      url: cdnUrl,
      ext
    };

    if (outputPath) {
      let targetPath = outputPath;
      if (fs.existsSync(targetPath) && fs.lstatSync(targetPath).isDirectory()) {
        targetPath = path.join(targetPath, `story_${storyMediaId}.${ext}`);
      }
      const res = await fetch(cdnUrl);
      const buffer = Buffer.from(await res.arrayBuffer());
      fs.writeFileSync(targetPath, buffer);
      result.output_path = targetPath;
      result.bytes_downloaded = buffer.length;
    }

    return result;
  }
}
