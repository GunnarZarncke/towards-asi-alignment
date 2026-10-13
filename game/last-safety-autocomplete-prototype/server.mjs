import http from 'node:http';
import {existsSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {loadEnvFile} from 'node:process';
import {fileURLToPath} from 'node:url';
import {randomUUID} from 'node:crypto';
import {newSession,clientState,cleanParse,exportSession,importSession} from './lib/game.mjs';
import {applyAction} from './lib/world/actions.mjs';
import {terminalState} from './lib/world/terminal-host.mjs';
import {npcsInRoom} from './lib/world/npcs.mjs';
import {parseUtterance} from './lib/llm.mjs';
import {phraseLines} from './lib/phrase.mjs';
import {makeParse} from './lib/grammar.mjs';
import {createConsole} from './lib/text/console.mjs';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
for (const rel of ['../../.env', '../.env', '.env']) {
  const envPath=path.join(ROOT, rel);
  if (existsSync(envPath)) loadEnvFile(envPath, {override: true});
}
const sessions=new Map();
const consoles=new Map();
const PORT=Number(process.env.PORT||3000);
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml'};
/** Server modules the browser may import. Each is checked to hold no oracle or NPC state. */
const PUBLIC_LIB=new Set(['grammar.mjs','floorplan.mjs','world/ranking-tables.mjs']);
const CHANNELS=new Set(['person','nora','note','think']);
function json(res,status,data){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(data))}
async function body(req){let str='';for await(const chunk of req){str+=chunk;if(str.length>200_000)throw Error('Request too large')}return JSON.parse(str||'{}')}
function getSession(req,res){
  let sid=(req.headers.cookie||'').match(/(?:^|;\s*)lab_sid=([\w-]+)/)?.[1];
  if(!sid || !sessions.has(sid)){sid=randomUUID();sessions.set(sid,newSession());res.setHeader('Set-Cookie',`lab_sid=${sid}; HttpOnly; SameSite=Lax; Path=/`)}
  return {sid,s:sessions.get(sid)};
}
const both=s=>({state:clientState(s),terminal:terminalState(s)});

const server=http.createServer(async(req,res)=>{
  try{
    const url=new URL(req.url,`http://${req.headers.host||'localhost'}`);
    if(url.pathname.startsWith('/api/')){
      const {sid,s}=getSession(req,res);
      if(req.method==='GET'){
        if(url.pathname==='/api/state')return json(res,200,clientState(s));
        if(url.pathname==='/api/terminal')return json(res,200,terminalState(s));
        if(url.pathname==='/api/export'){
          res.setHeader('Content-Disposition','attachment; filename="last-safety-review-save.json"');
          return json(res,200,exportSession(s));
        }
        return json(res,405,{error:'Method not allowed'});
      }
      if(req.method!=='POST')return json(res,405,{error:'Method not allowed'});
      const b=await body(req);
      if(url.pathname==='/api/reset'){sessions.set(sid,newSession());return json(res,200,both(sessions.get(sid)))}
      if(url.pathname==='/api/import'){
        const {session,error}=importSession(b,applyAction);
        if(error)return json(res,400,{error});
        sessions.set(sid,session);return json(res,200,both(session));
      }
      if(url.pathname==='/api/go'){const r=applyAction(s,'go',{room:b.room});return json(res,r.error?400:200,{...r,...both(s)})}
      if(url.pathname==='/api/inspect'){const r=applyAction(s,'inspect',{id:b.id});return json(res,r.error?400:200,{...r,...both(s)})}
      if(url.pathname==='/api/settings'){applyAction(s,'settings',{conceptLinksEnabled:!!b.conceptLinksEnabled});return json(res,200,both(s))}
      if(url.pathname==='/api/thought'){const r=applyAction(s,'thought',{action:b.action==='note'?'note':'close'});return json(res,r.error?400:200,{...r,...both(s)})}
      if(url.pathname==='/api/text'){
        if(!consoles.has(sid))consoles.set(sid,createConsole(()=>sessions.get(sid),{phrase:true}));
        const r=await consoles.get(sid).handle(String(b.line||'').slice(0,600));
        return json(res,200,r);
      }
      if(url.pathname==='/api/tool'){
        const r=applyAction(s,'tool',b||{});
        return json(res,r.ok===false&&r.reason==='Not available on this phone.'?403:200,{result:r,...both(s)});
      }
      if(url.pathname==='/api/parse'){
        const text=String(b.text||'').slice(0,600);
        const channel=CHANNELS.has(b.channel)?b.channel:'person';
        if(!text.trim())return json(res,200,{parse:makeParse(),state:clientState(s)});
        const here=npcsInRoom(s,s.room);
        const actorId=channel==='nora'?'nora':(here.includes(b.addressee)?b.addressee:here[0]||null);
        const parse=await parseUtterance({text,known:[...s.vocab],history:s.conversations,actorId,previousParse:b.previousParse,constructionTrace:b.constructionTrace},s.usage);
        return json(res,200,{parse:cleanParse({...parse,source:'llm'},s),state:clientState(s)});
      }
      if(url.pathname==='/api/respond'){
        const text=String(b.text||'').trim().slice(0,600);
        const parse=cleanParse(b.parse,s);
        if(!text&&!['think','commit'].includes(parse.kind))return json(res,400,{error:'Empty utterance'});
        const r=applyAction(s,'respond',{parse,addressee:b.addressee||null,text});
        if(r.error)return json(res,400,{error:r.error,...both(s)});
        if(r.thought)return json(res,200,{thought:r.thought,...both(s)});
        const lines=await phraseLines(s,text,r.lines||[]);
        return json(res,200,{reply:lines.map(l=>l.text).join(' '),lines,effects:r.effects||[],parse,...(r.ending?{ending:r.ending}:{}),...both(s)});
      }
      return json(res,404,{error:'Unknown API endpoint'});
    }
    if(req.method!=='GET')return json(res,405,{error:'Only GET supported'});
    const publicPath=url.pathname==='/'?'/index.html':url.pathname;
    const threeRoot=path.join(ROOT,'node_modules','three','build');
    const libRel=publicPath.startsWith('/lib/')?publicPath.slice('/lib/'.length):'';
    let absolute;
    if(libRel){
      if(!PUBLIC_LIB.has(libRel))return json(res,404,{error:'Not public'});
      absolute=path.join(ROOT,'lib',libRel);
    }
    else if(publicPath.startsWith('/vendor/three/'))absolute=path.resolve(threeRoot,`.${publicPath.slice('/vendor/three'.length)}`);
    else absolute=path.resolve(ROOT,'public',`.${publicPath}`);
    if(!libRel&&!absolute.startsWith(path.join(ROOT,'public')+path.sep)&&!absolute.startsWith(threeRoot+path.sep))return json(res,403,{error:'Forbidden'});
    const data=await readFile(absolute);
    res.writeHead(200,{'Content-Type':mime[path.extname(absolute)]||'application/octet-stream','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(data);
  }catch(e){const m=String(e?.message||e);const status=m.includes('ENOENT')?404:m.includes('JSON')?400:502;json(res,status,{error:m.slice(0,280)})}
});
server.listen(PORT,'127.0.0.1',()=>console.log(`Last Safety Review prototype: http://127.0.0.1:${PORT} (${process.env.OPENAI_API_KEY&&process.env.DEMO_MODE!=='1'?'live':'demo'})`));
