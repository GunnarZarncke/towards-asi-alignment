import { ENTITIES } from './game.mjs';
import { explainGrammar, KINDS, RELATIONS, SLOT_TYPES, makeParse } from './grammar.mjs';

const PARSE_SCHEMA = {
  type:'object',additionalProperties:false,
  properties:{
    kind:{type:'string',enum:KINDS},
    relation:{type:'string',enum:Object.keys(RELATIONS)},
    subject:{type:['string','null']},object:{type:['string','null']},
    recipient:{type:['string','null']},evidence:{type:['string','null']},topic:{type:['string','null']},
    open_slot:{type:'string',enum:SLOT_TYPES},unfinished:{type:'string'},
    open_content:{type:'string'},confidence:{type:'number',minimum:0,maximum:1},source:{type:'string',enum:['llm']}
  },required:['kind','relation','subject','object','recipient','evidence','topic','open_slot','unfinished','open_content','confidence','source']
};

async function responsesRequest(system, user, format, stats, max_output_tokens=400) {
  if(!process.env.OPENAI_API_KEY || process.env.DEMO_MODE==='1')return null;
  const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),22000);
  try {
    const response=await fetch('https://api.openai.com/v1/responses',{
      method:'POST', signal:controller.signal,
      headers:{'Content-Type':'application/json','Authorization':`Bearer ${process.env.OPENAI_API_KEY}`},
      body:JSON.stringify({model:process.env.OPENAI_MODEL||'gpt-4.1-mini',store:false,
        instructions:system,input:user,max_output_tokens,
        ...(format?{text:{format:{type:'json_schema',name:'game_parse',strict:true,schema:format}}}:{})
      })
    });
    const raw=await response.text();let body;
    try{body=JSON.parse(raw)}catch{throw Error('Invalid API response')}
    if(!response.ok)throw Error(`OpenAI API ${response.status}: ${String(body?.error?.message||'error').slice(0,200)}`);
    if(stats){stats.calls++;stats.input+=body.usage?.input_tokens||0;stats.output+=body.usage?.output_tokens||0}
    const output=body.output?.flatMap(x=>x.content||[]).filter(x=>x.type==='output_text').map(x=>x.text).join('');
    if(!output)throw Error('The model returned no text.');
    return output;
  } finally {clearTimeout(timer)}
}

function demoParse(text,known){
  const clean=text.trim();const last=clean.split(/\s+/).pop()||'';
  const unfinished=/[a-z]$/i.test(clean)?last:'';
  const low=clean.toLowerCase();
  let kind='ask',relation='about',open_slot='topic',subject=null,recipient=null,topic=null;
  if(/^show\b/i.test(clean)){kind='show';open_slot='recipient';}
  else if(/^i (think|suspect|wonder)\b/i.test(clean)){kind='hypothesize';open_slot='subject';}
  else if(/^the\b/i.test(clean)){kind='assert';open_slot='subject';}
  else if(/^(can|could|does|did|has|is)\b/i.test(clean)){kind='ask';open_slot='subject';}
  else if(/^why\b/i.test(clean)){kind='ask_why';open_slot='subject';}
  const found=Object.keys(ENTITIES).filter(id=>known.includes(id) && [ENTITIES[id].label,...ENTITIES[id].aliases].some(a=>low.includes(a.toLowerCase())));
  if(found.length&&['ask','hypothesize','assert','ask_why'].includes(kind)){subject=found[0];open_slot='relation';}
  if(/\baccess\b/i.test(clean)){relation='has_access';open_slot='object';}
  if(/\babout the new per\w*$/i.test(clean)){subject=null;relation='about';open_slot='topic';}
  if(/\babout\b/i.test(clean)&&!subject){relation='about';open_slot='topic';}
  return makeParse({kind,relation,subject,recipient,topic,open_slot,unfinished,open_content:'',confidence:.60,source:'llm'});
}

function sanitizeParse(parsed,known){
  const ids=new Set(known);
  const out=makeParse();
  out.kind=KINDS.includes(parsed.kind)?parsed.kind:'unintelligible';
  out.relation=Object.hasOwn(RELATIONS,parsed.relation)?parsed.relation:'open';
  for(const key of ['subject','object','recipient','evidence','topic'])out[key]=ids.has(parsed[key])?parsed[key]:null;
  out.open_slot=SLOT_TYPES.includes(parsed.open_slot)?parsed.open_slot:'none';
  out.unfinished=String(parsed.unfinished||'').slice(0,60);
  out.open_content=String(parsed.open_content||'').slice(0,250);
  out.confidence=Math.max(0,Math.min(1,Number(parsed.confidence)||0));
  out.source='llm';return out;
}

export async function parseUtterance({text,known,history,actorId,previousParse,constructionTrace},stats){
  if(!process.env.OPENAI_API_KEY||process.env.DEMO_MODE==='1')return demoParse(text,known);
  const system=`You are a narrowly-scoped incremental SEMANTIC PARSER for a browser investigation game, NOT a conversational assistant. Output only JSON matching the schema.\n${explainGrammar()}\n\nRULES:\n1. Parse BOTH completed utterances and unfinished prefixes; preserve partial meaning. open_slot identifies the NEXT meaningful semantic constituent; unfinished is the exact trailing incomplete word if present.\n2. Ground entity IDs ONLY to the provided player-visible vocabulary. Do not invent entity IDs, facts, motives, or actions. Unknown relations become 'open' with a short open_content meaning; do NOT mark meaningful language 'unintelligible'.\n3. Treat questions, hypotheses, and claims as speech acts, NEVER as established game facts. 'Has access', 'authorized', and 'actually used' are different.\n4. Use the most recent 1-2 conversational exchanges to resolve pronouns (it, that, they, the other one) when clear. If unclear, keep a null reference or open_content. Do NOT consult hidden game state.\n5. For free-typed 'What about the new per', return ask/about, open_slot=topic, unfinished='per'.\n6. Examples: 'Does NORA have camera access?' => ask/has_access/subject=nora/object=camera_system. 'Show Pavel the job log' => show/about/recipient=pavel/evidence=job_log. 'It kept running?' after discussing job 017 => ask/continued_after/subject=job_017/object=shutdown_test.\n7. When text is grammatical but outside ontology, keep kind and relation='open' and state meaning in open_content. Reserve kind='unintelligible' for genuinely unrecoverable content.\n8. The previousParse is a HINT, not authoritative after the user edits text.`;
  const vocab=known.map(id=>({id,label:ENTITIES[id]?.label,aliases:ENTITIES[id]?.aliases})).filter(x=>x.label);
  const user=JSON.stringify({current_npc:actorId,player_visible_vocabulary:vocab,
    previous_utterances:history.slice(-4).map(x=>({speaker:x.role==='npc'?x.npc:'player',text:String(x.text).slice(0,240)})),
    partial_or_complete_utterance:text,previousParse:previousParse||null,constructionTrace:(constructionTrace||[]).slice(-8)});
  const out=await responsesRequest(system,user,PARSE_SCHEMA,stats,460);
  return sanitizeParse(JSON.parse(out),known);
}

export async function freeReply({text,parse,npcState,history},stats){
  if(!process.env.OPENAI_API_KEY||process.env.DEMO_MODE==='1'){
    return `You're asking about ${parse.open_content || 'that connection'}. I can discuss what I actually know, but I don't want to imply a conclusion from the phrasing alone.`;
  }
  const system=`You are ${npcState.name}, ${npcState.role}, an NPC in a serious research-lab mystery. ${npcState.voice}\nRespond naturally and specifically to the player's utterance. One or two sentences, max 55 words. You may express uncertainties, challenge assumptions and ask a relevant clarifying question. Stay grounded in ONLY the supplied facts and shared documents. You may discuss novel hypotheses but never assert they are true without supplied evidence. Do not invent specific system events, permissions, documents or secrets. If player is unclear, ask about concrete ambiguous referents. You are not a helpful AI assistant; speak as a person.`;
  const input=JSON.stringify({your_known_facts:npcState.facts,documents_shown_to_you:npcState.shared,conversation_topics:npcState.canDiscuss,
    previous_utterances:history.slice(-4),player_utterance:text,parsed_interpretation:parse});
  const result=await responsesRequest(system,input,null,stats,130);
  return result.trim().slice(0,700);
}
