/** User profile, metadata discovery, and settings endpoints */

export class UserModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async self(): Promise<any> {
    return this.client.get("/api/v1/accounts/current_user/?edit=true");
  }

  public async infoByUsername(username: string): Promise<any> {
    return this.client.get(`/api/v1/users/${username}/usernameinfo/`);
  }

  public async infoById(userId: string | number): Promise<any> {
    return this.client.get(`/api/v1/users/${userId}/info/`);
  }

  public async updateBio(bio: string): Promise<any> {
    return this.client.post("/api/v1/accounts/set_biography/", { raw_text: bio });
  }
}
