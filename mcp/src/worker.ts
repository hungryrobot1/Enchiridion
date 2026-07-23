/**
 * Remote entry point: the Enchiridion MCP server on Cloudflare Workers.
 *
 * Serves MCP over Streamable HTTP at /mcp — stateless: each request gets a
 * fresh server instance wired to a fetch-native transport (@hono/mcp). The
 * corpus cache lives at module scope, so texts fetched from GitHub persist
 * across requests within an isolate.
 *
 * Same buildServer() as the stdio entry (src/server.ts) — one server, two
 * transports. Connect a client to:  https://<host>/mcp
 */

import { Hono } from 'hono';
import { StreamableHTTPTransport } from '@hono/mcp';
import { buildServer } from './tools.js';

const LANDING = `Enchiridion MCP server

This is a Model Context Protocol endpoint for the Enchiridion Great Books
curriculum (https://enchiridion.education).

Connect your MCP client to:  /mcp   (Streamable HTTP)

Repository: https://github.com/hungryrobot1/Enchiridion
`;

const app = new Hono();

app.all('/mcp', async (c) => {
  const server = buildServer();
  const transport = new StreamableHTTPTransport();
  await server.connect(transport);
  return transport.handleRequest(c);
});

app.get('/', (c) => c.text(LANDING));

export default app;
