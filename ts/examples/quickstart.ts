import { InstagramAPI, ThreadsAPI } from "../src";

async function main() {
  // Initialize Instagram mobile client with authentic iPhone 15 Pro TLS 1.3 fingerprint
  const ig = new InstagramAPI({
    apiKey: process.env.INSTAGRAM_API_KEY || "your_api_key",
    devicePreset: "iphone_15_pro"
  });

  console.log("Fetching self profile...");
  // const me = await ig.user.self();

  console.log("Watching story with authentic timestamps...");
  // await ig.story.seen("3141592653589793238_12345");

  console.log("Sending direct reaction...");
  // await ig.direct.sendReaction("thread_123", "item_456", "❤️");

  // Threads integration
  const threads = new ThreadsAPI({
    apiKey: process.env.INSTAGRAM_API_KEY || "your_api_key"
  });

  console.log("Searching Threads discussions (<80ms)...");
  // const results = await threads.search("ai agents", 5);
}

main().catch(console.error);
