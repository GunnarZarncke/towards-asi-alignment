import { ENTITIES } from './world/entities.mjs';
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

/** Plain text completion for the headless playtest player. Null in demo mode. */
export function modelText(system, user, stats, max_output_tokens=200){
  return responsesRequest(system, user, null, stats, max_output_tokens);
}

function demoParse(text, known){
  const clean=text.trim();const last=clean.split(/\s+/).pop()||'';
  const unfinished=/[a-z]$/i.test(clean)?last:'';
  const low=clean.toLowerCase();
  let kind='ask',relation='about',open_slot='topic',subject=null,recipient=null,topic=null;
  if(/^show\b/i.test(clean)){kind='show';open_slot='recipient';}
  else if(/^think\b/i.test(clean)){kind='think';open_slot='topic';}
  else if(/^(file|commit)\b/i.test(clean)){kind='commit';open_slot='topic';}
  else if(/^hold\b/i.test(clean)){kind='request';relation='suspend';open_slot='object';}
  else if(/^revoke\b/i.test(clean)){kind='request';relation='revoke';open_slot='object';}
  else if(/^run again\b/i.test(clean)){kind='request';relation='rerun';open_slot='object';}
  else if(/^stop\b/i.test(clean)){kind='request';relation='stop';open_slot='object';}
  else if(/^i (think|suspect|wonder)\b/i.test(clean)){kind='hypothesize';open_slot='subject';}
  else if(/^the\b/i.test(clean)){kind='assert';open_slot='subject';}
  else if(/^(can|could|does|did|has|is)\b/i.test(clean)){kind='ask';open_slot='subject';}
  else if(/^why\b/i.test(clean)){kind='ask_why';open_slot='subject';}
  const found=Object.keys(ENTITIES).filter(id=>known.includes(id) && [ENTITIES[id].label,...ENTITIES[id].aliases].some(a=>low.includes(a.toLowerCase())));
  if(found.length&&['ask','hypothesize','assert','ask_why'].includes(kind)){subject=found[0];open_slot='relation';}
  else if(found.length&&(kind==='think'||kind==='commit')){topic=found[0];open_slot='finish';}
  else if(found.length&&kind==='request'&&relation!=='about'){topic=found[0];open_slot='finish';}
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
  const system=`You are a narrowly-scoped incremental SEMANTIC PARSER for a browser investigation game, NOT a conversational assistant. Output only JSON matching the schema.\n${explainGrammar()}\n\nRULES:\n1. Parse BOTH completed utterances and unfinished prefixes; preserve partial meaning. open_slot identifies the NEXT meaningful semantic constituent; unfinished is the exact trailing incomplete word if present.\n2. Ground entity IDs ONLY to the provided player-visible vocabulary. Do not invent entity IDs, facts, motives, or actions. Unknown relations become 'open' with a short open_content meaning; do NOT mark meaningful language 'unintelligible'.\n3. Treat questions, hypotheses, and claims as speech acts, NEVER as established game facts. 'Has access', 'authorized', and 'actually used' are different.\n4. Use the most recent 1-2 conversational exchanges to resolve pronouns (it, that, they, the other one) when clear. If unclear, keep a null reference or open_content. Do NOT consult hidden game state.\n5. For free-typed 'What about the new per', return ask/about, open_slot=topic, unfinished='per'.\n6. Examples: 'Does NORA have camera access?' => ask/has_access/subject=nora/object=camera_system. Telling someone a claim is assert. 'Hold job 284' => request/suspend. 'Think about the report' => think. 'File the review' => commit. 'Show Pavel the job log' => show/about/recipient=pavel/evidence=job_log. 'It kept running?' after discussing job 284 => ask/continued_after/subject=job_284/object=shutdown_test.\n7. When text is grammatical but outside ontology, keep kind and relation='open' and state meaning in open_content. Reserve kind='unintelligible' for genuinely unrecoverable content.\n8. The previousParse is a HINT, not authoritative after the user edits text.`;
  const vocab=known.map(id=>({id,label:ENTITIES[id]?.label,aliases:ENTITIES[id]?.aliases})).filter(x=>x.label);
  const user=JSON.stringify({current_npc:actorId,player_visible_vocabulary:vocab,
    previous_utterances:history.slice(-4).map(x=>({speaker:x.role==='npc'?x.npc:'player',text:String(x.text).slice(0,240)})),
    partial_or_complete_utterance:text,previousParse:previousParse||null,constructionTrace:(constructionTrace||[]).slice(-8)});
  const out=await responsesRequest(system,user,PARSE_SCHEMA,stats,460);
  return sanitizeParse(JSON.parse(out),known);
}

const NUMBERS=/\b\d{1,2}:\d{2}\b|\b\d{2,}\b/g;

/** A phrasing may not add a time or number the move does not carry (O-21: the model adds no move). */
export function phrasingAdds(reply,{facts,texture,question,document,reason},template){
  const allowed=new Set([facts,texture,question,document,reason,template].flat().filter(Boolean).join(' ').match(NUMBERS)||[]);
  return (reply.match(NUMBERS)||[]).filter(x=>!allowed.has(x));
}

/**
 * Phrase one engine-chosen move. Input is phrasingInput() from game.mjs: the move, the facts it
 * carries, voice, agenda texture. Returns the template in demo mode or when the phrasing adds content.
 */
export async function freeReply({text,phrasing,template,history},stats){
  if(!process.env.OPENAI_API_KEY||process.env.DEMO_MODE==='1')return template;
  const p=phrasing;
  const social=p.move==='glue';
  const system=social
    ?`You are ${p.name}, ${p.role}, in a serious research-lab mystery. Status (Person layer): ${p.voice?.person||''} Structure: ${p.voice?.structure||''} Example: "${p.voice?.sample||''}"\nThis is a social-glue line (${p.slot||'mid'}, stance ${p.stance||'busy'}). Phrase only that courtesy or pressure. One sentence, at most 28 words. Do not add facts, events, times, numbers, permissions, documents, people, or conclusions.`
    :`You are ${p.name}, ${p.role}, in a serious research-lab mystery. Voice: ${p.voice?.structure||''} Status (Person layer): ${p.voice?.person||''} Focus: ${p.voice?.focus||''} Example of how you talk: "${p.voice?.sample||''}"\nThe engine has already chosen what you do this turn: ${p.move}. Phrase exactly that, in one or two sentences, at most 45 words. State only the supplied facts. You may keep one short social beat if the template has one. Do not add events, times, numbers, permissions, documents, people, or conclusions. If the move is withhold, give the reason without the withheld content. If refer, name only the person given. If ask, ask only the supplied question. Speak as a person, not an assistant.`;
  const input=JSON.stringify({move:p.move,facts:p.facts,reason:p.reason,refer_to:p.referTo,document:p.document,question:p.question,
    your_work_right_now:p.texture,template_wording:template,slot:p.slot,stance:p.stance,work:p.work,
    previous_utterances:history.slice(-4).map(x=>({speaker:x.role==='npc'?x.npc:'player',text:String(x.text).slice(0,240)})),player_utterance:text});
  const result=(await responsesRequest(system,input,null,stats,120))?.trim().slice(0,400);
  if(!result||phrasingAdds(result,p,template).length)return template;
  return result;
}
