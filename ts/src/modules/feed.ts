/** Feed, timeline, and explore discovery endpoints */

export class FeedModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async timeline(count: number = 15, maxId?: string): Promise<any> {
    const params: Record<string, string> = { count: String(count) };
    if (maxId) params.max_id = maxId;
    return this.client.get("/api/v1/feed/timeline/", params);
  }

  public async user(userId: string | number, maxId?: string): Promise<any> {
    const params: Record<string, string> = {};
    if (maxId) params.max_id = maxId;
    return this.client.get(`/api/v1/feed/user/${userId}/`, Object.keys(params).length ? params : undefined);
  }

  public async explore(isPrefetch: boolean = false): Promise<any> {
    return this.client.get("/api/v1/discover/topical_explore/", {
      is_prefetch: isPrefetch ? "true" : "false"
    });
  }
}
