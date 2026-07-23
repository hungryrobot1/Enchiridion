/** End-to-end smoke test: spawn the built server over stdio, call every tool. */
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const client = new Client({ name: 'smoke', version: '0.0.0' });
await client.connect(
  new StdioClientTransport({ command: 'node', args: ['dist/server.js'] })
);

const show = (label, res, n = 700) => {
  const t = res.content?.[0]?.text ?? '(no text)';
  console.log(`\n===== ${label} (${t.length} chars) =====`);
  console.log(t.slice(0, n));
};

const tools = await client.listTools();
console.log('tools:', tools.tools.map((t) => t.name).join(', '));

show('list_works kind=text era=rome', await client.callTool({ name: 'list_works', arguments: { kind: 'text', era: 'Rome' } }), 500);
show('list_works kind=supplement', await client.callTool({ name: 'list_works', arguments: { kind: 'supplement' } }), 500);
show('get_structure euclid', await client.callTool({ name: 'get_structure', arguments: { id: 'euclid-elements', depth: 1 } }), 700);
show('get_structure module', await client.callTool({ name: 'get_structure', arguments: { id: '1-ancient-greek', depth: 1 } }), 700);
show('read euclid I.47', await client.callTool({ name: 'read', arguments: { id: 'euclid-elements', section: 'book-i/proposition-47' } }), 700);
show('read whole (small work)', await client.callTool({ name: 'read', arguments: { id: 'epictetus-enchiridion' } }), 300);
show('read large (no section)', await client.callTool({ name: 'read', arguments: { id: 'holy-bible-kjv' } }), 400);
show('read module chapter section', await client.callTool({ name: 'read', arguments: { id: '1-ancient-greek', section: '01-alphabet-and-reading-aloud' } }), 300);
show('search plato-meno "square"', await client.callTool({ name: 'search', arguments: { id: 'plato-meno', query: 'the double' } }), 500);
show('get_syllabus', await client.callTool({ name: 'get_syllabus', arguments: {} }), 600);

await client.close();
console.log('\nsmoke: all calls returned');
