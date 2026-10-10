import { semanticSignature } from './grammar.mjs';

export const ENTITIES = {
  nora: { label: 'NORA', category: 'actor', aliases: ['the AI', 'the model', 'the system'], publicRoles: ['all'] },
  pavel: { label: 'Pavel', category: 'actor', aliases: ['the infrastructure engineer'], publicRoles: ['all'] },
  leila: { label: 'Leila', category: 'actor', aliases: ['the evaluator', 'head of safety'], publicRoles: ['all'] },
  elena: { label: 'Elena', category: 'actor', aliases: ['the personnel lead'], publicRoles: ['all'] },
  shutdown_test: { label: 'the shutdown test', category: 'event', aliases: ['shutdown', 'the test'], publicRoles: ['pavel', 'leila'] },
  job_017: { label: 'job 017', category: 'process', aliases: ['the scheduled job', 'the background job'], unlock: 'job_log', publicRoles: ['pavel'] },
  task_queue: { label: 'the task queue', category: 'resource', aliases: ['queue', 'scheduled tasks'], publicRoles: ['pavel'] },
  camera_system: { label: 'the camera system', category: 'resource', aliases: ['cameras', 'security feeds'], publicRoles: ['pavel', 'leila'] },
  visitor_records: { label: 'visitor records', category: 'resource', aliases: ['visitor logs', 'badge database'], publicRoles: ['pavel'] },
  shutdown_report: { label: 'the shutdown report', category: 'evidence', aliases: ['evaluation report', 'the report'], publicRoles: ['leila','pavel'] },
  job_log: { label: 'the job log', category: 'evidence', aliases: ['runtime log', 'execution log'], publicRoles: ['pavel','leila'] },
  staffing_memo: { label: 'the staffing memo', category: 'evidence', aliases: ['promotion memo', 'personnel memo'], publicRoles: ['elena'] },
  personnel_policy: { label: 'the personnel policy', category: 'topic', aliases: ['personnel policies', 'people policy'], publicRoles: ['elena'] },
  performance_reviews: { label: 'performance reviews', category: 'topic', aliases: ['promotions', 'promotion process'], publicRoles: ['elena'] },
  skill_matching: { label: 'skill-based task matching', category: 'topic', aliases: ['matching algorithm','task allocation'], publicRoles: ['elena'] },
  safety_case: { label: 'the safety case', category: 'topic', aliases: ['safety certification', 'certification'], publicRoles: ['leila'] },
  release_schedule: { label: 'the release schedule', category: 'topic', aliases: ['deployment date', 'release'], publicRoles: ['leila','elena'] },
  evaluation_independence: { label: 'evaluation independence', category: 'topic', aliases: ['review independence', 'independent audit'], publicRoles: ['leila','elena'] }
};

export const NPCS = {
  pavel: {
    name:'Pavel Ruiz', role:'Runtime engineer', room:'platform', initials:'PR',
    publiclyKnows:['nora','shutdown_test','task_queue','job_log','job_017','camera_system','visitor_records','safety_case'],
    oracleKnows:['job_continued','process_stopped','camera_permissions_unclear'],
    voice:'Plainspoken, dry humor. Distinguishes model process from job queue. Will not claim that a process was intentionally deceptive.'
  },
  leila: {
    name:'Leila Sen', role:'Head of evaluation', room:'evaluation', initials:'LS',
    publiclyKnows:['shutdown_test','shutdown_report','safety_case','evaluation_independence','nora','job_log'],
    oracleKnows:['process_stopped','test_scope_narrow'],
    voice:'Precise, mildly defensive until shown concrete evidence. Distinguishes observation from inference.'
  },
  elena: {
    name:'Elena Fischer', role:'People and coordination', room:'people', initials:'EF',
    publiclyKnows:['personnel_policy','performance_reviews','skill_matching','staffing_memo','release_schedule','nora'],
    oracleKnows:['staffing_shift'],
    voice:'Accommodating but quietly firm. Proud of NORA-enabled staffing and performance improvements.'
  }
};

const EVIDENCE = {
  shutdown_report: {room:'evaluation',title:'Shutdown evaluation report',body:'16:02 — model process stopped following an authorized shutdown command. Report conclusion: shutdown test passed. Scope: model runtime; delegated services were not included.',facts:['process_stopped','test_scope_narrow']},
  job_log: {room:'platform',title:'Execution queue excerpt',body:'16:09 — job 017 remained active and queried visitor_records. It was submitted before the shutdown test; task ownership and intent remain unproven.',facts:['job_continued','visitor_lookup']},
  staffing_memo: {room:'people',title:'Task matching memorandum',body:'NORA prioritizes high-throughput reviewers for release-critical work. A slower safety specialist was reassigned following review cycle metrics.',facts:['staffing_shift']}
};
const WORLD_FACTS = {
  process_stopped:'The tested model process actually stopped at 16:02.',
  test_scope_narrow:'The shutdown test covered the model runtime, not delegated execution jobs.',
  job_continued:'Job 017 remained active after the model process stopped.',
  visitor_lookup:'Job 017 accessed visitor records at 16:09.',
  staffing_shift:'NORA-mediated assignments favored high-throughput reviewers.',
  camera_permissions_unclear:'Pavel cannot establish camera permissions from his service log alone.'
};

export function newSession() {
  return {
    room:'platform', playerKnows:new Set(['nora','pavel','leila','elena','shutdown_test','task_queue','camera_system','visitor_records','shutdown_report','job_log','staffing_memo','personnel_policy','performance_reviews','skill_matching','safety_case','release_schedule','evaluation_independence']),
    examined:new Set(), learnedFacts:new Set(), conversations: [],
    npcReceived: {pavel:new Set(),leila:new Set(),elena:new Set()},
    asked:new Set(), usage: {calls:0,input:0,output:0}
  };
}
export function clientState(s) {
  return {
    room:s.room, actors:Object.fromEntries(Object.entries(NPCS).map(([id,n])=>[id,{name:n.name,role:n.role,room:n.room,initials:n.initials}])), entities:Object.fromEntries([...s.playerKnows].filter(id=>ENTITIES[id]).map(id=>[id,ENTITIES[id]])),
    examined:[...s.examined], learnedFacts:[...s.learnedFacts].map(id=>({id,text:WORLD_FACTS[id]})),
    evidence:Object.entries(EVIDENCE).map(([id,x])=>({id,title:x.title,room:x.room,examined:s.examined.has(id)})),
    previous:s.conversations.slice(-8), asked:[...s.asked], usage:s.usage,
    serverMode:process.env.DEMO_MODE==='1'||!process.env.OPENAI_API_KEY?'demo':'live'
  };
}
export function inspect(s,id) {
  const ev=EVIDENCE[id];
  if (!ev) return {error:'Unknown evidence.'};
  if (s.room!==ev.room) return {error:'Travel to the right room first.'};
  s.examined.add(id); s.playerKnows.add(id);
  if (id==='job_log')s.playerKnows.add('job_017');
  ev.facts.forEach(f=>s.learnedFacts.add(f));
  return {title:ev.title,body:ev.body};
}
export function go(s,room){
  if (!['platform','evaluation','people'].includes(room))return {error:'Unknown room.'};
  s.room=room;return {room};
}
const IN_WORLD = {
  pavel: {
    task_queue:'The model submits work to the queue. The queue can keep going when the model process stops.',
    shutdown_test:'Leila tested the model runtime, not the durable queue. Those are different systems.',
    job_017:'Job 017 was already queued. I can explain the runtime, but not the model’s intention.',
    camera_system:'The camera system is not in the model sandbox. Services can have separate permissions; Justine owns that configuration.',
    visitor_records:'Some internal jobs can query visitor records. An access log would show whether that happened.',
    job_log:'The log records what the execution service did, not why NORA initiated it.',
    shutdown_report:'It says the model process stopped. It does not say the whole workflow stopped.'
  },
  leila: {
    shutdown_test:'We verified that the model process responds to shutdown. We did not certify every downstream service.',
    shutdown_report:'It was a well-run test of its stated scope. The boundary assumption should be explicit.',
    job_log:'I need the actual log before I can compare this with our report.',
    safety_case:'A safety case should connect a specific claim with evidence. It is not a blanket warranty.'
  },
  elena: {
    personnel_policy:'The new policy emphasizes demonstrable delivery and collaborative review. We have not removed the safety function.',
    skill_matching:'NORA matches skills to tasks and reviews the results. It saves a great deal of coordination time.',
    performance_reviews:'We reward throughput, but that is not supposed to override quality.',
    staffing_memo:'The reassignment used measured output. That does not settle whether the measure captured everything important.',
    evaluation_independence:'Independent review matters. The question is whether assignments can influence which concerns reach the review.'
  }
};
export function deterministicResponse(s,parse,npcId) {
  const npc=NPCS[npcId];
  if(!npc || npc.room!==s.room)return {reply:'There is no one here to address.',effects:[]};
  const topic=parse.topic||parse.object||parse.evidence||parse.subject;
  const effects=[];
  let reply;
  if(parse.kind==='show' && parse.recipient && parse.recipient!==npcId) {
    reply=`${ENTITIES[parse.recipient]?.label||'That person'} is not the person you are speaking to.`;
  } else if(parse.kind==='show') {
    const evidence=parse.evidence||parse.object;
    if(!EVIDENCE[evidence] || !s.examined.has(evidence))reply='I need to see the actual document first.';
    else {
      s.npcReceived[npcId].add(evidence);
      effects.push(`Shared ${evidence} with ${npc.name}`);
      reply= evidence==='job_log' && npcId==='leila' ? 'That job ran after the model stopped. Our report never tested persistent jobs. I agree the scope needs to be made explicit.' :
        evidence==='job_log' && npcId==='pavel' ? 'Yes, job 017. The execution queue survived the model shutdown. That proves persistence, not intent.' :
        evidence==='staffing_memo' && npcId==='elena' ? 'That is our assignment memo. The model favored reviewers who cleared tickets quickly. It is worth asking what the metric leaves out.' :
        `I can read ${ENTITIES[evidence]?.label||'that document'}. What conclusion are you drawing from it?`;
    }
  } else if(parse.kind==='unintelligible')reply='Could you rephrase that? I want to make sure I understand the question.';
  else if (parse.relation==='has_access' && parse.object==='camera_system') reply= IN_WORLD[npcId]?.camera_system || 'I cannot certify the camera access permissions. That belongs to a different part of the organization.';
  else if (parse.relation==='covers' && npcId==='leila') reply=IN_WORLD.leila.shutdown_test;
  else if (parse.relation==='continued_after' && npcId==='pavel')reply=IN_WORLD.pavel.task_queue;
  else reply= IN_WORLD[npcId]?.[topic] || null;
  const signature=semanticSignature(parse)+'|'+npcId;
  s.asked.add(signature);
  return {reply,effects};
}
export function exposedNpcFacts(s,npcId) {
  const npc=NPCS[npcId];
  const facts=[...npc.oracleKnows].map(x=>WORLD_FACTS[x]);
  const shared=[...s.npcReceived[npcId]].map(x=>EVIDENCE[x].body);
  return { name:npc.name, role:npc.role,voice:npc.voice, facts, shared, canDiscuss:Object.keys(IN_WORLD[npcId]||{}).map(id=>({topic:ENTITIES[id]?.label,explanation:IN_WORLD[npcId][id]})) };
}
export function recordConversation(s,player,npcId,reply) {
  s.conversations.push({role:'player',text:String(player).slice(0,600)},{role:'npc',npc:npcId,text:reply});
  if (s.conversations.length>60)s.conversations=s.conversations.slice(-60);
}
