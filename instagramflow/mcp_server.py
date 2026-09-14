"""Model Context Protocol (MCP) Server for Instagram & Threads automation.

Run as an MCP server for Claude Desktop, Cursor, or Windsurf:
    python -m instagramflow.mcp_server
"""
from __future__ import annotations

import sys
import json
import os
from .client import InstagramAPI
from .threads import ThreadsAPI

TOOLS = [
    {
        "name": "instagram_send_direct_message",
        "description": "Send a 1-on-1 Instagram Direct Message with optional link preview",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Target Instagram username"},
                "text": {"type": "string", "description": "Message content"},
                "link_preview": {"type": "string", "description": "Optional URL to attach"}
            },
            "required": ["username", "text"]
        }
    },
    {
        "name": "instagram_run_warmup",
        "description": "Run an organic warmup session with feed scrolls and story viewing to eliminate checkpoints",
        "inputSchema": {
            "type": "object",
            "properties": {
                "feed_scrolls": {"type": "integer", "default": 8, "description": "Number of feed scroll events"},
                "story_views": {"type": "integer", "default": 4, "description": "Number of story views"}
            }
        }
    },
    {
        "name": "threads_search_posts",
        "description": "Sub-80ms real-time keyword search across public Threads discussions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword or hashtag"},
                "limit": {"type": "integer", "default": 10, "description": "Max posts to return"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "threads_reply_post",
        "description": "Reply directly to any external Threads discussion without App Review limitations",
        "inputSchema": {
            "type": "object",
            "properties": {
                "parent_post_id": {"type": "string", "description": "Thread post ID"},
                "text": {"type": "string", "description": "Reply message"}
            },
            "required": ["parent_post_id", "text"]
        }
    }
]

def handle_call_tool(name: str, arguments: dict) -> dict:
    api_key = os.getenv("INSTAGRAM_API_KEY", "ig_demo_key")
    if name == "instagram_send_direct_message":
        ig = InstagramAPI(api_key=api_key)
        res = ig.direct.send_message(
            username=arguments["username"],
            text=arguments["text"],
            link_preview=arguments.get("link_preview")
        )
        return {"content": [{"type": "text", "text": f"Direct message sent: {res.get('status', 'ok')}"}]}
    elif name == "instagram_run_warmup":
        ig = InstagramAPI(api_key=api_key)
        res = ig.warmup.run_session(
            feed_scrolls=arguments.get("feed_scrolls", 8),
            story_views=arguments.get("story_views", 4)
        )
        return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    elif name == "threads_search_posts":
        threads = ThreadsAPI(api_key=api_key)
        res = threads.search(query=arguments["query"], limit=arguments.get("limit", 10))
        posts = [p.model_dump() for p in res.posts]
        return {"content": [{"type": "text", "text": json.dumps(posts, indent=2)}]}
    elif name == "threads_reply_post":
        threads = ThreadsAPI(api_key=api_key)
        res = threads.reply(parent_post_id=arguments["parent_post_id"], text=arguments["text"])
        return {"content": [{"type": "text", "text": f"Reply dispatched: {res.get('reply_id')}"}]}
    raise ValueError(f"Unknown tool: {name}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--list-tools":
        print(json.dumps(TOOLS, indent=2))
        return

    # Standard JSON-RPC MCP loop for stdio transports
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "instagram-private-api-mcp", "version": "1.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                result = handle_call_tool(params.get("name"), params.get("arguments", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            else:
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
