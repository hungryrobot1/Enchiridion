/** Smoke test the remote (Streamable HTTP) entry — point at a running Worker. */
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';

const url = process.argv[2] ?? 'http://localhost:8787/mcp';
const client = new Client({ name: 'smoke-http', version: '0.0.0' });
await client.connect(new StreamableHTTPClientTransport(new URL(url)));

const show = (label, res, n = 400) => {
  const t = res.content?.[0]?.text ?? '(no text)';
  console.log(`\n===== ${label} (${t.length} chars) =====`);
  console.log(t.slice(0, n));
};

const tools = await client.listTools();
console.log('tools:', tools.tools.map((t) => t.name).join(', '));

show('read euclid I.47', await client.callTool({ name: 'read', arguments: { id: 'euclid-elements', section: 'book-i/proposition-47' } }));
show('list_works supplements', await client.callTool({ name: 'list_works', arguments: { kind: 'supplement' } }));
show('search meno', await client.callTool({ name: 'search', arguments: { id: 'plato-meno', query: 'the double' } }));

await client.close();
console.log('\nsmoke-http: all calls returned');
