import test from 'node:test';
import assert from 'node:assert/strict';
import {makeParse,semanticSignature} from '../lib/grammar.mjs';
import {newSession,clientState,go,inspect,ENTITIES} from '../lib/game.mjs';
import {getCandidates,insertFragment,localPrefixParse} from '../public/grammar.js';
const fresh=()=>clientState(newSession());
test('starts with contextual openers and offers no unobserved hidden fact',()=>{
  const opts=getCandidates({state:fresh(),parse:makeParse(),text:''});
  assert.ok(opts.some(x=>x.phrase==='Can'));
  assert.ok(opts.some(x=>x.phrase==='Show'));
  assert.ok(!opts.some(x=>x.phrase.includes('17')||x.phrase.includes('surveillance')));
});
test('selected grammatical fragments build a semantically typed question',()=>{
  const state=fresh();let parse=makeParse();let text='';
  function select(name){
    const opt=getCandidates({state,parse,text}).find(o=>o.phrase===name);
    assert.ok(opt,`option ${name}, found ${getCandidates({state,parse,text}).map(x=>x.phrase).join(', ')}`);
    text=insertFragment(text,opt,parse.unfinished);parse=opt.parse;
  }
  select('Can');select('NORA');select('access');select('the camera system');select('?');
  assert.equal(text,'Can NORA access the camera system?');
  assert.equal(parse.kind,'ask');assert.equal(parse.relation,'has_access');
  assert.equal(parse.subject,'nora');assert.equal(parse.object,'camera_system');
  assert.equal(parse.open_slot,'none');
});
test('replaces the partial word and avoids duplicating an article',()=>{
  assert.equal(insertFragment('What about the new per',{phrase:'personnel policy?'},'per'),'What about the new personnel policy?');
  assert.equal(insertFragment('What about the',{phrase:'the shutdown test'},''),'What about the shutdown test');
});
test('SHOW does not complete document ids as picks',()=>{
  const s=newSession(),p=makeParse({kind:'show',open_slot:'evidence',recipient:'pavel'});
  inspect(s,'job_log');
  assert.equal(getCandidates({state:clientState(s),parse:p,text:'Show Pavel'}).some(x=>x.entityId==='job_log'),false);
});
test('Request opening is offered and topics are not evidence files',()=>{
  const opts=getCandidates({state:fresh(),parse:makeParse(),text:''});
  assert.ok(opts.some(x=>x.phrase==='Request'));
  const p=makeParse({kind:'request',relation:'about',open_slot:'topic'});
  const topics=getCandidates({state:fresh(),parse:p,text:''});
  assert.ok(topics.some(x=>x.entityId==='evaluation_records'));
  assert.ok(!topics.some(x=>x.entityId==='job_log'));
});
test('room movement and investigation reveal only justified knowledge',()=>{
  const s=newSession();s.room='platform';assert.ok(!s.vocab.includes('job_284'));
  assert.ok(inspect(s,'job_log').body);assert.ok(s.vocab.includes('job_284'));assert.ok(s.learned.job_continued);
  assert.ok(!s.learned.staffing_shift);
  assert.equal(go(s,'people').error,'No door from here.');
  assert.equal(go(s,'tech').room,'tech');
  assert.equal(go(s,'test').error,'That door needs a higher clearance.');
  go(s,'people');inspect(s,'staffing_memo');assert.ok(s.learned.staffing_shift);
});
test('Think is offered only in an empty room; File is an opening',()=>{
  const occupied=getCandidates({state:fresh(),parse:makeParse(),text:''});
  assert.ok(occupied.some(x=>x.phrase==='File'));
  assert.ok(!occupied.some(x=>x.parse.kind==='think'));
  const state=fresh();
  for (const actor of Object.values(state.actors)) actor.room='people';
  state.room='platform';
  const alone=getCandidates({state,parse:makeParse(),text:''});
  assert.ok(alone.some(x=>x.phrase==='Think' && x.parse.kind==='think'));
});
test('typed openers are recognized locally',()=>{
  assert.equal(localPrefixParse('Can').open_slot,'subject');
  assert.equal(localPrefixParse('Sho').open_slot,'opening');
  assert.equal(localPrefixParse('What about the new per'),null);
});
