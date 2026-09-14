/** Comments and threaded reply moderation endpoints */

export class CommentModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async list(mediaId: string | number, minId?: string): Promise<any> {
    const params: Record<string, string> = {};
    if (minId) params.min_id = minId;
    return this.client.get(`/api/v1/media/${mediaId}/comments/`, Object.keys(params).length ? params : undefined);
  }

  public async replies(mediaId: string | number, commentId: string | number, minId?: string): Promise<any> {
    const params: Record<string, string> = {};
    if (minId) params.min_id = minId;
    return this.client.get(
      `/api/v1/media/${mediaId}/comments/${commentId}/child_comments/`,
      Object.keys(params).length ? params : undefined
    );
  }

  public async add(
    mediaId: string | number,
    text: string,
    repliedToCommentId?: string | number
  ): Promise<any> {
    const data: Record<string, string> = { comment_text: text };
    if (repliedToCommentId) data.replied_to_comment_id = String(repliedToCommentId);
    return this.client.post(`/api/v1/media/${mediaId}/comment/`, data);
  }

  public async like(commentId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${commentId}/comment_like/`);
  }

  public async unlike(commentId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${commentId}/comment_unlike/`);
  }

  public async delete(mediaId: string | number, commentId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/comment/${commentId}/delete/`);
  }

  public async pin(mediaId: string | number, commentId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/comment/${commentId}/pin/`);
  }

  public async unpin(mediaId: string | number, commentId: string | number): Promise<any> {
    return this.client.post(`/api/v1/media/${mediaId}/comment/${commentId}/unpin/`);
  }
}
