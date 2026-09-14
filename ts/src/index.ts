/**
 * @molkex/instagram-private-api
 * Modern, headless Instagram & Threads Mobile Private API SDK for Node.js and TypeScript.
 */

export { InstagramAPI } from "./client";
export { ThreadsAPI } from "./threads";
export { RemoteSigner } from "./remote-signer";

export * from "./types";
export * from "./errors";

export { UserModule } from "./modules/user";
export { FeedModule } from "./modules/feed";
export { DirectModule } from "./modules/direct";
export { MediaModule } from "./modules/media";
export { CommentModule } from "./modules/comment";
export { StoryModule } from "./modules/story";
export { NoteModule } from "./modules/note";
export { FriendshipModule } from "./modules/friendship";
export { WarmupModule } from "./modules/warmup";
