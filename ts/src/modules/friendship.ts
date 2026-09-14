/** Follow, unfollow, block, and follower pagination endpoints */

export class FriendshipModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async create(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/create/${userId}/`, { user_id: String(userId) });
  }

  public async destroy(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/destroy/${userId}/`, { user_id: String(userId) });
  }

  public async block(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/block/${userId}/`, { user_id: String(userId) });
  }

  public async unblock(userId: string | number): Promise<any> {
    return this.client.post(`/api/v1/friendships/unblock/${userId}/`, { user_id: String(userId) });
  }

  public async followers(userId: string | number, maxId?: string): Promise<any> {
    const params: Record<string, string> = {};
    if (maxId) params.max_id = maxId;
    return this.client.get(`/api/v1/friendships/${userId}/followers/`, Object.keys(params).length ? params : undefined);
  }

  public async following(userId: string | number, maxId?: string): Promise<any> {
    const params: Record<string, string> = {};
    if (maxId) params.max_id = maxId;
    return this.client.get(`/api/v1/friendships/${userId}/following/`, Object.keys(params).length ? params : undefined);
  }
}
