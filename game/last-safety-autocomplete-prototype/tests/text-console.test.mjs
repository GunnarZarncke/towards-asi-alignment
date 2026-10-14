import test from 'node:test';
import assert from 'node:assert/strict';

process.env.DEMO_MODE = '1';
const { newSession } = await import('../lib/game.mjs');
const { createConsole, departureLine } = await import('../lib/text/console.mjs');
const { clientState } = await import('../lib/game.mjs');
const { FACTS } = await import('../lib/world/facts.mjs');

function setup() {
  const s = newSession();
  const con = createConsole(() => s);
  const outs = [con.start()];
  const run = async line => { const { out } = await con.handle(line); outs.push(out); return out; };
  return { s, con, run, outs };
}

test('departureLine names the destination room', () => {
  const s = newSession();
  s.npcs.ian.room = 'courtyard';
  const c = clientState(s);
  assert.match(departureLine(c, 'ian'), /heads to Open-air Courtyard/);
});

test('start describes the room; later commands do not reprint it', async () => {
  const { run, outs } = setup();
  assert.match(outs[0], /Commons \/ Arrival/);
  assert.match(outs[0], /Ian Harake/);
  assert.match(outs[0], /Doors:/);
  const st = await run('status');
  assert.doesNotMatch(st, /Doors:/);
  assert.match(await run('look'), /Doors:/);
});

test('phone is closed before Lab Access; a picked sentence prints only the change', async () => {
  const { run } = setup();
  assert.match(await run('phone'), /no handset access/);
  assert.match(await run('s'), /^To Ian Harake:/);
  const out = await run('1');
  assert.match(out, /^Ian Harake: /m);
  assert.match(out, /\[phone\] Lab Access is active/);
  const again = await run('status');
  assert.doesNotMatch(again, /Lab Access is active/);
  assert.match(await run('phone'), /== Lab Access ==/);
});

test('go lists targets when bare; prefix and case-insensitive room match', async () => {
  const { run } = setup();
  assert.match(await run('go'), /Go where:/);
  assert.match(await run('go cour'), /Open-air Courtyard|Courtyard/);
  await run('go collab');
  assert.match(await run('look'), /Collaboration|collab/i);
});

test('open lists files when bare; prefix match on name', async () => {
  const { run } = setup();
  await run('s');
  await run('1');
  assert.match(await run('open'), /^Files:/);
  const listed = await run('files');
  assert.match(listed, /^\s+1\./m);
  const out = await run('open lab');
  assert.match(out, /^-- /);
});

test('first visit gets the full description, a revisit the short one', async () => {
  const { run } = setup();
  const first = await run('go courtyard');
  assert.match(first, /Open-air Courtyard/);
  assert.match(first, /informal conversation/);
  await run('go collab');
  const back = await run('go courtyard');
  assert.match(back, /Open-air Courtyard/);
  assert.doesNotMatch(back, /informal conversation/);
});

test('no fact text the player has not learned or thought reaches the console', async () => {
  const { s, run, outs } = setup();
  for (const line of ['s', '1', 'files', '1', 'go collab', 's', '1', 's', '2', 'go people', 's', '1', 's', '3', 'go courtyard', 'think job', 'keep', 'msg nora', '1', 'records', 'know']) await run(line);
  const text = outs.join('\n');
  for (const [id, f] of Object.entries(FACTS)) {
    if (!text.includes(f.text)) continue;
    const ok = s.learned[id] || s.assertions.some(a => a.signature === id && a.source === 'thought');
    assert.ok(ok, `console showed unlearned fact ${id}`);
  }
});
