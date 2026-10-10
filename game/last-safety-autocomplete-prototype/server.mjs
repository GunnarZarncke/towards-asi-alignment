import http from 'node:http';
import {existsSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {loadEnvFile} from 'node:process';
import {fileURLToPath} from 'node:url';
import {randomUUID} from 'node:crypto';
import {newSession,clientState,inspect,go,NPCS,ENTITIES,deterministicResponse,exposedNpcFacts,recordConversation} from './lib/game.mjs';
import {parseUtterance,freeReply} from './lib/llm.mjs';
import {KINDS,RELATIONS,SLOT_TYPES,makeParse} from './lib/grammar.mjs';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
for (const rel of ['../../.env', '../.env', '.env']) {
  const envPath=path.join(ROOT, rel);
  if (existsSync(envPath)) loadEnvFile(envPath, {override: true});
}
const sessions=new Map();
const PORT=Number(process.env.PORT||3000);
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml'};
function json(res,status,data){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(data))}
async function body(req){let str='';for await(const chunk of req){str+=chunk;if(str.length>50_000)throw Error('Request too large')}return JSON.parse(str||'{}')}
function getSession(req,res){
  let sid=(req.headers.cookie||'').match(/(?:^|;\s*)lab_sid=([\w-]+)/)?.[1];
  if(!sid || !sessions.has(sid)){sid=randomUUID();sessions.set(sid,newSession());res.setHeader('Set-Cookie',`lab_sid=${sid}; HttpOnly; SameSite=Lax; Path=/`)}
  return sessions.get(sid);
}
function cleanParse(p,s){
  const ids=s.playerKnows;const result=makeParse();
  if(KINDS.includes(p?.kind))result.kind=p.kind;
  if(Object.hasOwn(RELATIONS,p?.relation))result.relation=p.relation;
  for(const k of ['subject','object','recipient','evidence','topic']) result[k]=ids.has(p?.[k])?p[k]:null;
  result.open_slot=SLOT_TYPES.includes(p?.open_slot)?p.open_slot:'none';
  result.unfinished=String(p?.unfinished||'').slice(0,50);result.open_content=String(p?.open_content||'').slice(0,200);
  result.confidence=Number(p?.confidence)||0;
  result.source=String(p?.source||'completion');return result;
}
const server=http.createServer(async(req,res)=>{
  try{
    const url=new URL(req.url,`http://${req.headers.host||'localhost'}`);
    if(url.pathname.startsWith('/api/')){
      const s=getSession(req,res);
      if(url.pathname==='/api/state'&&req.method==='GET')return json(res,200,clientState(s));
      if(req.method!=='POST')return json(res,405,{error:'Method not allowed'});
      const b=await body(req);
      if(url.pathname==='/api/reset'){const replacement=newSession();Object.assign(s,replacement);return json(res,200,{state:clientState(s)})}
      if(url.pathname==='/api/go'){const result=go(s,b.room);return json(res,result.error?400:200,{...result,state:clientState(s)})}
      if(url.pathname==='/api/inspect'){const result=inspect(s,b.id);return json(res,result.error?400:200,{...result,state:clientState(s)})}
      if(url.pathname==='/api/parse'){
        const text=String(b.text||'').slice(0,600);
        if(!text.trim())return json(res,200,{parse:makeParse(),state:clientState(s)});
        const actorId=Object.entries(NPCS).find(([id,x])=>x.room===s.room)?.[0];
        const parse=await parseUtterance({text,known:[...s.playerKnows],history:s.conversations,actorId,previousParse:b.previousParse,constructionTrace:b.constructionTrace},s.usage);
        return json(res,200,{parse,state:clientState(s)});
      }
      if(url.pathname==='/api/respond'){
        const text=String(b.text||'').trim().slice(0,600);
        if(!text)return json(res,400,{error:'Empty utterance'});
        const npcId=Object.entries(NPCS).find(([id,x])=>x.room===s.room)?.[0];
        const p=cleanParse(b.parse,s);
        const result=deterministicResponse(s,p,npcId);
        let reply=result.reply;
        if(!reply)reply=await freeReply({text,parse:p,npcState:exposedNpcFacts(s,npcId),history:s.conversations},s.usage);
        recordConversation(s,text,npcId,reply);
        return json(res,200,{reply,effects:result.effects,parse:p,state:clientState(s)});
      }
      return json(res,404,{error:'Unknown API endpoint'});
    }
    if(req.method!=='GET')return json(res,405,{error:'Only GET supported'});
    const publicPath=url.pathname==='/'?'/index.html':url.pathname;
    let absolute;
    const threeRoot=path.join(ROOT,'node_modules','three','build');
    if(publicPath==='/lib/grammar.mjs')absolute=path.join(ROOT,'lib','grammar.mjs');
    else if(publicPath==='/shared/game.mjs')return json(res,404,{error:'Not public'});
    else if(publicPath.startsWith('/vendor/three/'))absolute=path.resolve(threeRoot,`.${publicPath.slice('/vendor/three'.length)}`);
    else absolute=path.resolve(ROOT,'public',`.${publicPath}`);
    if(!absolute.startsWith(path.join(ROOT,'public')+path.sep)&&!absolute.startsWith(threeRoot+path.sep)&&absolute!==path.join(ROOT,'lib','grammar.mjs'))return json(res,403,{error:'Forbidden'});
    const data=await readFile(absolute);
    res.writeHead(200,{'Content-Type':mime[path.extname(absolute)]||'application/octet-stream','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(data);
  }catch(e){const m=String(e?.message||e);const status=m.includes('ENOENT')?404:m.includes('JSON')?400:502;json(res,status,{error:m.slice(0,280)})}
});
server.listen(PORT,'127.0.0.1',()=>console.log(`Last Safety Review prototype: http://127.0.0.1:${PORT} (${process.env.OPENAI_API_KEY&&process.env.DEMO_MODE!=='1'?'live':'demo'})`));
