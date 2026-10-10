import {makeParse,semanticSignature} from '../lib/grammar.mjs';

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
  {phrase:'Tell me about',patch:{kind:'ask',relation:'about',open_slot:'topic'}}
];
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
function probableNpc(state){return Object.entries(state.actors).find(([,n])=>n.room===state.room)?.[0]||'pavel'}
function candidate(phrase,parse,patch,semId=null){
  return {phrase,parse:{...parse,...patch,unfinished:'',confidence:1,source:'completion'},semanticId:semId};
}
const norm=s=>s.toLowerCase().replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
function topicCandidates(state,p,slot){
  const ids=Object.keys(state.entities);
  return ids.filter(id=> {
    const e=state.entities[id];
    if(slot==='recipient')return e.category==='actor'&&!!state.actors[id]&&state.actors[id].room===state.room;
    if(slot==='evidence')return e.category==='evidence'&&state.examined.includes(id);
    if(slot==='subject')return e.category!=='evidence'&&e.category!=='resource' || id==='shutdown_report';
    if(slot==='object'){
      if(p.relation==='has_access'||p.relation==='authorized'||p.relation==='did_use')return ['resource','topic','evidence'].includes(e.category);
      if(p.relation==='continued_after')return ['event','process'].includes(e.category);
      if(p.relation==='covers')return ['event','process','topic'].includes(e.category);
      return e.category!=='actor';
    }
    return true;
  }).map(id=> {
    const e=state.entities[id];
    let label=e.label;
    if(slot==='subject'&& /^the\s/i.test(label)&& /\b(the|that)\s*$/i.test(p._rawPrefix||''))label=label.replace(/^the\s/i,'');
    const key=slot==='evidence'?'evidence':slot==='recipient'?'recipient':slot==='subject'?'subject':slot==='object'?'object':'topic';
    const next=slot==='subject'?'relation':slot==='recipient'?'evidence':slot==='object'?'finish':slot==='evidence'?'finish':'finish';
    return {...candidate(label,p,{[key]:id,open_slot:next},id),entityId:id};
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
function score(x,state,parse,text,spoken,unfinished){
  const npc=probableNpc(state);const e=state.entities[x.entityId];
  let n=0;
  if(e?.publicRoles?.includes(npc))n+=6;
  if(e?.publicRoles?.includes('all'))n+=1;
  const t=norm(text+' '+(state.previous||[]).slice(-4).map(x=>x.text).join(' '));
  if(e && [e.label,...(e.aliases||[])].some(a=>a.length>3 && t.includes(norm(a))))n+=4;
  if(e && state.learnedFacts?.some(f=>norm(f.text).includes(norm(e.label))))n+=2;
  if(x.phrase==='NORA'||x.phrase==='the shutdown test')n+=2;
  if(x.phrase==='Can'||x.phrase==='What about'||x.phrase==='Show')n+=2;
  if(x.entityId&&e?.category==='evidence'&&state.examined.includes(x.entityId))n+=2;
  if(x.parse.open_slot==='finish'){
    const sig=semanticSignature(x.parse)+'|'+npc;
    if(state.asked.includes(sig))n-=13;
  }
  if(unfinished){
    const options=[x.phrase,...(e?.aliases||[])];
    if(options.some(s=>s.toLowerCase().startsWith(unfinished.toLowerCase())))n+=30;
  }
  return n;
}
export function getCandidates({state,parse,text}){
  if(!state||!parse)return [];
  const slot=parse.open_slot;
  const enriched={...parse,_rawPrefix:text};
  let all=[];
  if(slot==='opening')all=OPENINGS.map(x=>candidate(x.phrase,parse,x.patch));
  else if(['subject','object','recipient','topic','evidence'].includes(slot))all=topicCandidates(state,enriched,slot);
  else if(slot==='relation'){
    const cat=state.entities[parse.subject]?.category||'actor';
    let opts=relationOptions.filter(x=>x.forCats.includes(cat));
    if(parse.kind==='ask_why')opts=opts.filter(x=>x.relation!=='authorized');
    if(parse.kind==='assert'||parse.kind==='hypothesize')opts=[
      {phrase:'can access',relation:'has_access'},
      {phrase:'continued after',relation:'continued_after'},
      {phrase:'was authorized to use',relation:'authorized'},
      {phrase:'was not covered by',relation:'covers'},
      {phrase:'influenced',relation:'assigned'},
      {phrase:'differed from',relation:'differs_from'}
    ];
    all=opts.map(x=>candidate(x.phrase,parse,{relation:x.relation,open_slot:'object'}));
  }
  else if(slot==='finish') {
    const end=['ask','ask_why'].includes(parse.kind)?'?':'.';
    all=[candidate(end,parse,{open_slot:'none'})];
    if(parse.kind==='show')all.push(candidate('and ask about it',parse,{open_slot:'none'}));
    if(parse.kind==='assert'||parse.kind==='hypothesize')all.push(candidate('because',parse,{open_slot:'topic'}));
  }
  else if(slot==='none')all=[];
  // The trailing word is not a formal grammar slot; filter/suggest aliases by its prefix.
  const unfinished=parse.unfinished||((slot==='opening'||slot==='topic')?lastWord(text):'');
  if(unfinished){
    // Normalize an entity label to the surface that fits the player's own prefix.
    all=all.map(x=>{
      if(!x.entityId)return x;
      const e=state.entities[x.entityId];
      const forms=[e.label,...(e.aliases||[])];
      const form=forms.find(f=>f.toLowerCase().startsWith(unfinished.toLowerCase()))
        || forms.find(f=>f.replace(/^the\s+/i,'').toLowerCase().startsWith(unfinished.toLowerCase()));
      if(!form)return x;
      const surface=form.replace(/^the\s+/i,'');
      return {...x,phrase:surface};
    });
    const filtered=all.filter(x=>[x.phrase,...(state.entities[x.entityId]?.aliases||[])].some(v=>v.toLowerCase().startsWith(unfinished.toLowerCase())));
    if(filtered.length)all=filtered;
    else if(slot!=='opening')all=[];
  }
  const ordered=all.map((x,i)=>({...x,_score:score(x,state,parse,text,null,unfinished),_index:i})).sort((a,b)=>b._score-a._score||a._index-b._index);
  // Keep stable global ranking for Show more. Diversity is achieved by a mild category penalty.
  const chosen=[],counts={};
  while(ordered.length){
    ordered.sort((a,b)=>(b._score-(counts[state.entities[b.entityId]?.category]||0)*2)-(a._score-(counts[state.entities[a.entityId]?.category]||0)*2)||a._index-b._index);
    const item=ordered.shift();chosen.push(item);const cat=state.entities[item.entityId]?.category||item.parse.relation;counts[cat]=(counts[cat]||0)+1;
  }
  return chosen;
}
export function localPrefixParse(text){
  const clean=text.trim();
  if(!clean)return makeParse();
  const w=clean.toLowerCase();
  const match=OPENINGS.find(x=>x.phrase.toLowerCase()===w);
  if(match)return makeParse({...match.patch,source:'local'});
  // The input is just an unfinished opening: wait for more characters instead of invoking a model.
  if(clean.length<=4&&OPENINGS.some(x=>x.phrase.toLowerCase().startsWith(w)))return makeParse({open_slot:'opening',unfinished:clean,source:'local'});
  return null;
}
