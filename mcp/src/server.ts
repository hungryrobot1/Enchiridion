#!/usr/bin/env node
/**
 * Local entry point: the Enchiridion MCP server over stdio.
 * (The remote entry point is src/worker.ts — Cloudflare Workers.)
 */

import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { buildServer } from './tools.js';

const transport = new StdioServerTransport();
await buildServer().connect(transport);
console.error('enchiridion-mcp: serving the published corpus over stdio');
