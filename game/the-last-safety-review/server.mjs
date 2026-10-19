import http from 'node:http';
import {existsSync,readdirSync,readFileSync} from 'node:fs';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import {loadEnvFile} from 'node:process';
import {fileURLToPath} from 'node:url';
import {randomUUID,createHash} from 'node:crypto';
import {newSession,clientState,cleanParse,exportSession,importSession} from './lib/game.mjs';
import {applyAction} from './lib/world/actions.mjs';
import {terminalState,handsetMediaPayload} from './lib/world/terminal-host.mjs';
import {npcsInRoom} from './lib/world/npcs.mjs';
import {parseUtterance,preparePlayerUtterance} from './lib/llm.mjs';
import {phraseLines} from './lib/phrase.mjs';
import {makeParse} from './lib/grammar.mjs';
import {createConsole} from './lib/text/console.mjs';
import {tabCompleteLines} from './lib/text/tab-complete.mjs';
import {initTelemetryLog,appendTelemetryRow,playTelemetry} from './lib/telemetry.mjs';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
initTelemetryLog();
for (const rel of ['../../.env', '../.env', '.env']) {
  const envPath=path.join(ROOT, rel);
  if (existsSync(envPath)) loadEnvFile(envPath, {override: true});
}
const sessions=new Map();
const consoles=new Map();
const lastSeen=new Map();
const PORT=Number(process.env.PORT||3000);
/** Idle sessions are dropped after this long (all state is in memory). */
const SESSION_TTL_MS=Number(process.env.SESSION_TTL_HOURS||6)*3_600_000;
setInterval(()=>{
  const cutoff=Date.now()-SESSION_TTL_MS;
  for(const [sid,t] of lastSeen)if(t<cutoff){lastSeen.delete(sid);sessions.delete(sid);consoles.delete(sid)}
},10*60_000).unref();
/** Inline scripts (import map, text console boot) are allowed by hash; nothing else inline runs. */
const inlineScripts=['index.html','text.html','terminal/index.html'].flatMap(f=>{
  const file=path.join(ROOT,'public',f);
  return existsSync(file)?[...readFileSync(file,'utf8').matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m=>`'sha256-${createHash('sha256').update(m[1]).digest('base64')}'`):[];
});
const CSP=`default-src 'self'; script-src 'self' https://static.cloudflareinsights.com ${inlineScripts.join(' ')}; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' https://cloudflareinsights.com; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'self'`;
class HttpError extends Error{constructor(status,message){super(message);this.status=status}}
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.mjs':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml'};
/** Server modules the browser may import. Each is checked to hold no oracle or NPC state. */
const PUBLIC_LIB=new Set(['grammar.mjs','floorplan.mjs','world/ranking-tables.mjs']);
const CHANNELS=new Set(['person','nora','note','think']);
function json(res,status,data){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(data))}
async function body(req){let str='';for await(const chunk of req){str+=chunk;if(str.length>3_500_000)throw new HttpError(413,'Request too large.')}try{return JSON.parse(str||'{}')}catch{throw new HttpError(400,'Bad request.')}}
function getSession(req,res){
  let sid=(req.headers.cookie||'').match(/(?:^|;\s*)lab_sid=([\w-]+)/)?.[1];
  if(!sid || !sessions.has(sid)){sid=randomUUID();sessions.set(sid,newSession());res.setHeader('Set-Cookie',`lab_sid=${sid}; HttpOnly; SameSite=Lax; Path=/`)}
  lastSeen.set(sid,Date.now());
  return {sid,s:sessions.get(sid)};
}
const both=(s,{track}= {})=>{
  const out={state:clientState(s),terminal:terminalState(s)};
  if(track) out.telemetry=playTelemetry(s);
  return out;
};
function bothTracked(s,sid){
  appendTelemetryRow(playTelemetry(s),{sid});
  return both(s,{track:true});
}
/** Reset and import start a new game but keep the model budget, so they do not refill it. */
function replaceSession(sid,old,next){next.usage=old.usage;sessions.set(sid,next);return next}

const server=http.createServer(async(req,res)=>{
  res.setHeader('Content-Security-Policy',CSP);
  res.setHeader('X-Content-Type-Options','nosniff');
  res.setHeader('Referrer-Policy','no-referrer');
  try{
    const url=new URL(req.url,`http://${req.headers.host||'localhost'}`);
    if(url.pathname.startsWith('/api/')){
      const {sid,s}=getSession(req,res);
      if(req.method==='GET'){
        if(url.pathname==='/api/state')return json(res,200,clientState(s));
        if(url.pathname==='/api/terminal')return json(res,200,terminalState(s));
        if(url.pathname==='/api/handset-file'){
          const media=handsetMediaPayload(s,url.searchParams.get('rel'));
          if(!media)return json(res,404,{error:'Not readable.'});
          res.writeHead(200,{'Content-Type':media.mime,'Cache-Control':'no-store','Content-Security-Policy':"default-src 'none'; sandbox"});
          return res.end(media.body);
        }
        if(url.pathname==='/api/export'){
          res.setHeader('Content-Disposition','attachment; filename="last-safety-review-save.json"');
          return json(res,200,exportSession(s));
        }
        return json(res,405,{error:'Method not allowed'});
      }
      if(req.method!=='POST')return json(res,405,{error:'Method not allowed'});
      const b=await body(req);
      if(url.pathname==='/api/reset')return json(res,200,bothTracked(replaceSession(sid,s,newSession()),sid));
      if(url.pathname==='/api/import'){
        const {session,error}=await importSession(b,applyAction);
        if(error)return json(res,400,{error});
        return json(res,200,bothTracked(replaceSession(sid,s,session),sid));
      }
      if(url.pathname==='/api/go'){const r=applyAction(s,'go',{room:b.room});return json(res,r.error?400:200,{...r,...bothTracked(s,sid)})}
      if(url.pathname==='/api/inspect'){const r=applyAction(s,'inspect',{id:b.id});return json(res,r.error?400:200,{...r,...bothTracked(s,sid)})}
      if(url.pathname==='/api/settings'){applyAction(s,'settings',{conceptLinksEnabled:!!b.conceptLinksEnabled});return json(res,200,bothTracked(s,sid))}
      if(url.pathname==='/api/thought'){const r=applyAction(s,'thought',{action:b.action==='note'?'note':'close'});return json(res,r.error?400:200,{...r,...bothTracked(s,sid)})}
      if(url.pathname==='/api/text'){
        if(!consoles.has(sid))consoles.set(sid,createConsole(()=>sessions.get(sid),{phrase:true}));
        const r=await consoles.get(sid).handle(String(b.line||'').slice(0,600));
        return json(res,200,r);
      }
      if(url.pathname==='/api/tab-complete'){
        const line=String(b.line||'').slice(0,600);
        const page=Math.max(0,Number(b.page)||0);
        const lines=await tabCompleteLines(s,line,page);
        return json(res,200,{lines,line});
      }
      if(url.pathname==='/api/tool'){
        const r=await applyAction(s,'tool',b||{});
        return json(res,r.ok===false&&r.reason==='Not available on this phone.'?403:200,{result:r,...bothTracked(s,sid)});
      }
      if(url.pathname==='/api/parse'){
        const text=preparePlayerUtterance(b.text);
        const channel=CHANNELS.has(b.channel)?b.channel:'person';
        if(!text.trim())return json(res,200,{parse:makeParse(),state:clientState(s)});
        const here=npcsInRoom(s,s.room);
        const actorId=channel==='nora'?'nora':(here.includes(b.addressee)?b.addressee:here[0]||null);
        const parse=await parseUtterance({text,known:[...s.vocab],history:s.conversations,actorId,previousParse:b.previousParse,constructionTrace:b.constructionTrace},s.usage);
        return json(res,200,{parse:cleanParse({...parse,source:'llm'},s),state:clientState(s)});
      }
      if(url.pathname==='/api/respond'){
        const text=preparePlayerUtterance(b.text);
        const here=npcsInRoom(s,s.room);
        const actorId=here.includes(b.addressee)?b.addressee:here[0]||null;
        let parse=cleanParse(b.parse,s);
        if(parse.source!=='completion'){
          const p=await parseUtterance({text,known:[...s.vocab],history:s.conversations,actorId,previousParse:parse,constructionTrace:b.constructionTrace},s.usage);
          parse=cleanParse({...p,source:'llm'},s);
        }
        if(!text&&!['think','commit'].includes(parse.kind))return json(res,400,{error:'Empty utterance'});
        const r=applyAction(s,'respond',{parse,addressee:b.addressee||null,text});
        if(r.error)return json(res,400,{error:r.error,...both(s)});
        if(r.thought)return json(res,200,{thought:r.thought,...bothTracked(s,sid)});
        const lines=await phraseLines(s,text,r.lines||[]);
        return json(res,200,{reply:lines.map(l=>l.text).join(' '),lines,effects:r.effects||[],parse,...(r.ending?{ending:r.ending}:{}),...bothTracked(s,sid)});
      }
      if(url.pathname==='/api/telemetry'){
        const row={
          fuel:Number(b.fuel),
          room:String(b.room||'').slice(0,40),
          act:String(b.act||'').slice(0,20),
          npc:b.npc==null?null:String(b.npc).slice(0,40),
          knowledge:b.knowledge==null?null:String(b.knowledge).slice(0,80),
        };
        if(!Number.isFinite(row.fuel)||!row.room||!row.act)return json(res,400,{error:'Bad request.'});
        appendTelemetryRow(row,{sid});
        res.writeHead(204,{'Cache-Control':'no-store'});
        return res.end();
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
    res.writeHead(200,{'Content-Type':mime[path.extname(absolute)]||'application/octet-stream','Cache-Control':'no-store'});res.end(data);
  }catch(e){
    // Details stay in the server log; the browser gets a fixed message (no paths, no upstream text).
    if(e instanceof HttpError)return json(res,e.status,{error:e.message});
    if(e?.code==='ENOENT'||e?.code==='EISDIR')return json(res,404,{error:'Not found.'});
    console.error(e);
    json(res,502,{error:'Something went wrong on the server. Try again.'});
  }
});
server.listen(PORT,'127.0.0.1',()=>console.log(`Last Safety Review prototype: http://127.0.0.1:${PORT} (${process.env.OPENAI_API_KEY&&process.env.DEMO_MODE!=='1'?'live':'demo'})`));
