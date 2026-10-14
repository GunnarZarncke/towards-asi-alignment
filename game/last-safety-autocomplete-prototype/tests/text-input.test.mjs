import test from 'node:test';
import assert from 'node:assert/strict';
import { utteranceSlice } from '../lib/text/tab-complete.mjs';

test('utteranceSlice: speech vs commands', () => {
  assert.deepEqual(utteranceSlice('Can Daniel'), { utterance: 'Can Daniel', prefix: '' });
  assert.deepEqual(utteranceSlice('say Can Daniel'), { utterance: 'Can Daniel', prefix: 'say ' });
  assert.equal(utteranceSlice('go courtyard'), null);
  assert.equal(utteranceSlice('s access'), null);
  assert.equal(utteranceSlice('3'), null);
});
