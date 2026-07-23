# Enchiridion MCP Server

Connects an AI model to the [Enchiridion](https://enchiridion.education) corpus so it can facilitate your reading — anchored to the actual texts, not its recollection of them.

The server exposes the certified library (primary texts, lab manuals and study guides, and the language modules) over the
[Model Context Protocol](https://modelcontextprotocol.io). Content is fetched
from this repository at `main`; nothing is bundled, so every text is available the moment it is published. Section paths match the web reader's deep links — when the model cites a passage, it can hand you a link that opens the same section on the site.

## Tools

| tool | what it does |
|---|---|
| `list_works` | the library: texts, supplements, modules (filter by kind or era) |
| `get_structure` | a work's metadata and table of contents, with stable section paths |
| `read` | the markdown itself — whole work, or exactly one section |
| `search` | literal search within a work, matches mapped to sections |
| `get_syllabus` | the Grand Tour: the program's published reading sequence |

Only certified content is served (texts whose processing is complete). The
pedagogy travels with the server: its instructions set the seminar posture —
the model as conversation partner rather than lecturer, everything rooted in
passages you can check.

## Connecting (remote — recommended)

The server runs as a hosted endpoint; no install required. Add the URL to any
MCP-capable client (claude.ai custom connectors, Claude Desktop, Claude Code,
and others):

```
https://enchiridion-mcp.enchiridion.workers.dev/mcp
```

Claude Code:

```sh
claude mcp add --transport http enchiridion https://enchiridion-mcp.enchiridion.workers.dev/mcp
```

<!-- A friendlier alias (mcp.enchiridion.education) can be added later via a
     Cloudflare custom domain, once DNS moves off Vercel. -->

## Running locally (stdio)

Requires Node 18+.

```sh
cd mcp
npm install
npm run build
claude mcp add enchiridion -- node /path/to/Enchiridion/mcp/dist/server.js
```

Or in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "enchiridion": {
      "command": "node",
      "args": ["/path/to/Enchiridion/mcp/dist/server.js"]
    }
  }
}
```

Both entries are the same server (`src/tools.ts`); only the transport differs
(`src/server.ts` = stdio, `src/worker.ts` = Streamable HTTP on Cloudflare
Workers).

## Development

```sh
npm run dev             # stdio server from source (tsx)
npm run verify-toc      # assert section paths match the live reader, corpus-wide
node scripts/smoke.mjs  # spawn the stdio server and exercise every tool
npx wrangler dev        # run the Worker locally, then:
node scripts/smoke-http.mjs   # exercise every tool over Streamable HTTP
npx wrangler deploy     # deploy to Cloudflare Workers
```

`verify-toc` is the contract with the site: it lifts the reader's own
sectioning functions from `site/src/readers/md-reader.js` and diffs both
implementations over every markdown file in the corpus. If the reader's slug
logic ever changes, this fails loudly and the mirror in `src/toc.ts` must be
updated to match.
