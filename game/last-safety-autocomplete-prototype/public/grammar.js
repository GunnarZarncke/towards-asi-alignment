import {makeParse,semanticSignature} from '../lib/grammar.mjs';
import {DOMAINS,RELATED_DOMAINS,UBIQUITOUS} from '../lib/world/ranking-tables.mjs';

/** O-19 knobs (spec/ranking.md "Configurable defaults"). Playtests move these, not the procedure. */
export const RANKING=Object.freeze({
  COST:Object.freeze({ref:1,comention:1,role:0,domain:0,related:1,group:2,lab:3}),
  EVENT_TIME_SCALE:15,
  DISCOVERY_TIME_SCALE:3,
  MAX_DISTANCE:3,
  WEIGHT:Object.freeze({parse:1,focus:.9,request:.9,turn1:.8,turn2:.55,recent:.6,role:.45}),
  RECENT_DISCOVERY_VALUES:3,
  GENERIC_PRIOR:.05,
  DIVERSITY_BONUS:.15,
  PAGE_SIZE:5,
});

const OPENINGS=[
  {phrase:'Can',patch:{kind:'ask',relation:'about',open_slot:'subject'}},
  {phrase:'Does',patch:{kind:'ask',relation:'about',open_slot:'subject'}},
  {phrase:'What about',patch:{kind:'ask',relation:'about',open_slot:'topic'}},
  {phrase:'Show',patch:{kind:'show',relation:'about',open_slot:'recipient'}},
  {phrase:'The',patch:{kind:'assert',relation:'about',open_slot:'subject'}},
  {phrase:'I think',patch:{kind:'hypothesize',relation:'about',open_slot:'subject'}},
  {phrase:'Why did',patch:{kind:'ask_why',relation:'about',open_slot:'subject'}},
  {phrase:'Has',patch:{kind:'ask',relation:'about',open_slot:'subject'}},
  {phrase:'Is',patch:{kind:'ask',relation:'about',open_slot:'subject'}},
  {phrase:'Could',patch:{kind:'ask',relation:'about',open_slot:'subject'}},
  {phrase:'Tell me about',patch:{kind:'ask',relation:'about',open_slot:'topic'}},
  {phrase:'Request',patch:{kind:'request',relation:'about',open_slot:'topic'}},
  {phrase:'Hold',patch:{kind:'request',relation:'suspend',open_slot:'object'}},
  {phrase:'Revoke',patch:{kind:'request',relation:'revoke',open_slot:'object'}},
  {phrase:'Run again',patch:{kind:'request',relation:'rerun',open_slot:'object'}},
  {phrase:'Stop',patch:{kind:'request',relation:'stop',open_slot:'object'}},
  {phrase:'Think',patch:{kind:'think',relation:'about',open_slot:'topic'}},
  {phrase:'File',patch:{kind:'commit',relation:'about',open_slot:'topic'}}
];
const CHANNEL_KINDS={
  person:null,
  nora:new Set(['ask','ask_why','show','request','assert','hypothesize']),
  note:new Set(['assert','hypothesize']),
  think:new Set(['think']),
};
const relationOptions=[
  {phrase:'access',relation:'has_access',forCats:['actor','process']},
  {phrase:'have access to',relation:'has_access',forCats:['actor','process']},
  {phrase:'know about',relation:'knows',forCats:['actor']},
  {phrase:'continue after',relation:'continued_after',forCats:['actor','process']},
  {phrase:'cover',relation:'covers',forCats:['event','evidence','topic']},
  {phrase:'cause',relation:'caused',forCats:['actor','event','process']},
  {phrase:'use',relation:'did_use',forCats:['actor','process']},
  {phrase:'authorize',relation:'authorized',forCats:['actor']},
  {phrase:'influence',relation:'assigned',forCats:['actor']},
  {phrase:'differ from',relation:'differs_from',forCats:['event','evidence','topic','process']}
];
const ASSERT_RELATIONS=[
  {phrase:'can access',relation:'has_access'},
  {phrase:'continued after',relation:'continued_after'},
  {phrase:'was authorized to use',relation:'authorized'},
  {phrase:'was not covered by',relation:'covers'},
  {phrase:'influenced',relation:'assigned'},
  {phrase:'differed from',relation:'differs_from'}
];
const REF_FIELDS=['subject','object','recipient','evidence','topic'];
const present=a=>a&&a.presence!=='absent'&&a.room;
const HI_PATCH={kind:'social',relation:'open',open_slot:'none'};
function presentAddressees(state,addressees){
  return (addressees||[]).filter(id=>{
    const a=state.actors?.[id];
    return a&&a.presence!=='absent'&&a.room===state.room;
  });
}
/** One social opener: first in-room talk this stay, or nothing else matches (O-19). */
function hiEligible({state,parse,channel,addressees,rowCount}){
  if(parse.kind==='social')return false;
  if(channel!=='person')return false;
  const here=presentAddressees(state,addressees);
  if(!here.length)return false;
  const firstContact=here.some(id=>!state.actors[id].spokeSinceArrive);
  return firstContact||rowCount===0;
}
function maybeHi({state,parse,channel,addressees,rows}){
  if(!hiEligible({state,parse,channel,addressees,rowCount:rows.length}))return rows;
  if(rows.some(r=>r.phrase==='Hi'&&r.parse.kind==='social'))return rows;
  return [...rows,hiCandidate(parse)];
}
function hiCandidate(parse){
  return {...candidate('Hi',parse,HI_PATCH),patch:HI_PATCH};
}

function candidate(phrase,parse,patch,semId=null){
  return {phrase,parse:{...parse,...patch,unfinished:'',confidence:1,source:'completion'},semanticId:semId};
}
function topicCandidates(state,p,slot,addressees){
  const ids=Object.keys(state.entities);
  return ids.filter(id=> {
    const e=state.entities[id];
    if(slot==='recipient')return e.category==='actor'&&addressees.includes(id);
    if(slot==='evidence')return false;
    if(slot==='subject'){
      if(e.category==='actor'&&/\bthe\s*$/i.test(p._rawPrefix||''))return false;
      return e.category!=='evidence'&&e.category!=='resource';
    }
    if(slot==='object'){
      if(id===p.subject)return false;
      if(p.relation==='has_access'||p.relation==='authorized'||p.relation==='did_use')return ['resource','topic'].includes(e.category);
      if(p.relation==='continued_after')return ['event','process'].includes(e.category);
      if(p.relation==='covers')return ['event','process','topic'].includes(e.category);
      if(p.relation==='suspend'||p.relation==='stop'||p.relation==='rerun')return ['process','event','topic'].includes(e.category);
      if(p.relation==='revoke')return ['process','resource','topic'].includes(e.category);
      return e.category!=='actor'&&e.category!=='evidence';
    }
    if(slot==='topic' && p.kind==='think')return true;
    if(slot==='topic')return e.category!=='evidence';
    return true;
  }).map(id=> {
    const e=state.entities[id];
    let label=e.label;
    if(slot==='subject'&& /^the\s/i.test(label)&& /\b(the|that)\s*$/i.test(p._rawPrefix||''))label=label.replace(/^the\s/i,'');
    const next=slot==='subject'?'relation':'finish';
    return {...candidate(label,p,{[slot]:id,open_slot:next},id),entityId:id};
  });
}
function lastWord(text){return (text.match(/[A-Za-z][\w-]*$/)||[])[0]||''}
export function insertFragment(text,option,unfinished){
  let prefix=String(unfinished||'');
  const trimmed=text.trimEnd();
  const typedEnd=lastWord(trimmed);
  if(prefix && typedEnd.toLowerCase()!==prefix.toLowerCase())prefix='';
  const matches=prefix && option.phrase.toLowerCase().startsWith(prefix.toLowerCase());
  if(matches){return trimmed.slice(0,trimmed.length-prefix.length)+option.phrase;}
  if(!trimmed)return option.phrase;
  if(/\bthe$/i.test(trimmed) && /^the\s+/i.test(option.phrase))return trimmed+' '+option.phrase.replace(/^the\s+/i,'');
  if(/^[?.!,;]/.test(option.phrase))return trimmed+option.phrase;
  return trimmed+' '+option.phrase;
}

// ---------- virtual graph (built per call, discarded) ----------

const dom=d=>`d:${d}`;
const isDomain=n=>n.startsWith('d:');

function buildGraph(state,cfg){
  const C=cfg.COST;
  const facts=Object.fromEntries((state.learnedFacts||[]).map(f=>[f.id,f]));
  const entityIds=Object.keys(state.entities||{});
  const factIds=Object.keys(facts);
  const items=new Set([...entityIds,...factIds]);
  const ubiq=new Set(UBIQUITOUS);
  const refsOf=n=>facts[n]?facts[n].refs.filter(r=>state.entities[r]):[];
  const domainsOf=n=>{
    if(ubiq.has(n))return [];
    if(state.entities[n])return state.entities[n].domains||[];
    if(facts[n])return [...new Set(refsOf(n).filter(r=>!ubiq.has(r)).flatMap(r=>state.entities[r].domains||[]))];
    return [];
  };
  const factsRef={};
  for(const f of factIds)for(const r of refsOf(f))(factsRef[r]??=[]).push(f);
  const byDomain={};
  for(const n of items)for(const d of domainsOf(n))(byDomain[d]??=[]).push(n);
  const roleRows=(state.roleDomains||[]).filter(r=>(state.introduced||[]).includes(r.id));
  const roleOf=Object.fromEntries(roleRows.map(r=>[r.id,r.domains]));
  const turns=(state.previous||[]).slice(-2).map(t=>(t.refs||[]).filter(r=>items.has(r)));
  const eventAt=n=>state.entities[n]?.eventAt??facts[n]?.eventAt??null;
  const discoveredAt=n=>state.entities[n]?(state.discoveredAt||{})[n]??null:facts[n]?.discoveredAt??null;
  const temporal=(a,b)=>{
    const costs=[];
    const ea=eventAt(a),eb=eventAt(b);
    if(ea!=null&&eb!=null)costs.push(Math.abs(ea-eb)/cfg.EVENT_TIME_SCALE);
    const da=discoveredAt(a),db=discoveredAt(b);
    if(da!=null&&db!=null)costs.push(Math.abs(da-db)/cfg.DISCOVERY_TIME_SCALE);
    return costs.length?Math.min(...costs):null;
  };
  /** Ids that share a specific context with n: an authored ref, a non-ubiquitous shared entity, or a domain. */
  const contexts=n=>{
    const out=new Set();
    if(facts[n])for(const r of refsOf(n)){out.add(r);if(!ubiq.has(r))for(const f of factsRef[r]||[])out.add(f);}
    if(state.entities[n])for(const f of factsRef[n]||[])out.add(f);
    for(const d of domainsOf(n))for(const m of byDomain[d]||[])out.add(m);
    out.delete(n);
    return out;
  };
  function neighbors(n){
    const out=[];
    if(isDomain(n)){
      const d=n.slice(2);
      for(const m of byDomain[d]||[])out.push([m,C.domain]);
      for(const [id,ds] of Object.entries(roleOf))if(ds.includes(d)&&items.has(id))out.push([id,C.role]);
      for(const [a,b] of RELATED_DOMAINS){if(a===d)out.push([dom(b),C.related]);if(b===d)out.push([dom(a),C.related]);}
      for(const x of Object.keys(DOMAINS))if(x!==d&&DOMAINS[x]===DOMAINS[d])out.push([dom(x),C.group]);
      return out;
    }
    for(const d of domainsOf(n))out.push([dom(d),C.domain]);
    for(const d of roleOf[n]||[])out.push([dom(d),C.role]);
    if(facts[n]){
      const refs=refsOf(n);
      for(const r of refs)out.push([r,C.ref]);
    }
    for(const f of factsRef[n]||[]){
      out.push([f,C.ref]);
      for(const r of refsOf(f))if(r!==n)out.push([r,C.ref]);
    }
    for(const t of turns)if(t.includes(n))for(const m of t)if(m!==n)out.push([m,C.comention]);
    for(const m of contexts(n)){const c=temporal(n,m);if(c!=null)out.push([m,c]);}
    for(const m of items)if(m!==n)out.push([m,C.lab]);
    return out;
  }
  const temporalEdge=(a,b)=>contexts(a).has(b)?temporal(a,b):null;
  return {neighbors,temporalEdge,ubiq,has:n=>isDomain(n)?!!DOMAINS[n.slice(2)]:items.has(n)};
}

/** Cost of the temporal edge between two nodes, or null when they share no specific context. */
export function temporalEdge(state,a,b,cfg=RANKING){
  return buildGraph(state,cfg).temporalEdge(a,b);
}

function shortest(graph,source,max){
  const dist=new Map([[source,0]]);
  const done=new Set();
  const frontier=[[0,source]];
  while(frontier.length){
    frontier.sort((a,b)=>a[0]-b[0]);
    const [d,u]=frontier.shift();
    if(done.has(u))continue;
    done.add(u);
    if(u!==source&&graph.ubiq.has(u))continue;
    for(const [v,c] of graph.neighbors(u)){
      const nd=d+c;
      if(nd>max||nd>=(dist.get(v)??Infinity))continue;
      dist.set(v,nd);frontier.push([nd,v]);
    }
  }
  return dist;
}

function anchorsOf(state,parse,addressees,cfg){
  const W=cfg.WEIGHT,out=new Map();
  const add=(id,w)=>{if(id&&w>(out.get(id)||0))out.set(id,w)};
  const known=id=>!!state.entities?.[id]||(state.learnedFacts||[]).some(f=>f.id===id);
  for(const k of REF_FIELDS)if(known(parse[k]))add(parse[k],W.parse);
  const focus=(state.examined||[]).at(-1);
  if(known(focus))add(focus,W.focus);
  const turns=(state.previous||[]).slice(-2);
  if(parse.kind==='request'){
    for(const t of turns)for(const r of t.refs||[])if(state.entities?.[r]?.category==='evidence')add(r,W.request);
  }
  for(const r of turns.at(-1)?.refs||[])if(known(r))add(r,W.turn1);
  if(turns.length>1)for(const r of turns[0].refs||[])if(known(r))add(r,W.turn2);
  const disc=state.discoveredAt||{};
  const latest=[...new Set(Object.values(disc))].sort((a,b)=>b-a).slice(0,cfg.RECENT_DISCOVERY_VALUES);
  for(const [id,at] of Object.entries(disc))if(latest.includes(at)&&known(id))add(id,W.recent);
  const rows=(state.roleDomains||[]).filter(r=>addressees.includes(r.id)&&(state.introduced||[]).includes(r.id));
  for(const d of new Set(rows.flatMap(r=>r.domains)))add(dom(d),W.role);
  return out;
}

/** Shortest virtual-graph distances from one node, for tests and playtest tuning. */
export function distancesFrom(state,source,cfg=RANKING){
  return shortest(buildGraph(state,cfg),source,cfg.MAX_DISTANCE);
}

/** R(v) = max over anchors of w · 2^-d(a,v), within MAX_DISTANCE. */
export function relevance(state,parse,addressees=[],cfg=RANKING){
  const graph=buildGraph(state,cfg);
  const R=new Map();
  for(const [a,w] of anchorsOf(state,parse,addressees,cfg)){
    if(!graph.has(a))continue;
    for(const [v,d] of shortest(graph,a,cfg.MAX_DISTANCE)){
      const r=w*2**-d;
      if(r>(R.get(v)||0))R.set(v,r);
    }
  }
  return R;
}

// ---------- selection ----------

function referents(x){return REF_FIELDS.map(k=>x.patch?.[k]).filter(Boolean)}
function branchOf(x,slot,state){
  if(slot==='opening')return `k:${x.parse.kind}`;
  if(slot==='relation')return `r:${x.parse.relation}`;
  if(slot==='finish')return `f:${x.parse.open_slot}`;
  const e=state.entities[x.entityId];
  return e?.domains?.[0]?`d:${e.domains[0]}`:`c:${e?.category||'none'}`;
}
function actionOf(x,slot,parse){
  if(slot==='finish')return `${x.parse.kind}|finish`;
  if(slot==='opening'){
    const rel=x.patch.relation&&x.patch.relation!=='about'?x.patch.relation:(parse.relation&&parse.relation!=='about'?parse.relation:'about');
    return `${x.parse.kind}|${rel}`;
  }
  return `${x.parse.kind}|${x.parse.relation}`;
}
function omitted(x,omit){
  return omit.some(o=>o.phrase===x.phrase||(o.parse&&x.parse.kind===o.parse.kind&&x.parse.relation===o.parse.relation&&x.parse.open_slot!=='opening'&&x.patch?.relation===o.parse.relation));
}

/** Openings that answer an NPC's open question in this channel (O-46). */
function replyOpenings(state,parse,addressees){
  const q=state.pendingQuestion;
  if(!q||!addressees.includes(q.npc))return [];
  const ref=REF_FIELDS.map(k=>q.parse?.[k]).find(id=>state.entities?.[id]);
  const name=state.actors?.[q.npc]?.name?.split(' ')[0]||q.npc;
  const out=[];
  const specific=ref&&q.parse.relation&&q.parse.relation!=='about';
  if(specific)out.push({phrase:`Tell ${name} ${state.entities[ref].label}`,patch:{kind:'assert',subject:ref,open_slot:'relation'}});
  else out.push({phrase:`Tell ${name}`,patch:{kind:'assert',open_slot:'subject'}});
  out.push({phrase:`Show ${name}`,patch:{kind:'show',relation:'about',recipient:q.npc,open_slot:'finish'}});
  return out;
}

/**
 * Ordered completions (spec/ranking.md). Reads only its arguments: the player projection, the
 * parse, the typed text, the addressees, the channel, and the engine's omit list for NORA.
 */
export function getCandidates({state,parse,text='',addressees,channel='person',omit=[],config=RANKING}){
  if(!state||!parse)return [];
  const cfg=config;
  const who=addressees??Object.entries(state.actors||{}).filter(([,a])=>present(a)&&a.room===state.room).map(([id])=>id);
  const slot=parse.open_slot;
  const enriched={...parse,_rawPrefix:text};
  let rows=[];
  if(slot==='opening'){
    const allowed=CHANNEL_KINDS[channel]||null;
    const someoneHere=Object.values(state.actors||{}).some(a=>present(a)&&a.room===state.room);
    const base=[...replyOpenings(state,parse,who),...OPENINGS].filter(x=>{
      if(allowed&&!allowed.has(x.patch.kind))return false;
      if(x.patch.kind==='think')return !someoneHere&&(channel==='person'||channel==='think');
      if(x.patch.kind==='commit')return channel==='person';
      return true;
    });
    rows=base.map(x=>({...candidate(x.phrase,parse,x.patch),patch:x.patch}));
  }
  else if(REF_FIELDS.includes(slot))rows=topicCandidates(state,enriched,slot,who).map(x=>({...x,patch:{[slot]:x.entityId}}));
  else if(slot==='relation'){
    const cat=state.entities[parse.subject]?.category||'actor';
    let opts=relationOptions.filter(x=>x.forCats.includes(cat));
    if(parse.kind==='ask_why')opts=opts.filter(x=>x.relation!=='authorized');
    if(parse.kind==='assert'||parse.kind==='hypothesize')opts=ASSERT_RELATIONS;
    rows=opts.map(x=>({...candidate(x.phrase,parse,{relation:x.relation,open_slot:'object'}),patch:{relation:x.relation}}));
  }
  else if(slot==='finish') {
    const end=['ask','ask_why'].includes(parse.kind)?'?':'.';
    rows=[{...candidate(end,parse,{open_slot:'none'}),patch:{}}];
    if(parse.kind==='show')rows.push({...candidate('and ask about it',parse,{open_slot:'none'}),patch:{}});
    if(parse.kind==='assert'||parse.kind==='hypothesize')rows.push({...candidate('because',parse,{open_slot:'topic'}),patch:{}});
  }
  if(channel==='nora'&&omit.length)rows=rows.filter(x=>!omitted(x,omit));
  const typedTail=parse.source!=='completion'&&(slot==='opening'||slot==='topic')&&!/\s$/.test(text);
  const unfinished=parse.unfinished||(typedTail?lastWord(text):'');
  if(unfinished){
    const u=unfinished.toLowerCase();
    rows=rows.map(x=>{
      if(!x.entityId)return x;
      const e=state.entities[x.entityId];
      const forms=[e.label,...(e.aliases||[])];
      const form=forms.find(f=>f.toLowerCase().startsWith(u))||forms.find(f=>f.replace(/^the\s+/i,'').toLowerCase().startsWith(u));
      return form?{...x,phrase:form.replace(/^the\s+/i,''),_matched:true}:x;
    }).map(x=>x._matched||x.phrase.toLowerCase().startsWith(u)?{...x,_matched:true}:x);
    rows=rows.filter(x=>x._matched);
  }
  const seen=new Map();
  for(const x of rows){
    const sig=semanticSignature(x.parse)+'|'+x.parse.open_slot;
    if(!seen.has(sig))seen.set(sig,x);
  }
  rows=[...seen.values()];
  if(slot==='opening')rows=maybeHi({state,parse,channel,addressees,rows});
  if(slot==='opening'&&!text.trim())return rows.map(strip);
  const R=relevance(state,parse,who,cfg);
  const scored=rows.map((x,i)=>{
    const refs=referents(x);
    const score=refs.length?Math.max(0,...refs.map(id=>R.get(id)||0)):cfg.GENERIC_PRIOR;
    return {...x,_score:score,_index:i,_branch:branchOf(x,slot,state),_action:actionOf(x,slot,parse)};
  });
  const chosen=[];
  const branches=new Set(),actions=new Set();
  while(scored.length){
    let best=0,bestValue=-Infinity;
    scored.forEach((x,i)=>{
      const bonus=!branches.has(x._branch)&&!actions.has(x._action)?cfg.DIVERSITY_BONUS:0;
      const v=x._score+bonus;
      if(v>bestValue+1e-12){best=i;bestValue=v;}
    });
    const [x]=scored.splice(best,1);
    branches.add(x._branch);actions.add(x._action);
    chosen.push(x);
  }
  return chosen.map(strip);
}
function strip(x){
  const {patch,_matched,...rest}=x;
  return rest;
}
export function localPrefixParse(text){
  const clean=text.trim();
  if(!clean)return makeParse();
  const w=clean.toLowerCase();
  if(w==='hi'||w==='hello')return makeParse({...HI_PATCH,source:'local'});
  const match=OPENINGS.find(x=>x.phrase.toLowerCase()===w);
  if(match)return makeParse({...match.patch,source:'local'});
  if(clean.length<=4&&OPENINGS.some(x=>x.phrase.toLowerCase().startsWith(w)))return makeParse({open_slot:'opening',unfinished:clean,source:'local'});
  return null;
}
