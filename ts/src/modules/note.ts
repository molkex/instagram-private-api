/** Direct tray 24-hour status notes */

export class NoteModule {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  public async getNotes(): Promise<any> {
    return this.client.get("/api/v1/notes/get_notes/");
  }

  public async create(text: string, audience: number = 0): Promise<any> {
    return this.client.post("/api/v1/notes/create_note/", {
      text,
      audience: String(audience)
    });
  }

  public async delete(noteId: string | number): Promise<any> {
    return this.client.post("/api/v1/notes/delete_note/", {
      id: String(noteId)
    });
  }
}
