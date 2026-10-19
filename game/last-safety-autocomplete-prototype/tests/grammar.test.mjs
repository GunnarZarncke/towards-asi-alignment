import test from 'node:test';
import assert from 'node:assert/strict';
import {makeParse,semanticSignature} from '../lib/grammar.mjs';
import {newSession,clientState,go,inspect,ENTITIES} from '../lib/game.mjs';
import {getCandidates,insertFragment,localPrefixParse} from '../public/grammar.js';
import {P,say,startedSession,walk} from './helpers.mjs';
const fresh=()=>clientState(newSession());
const hereIds=state=>Object.entries(state.actors).filter(([,a])=>a.room===state.room&&a.presence!=='absent').map(([id])=>id);
const personOpen=(state,parse=makeParse(),text='')=>getCandidates({state,parse,text,addressees:hereIds(state),channel:'person'});
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
  select('Can');select('Ian');select('know about');select('the review');select('?');
  assert.equal(text,'Can Ian know about the review?');
  assert.equal(parse.kind,'ask');assert.equal(parse.relation,'knows');
  assert.equal(parse.subject,'ian');assert.equal(parse.object,'review');
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
test('Request opening is offered; unseen systems are not topics',()=>{
  const opts=getCandidates({state:fresh(),parse:makeParse(),text:''});
  assert.ok(opts.some(x=>x.phrase==='Request'));
  const p=makeParse({kind:'request',relation:'about',open_slot:'topic'});
  const topics=getCandidates({state:fresh(),parse:p,text:''});
  assert.ok(topics.some(x=>x.entityId==='review' || x.entityId==='nora'));
  assert.ok(!topics.some(x=>x.entityId==='evaluation_records' || x.entityId==='camera_system' || x.entityId==='task_queue' || x.entityId==='job_log'));
});
test('room movement and investigation reveal only justified knowledge',()=>{
  const s=startedSession();
  walk(s,'platform');
  assert.ok(!s.vocab.includes('job_284'));
  assert.ok(inspect(s,'job_log').body);
  assert.ok(s.vocab.includes('job_284'));
  assert.ok(s.learned.job_continued);
  assert.ok(!s.learned.staffing_shift);
  assert.equal(go(s,'people').error,'No door from here.');
  assert.equal(go(s,'tech').room,'tech');
  assert.equal(go(s,'test').error,'That door needs a higher clearance.');
  go(s,'people');
  inspect(s,'staffing_memo');
  assert.ok(s.learned.staffing_shift);
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
  assert.equal(localPrefixParse('Hi').kind,'social');
});
test('Hi social opener: first contact, not when already social or after talking',()=>{
  const state=fresh();
  assert.ok(personOpen(state).some(x=>x.phrase==='Hi'&&x.parse.kind==='social'));
  const social=makeParse({kind:'social',relation:'open',open_slot:'none'});
  assert.ok(!personOpen(state,social).some(x=>x.phrase==='Hi'));
  const s=startedSession();
  walk(s,'platform');
  assert.ok(personOpen(clientState(s)).some(x=>x.phrase==='Hi'),'first talk with Pavel this stay');
  say(s,'pavel',P('social','open'),'Hi.');
  const afterTalk=clientState(s);
  assert.ok(!personOpen(afterTalk).some(x=>x.phrase==='Hi'),'after a line to Pavel, only epistemic openings');
  const stuck=personOpen(afterTalk,makeParse({source:'local'}),'zzzz');
  assert.ok(stuck.some(x=>x.phrase==='Hi'),'no prefix match falls back to Hi');
  assert.ok(!getCandidates({state:afterTalk,parse:makeParse(),text:'',addressees:['nora'],channel:'nora'}).some(x=>x.phrase==='Hi'));
});
