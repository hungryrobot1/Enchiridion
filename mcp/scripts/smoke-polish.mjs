/** Focused checks for the polish pass: range-collapse, lang, images, budget. */
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const client = new Client({ name: 'smoke-polish', version: '0.0.0' });
await client.connect(new StdioClientTransport({ command: 'node', args: ['dist/server.js'] }));

const call = (name, args) => client.callTool({ name, arguments: args });
const textOf = (r) => r.content.find((c) => c.type === 'text')?.text ?? '';
const imgs = (r) => r.content.filter((c) => c.type === 'image');

console.log('=== get_structure euclid (range-collapse; was ~450 lines) ===');
const gs = textOf(await call('get_structure', { id: 'euclid-elements' }));
console.log(gs.split('\n').length, 'lines');
console.log(gs.split('\n').filter((l) => /book-i\b/.test(l)).join('\n'));

console.log('\n=== get_structure euclid section=book-i (expand one book) ===');
const gsb = textOf(await call('get_structure', { id: 'euclid-elements', section: 'book-i' }));
console.log(gsb.split('\n').slice(-6).join('\n'));

console.log('\n=== read I.47 default (English only, diagram inlined) ===');
const r47 = await call('read', { id: 'euclid-elements', section: 'book-i/proposition-47' });
const t47 = textOf(r47);
console.log('images returned:', imgs(r47).length, '| mimeType:', imgs(r47)[0]?.mimeType, '| kb:', Math.round((imgs(r47)[0]?.data.length ?? 0) * 0.75 / 1024));
console.log('has Greek?', /ὀρθογων/.test(t47), '| has English?', /right-angled/.test(t47));
console.log('image ref absolute?', /!\[.*\]\(https:\/\/raw\./.test(t47));
console.log(t47.slice(0, 260));

console.log('\n=== read I.47 lang=both (Greek present) ===');
const r47b = textOf(await call('read', { id: 'euclid-elements', section: 'book-i/proposition-47', lang: 'both' }));
console.log('has Greek?', /ὀρθογων/.test(r47b), '| has English?', /right-angled/.test(r47b));

console.log('\n=== read whole book-i (should degrade to sub-structure, no flood) ===');
const rbi = await call('read', { id: 'euclid-elements', section: 'book-i' });
console.log('images:', imgs(rbi).length, '| text lines:', textOf(rbi).split('\n').length);
console.log(textOf(rbi).split('\n').slice(0, 4).join('\n'));

await client.close();
console.log('\nsmoke-polish: done');
