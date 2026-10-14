import test from 'node:test';
import assert from 'node:assert/strict';
import { parseImageDataUrl } from '../lib/photo-data.mjs';
import { writeNote } from '../lib/game.mjs';
import { newSession } from '../lib/game.mjs';
import { applyAction } from './helpers.mjs';

test('parseImageDataUrl accepts valid base64 and rejects truncated payloads', () => {
  const b64 = Buffer.alloc(320, 0xff).toString('base64');
  const ok = parseImageDataUrl(`data:image/jpeg;base64,${b64}`);
  assert.equal(ok?.mime, 'jpeg');
  assert.equal(ok?.body.length, 320);
  assert.equal(parseImageDataUrl('data:image/jpeg;base64,!!!'), null);
  assert.equal(parseImageDataUrl(`data:image/jpeg;base64,${Buffer.from('tiny').toString('base64')}`), null);
});

test('writeNote rejects corrupt image data instead of storing a broken file', () => {
  const s = newSession();
  s.labAccessActive = true;
  const bad = writeNote(s, { rel: 'photos/x.jpg', name: 'X', text: 'data:image/jpeg;base64,!!!', kind: 'image' });
  assert.equal(bad.ok, false);
  assert.equal(s.files.some(f => f.rel === 'photos/x.jpg'), false);
  const good = writeNote(s, {
    rel: 'photos/x.jpg',
    name: 'X',
    text: `data:image/jpeg;base64,${Buffer.alloc(320, 0xab).toString('base64')}`,
    kind: 'image',
  });
  assert.equal(good.ok, true);
  const read = applyAction(s, 'tool', { tool: 'file.read', rel: 'photos/x.jpg' });
  assert.equal(read.ok, true);
  assert.match(read.file.href, /handset-file/);
});
