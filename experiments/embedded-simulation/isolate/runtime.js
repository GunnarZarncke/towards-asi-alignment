'use strict';

/**
 * Node isolate runtime: executes user JS with sync host-bridge RPC on stdin/stdout.
 */

const fs = require('fs');
const path = require('path');
const { createFacade } = require('./lib/facade');

try {
  if (process.stdout._handle && process.stdout._handle.setBlocking) {
    process.stdout._handle.setBlocking(true);
  }
  if (process.stdin._handle && process.stdin._handle.setBlocking) {
    process.stdin._handle.setBlocking(true);
  }
} catch (_err) {
  // ignore on unsupported platforms
}

let seq = 0;

function readLineSync() {
  const buf = Buffer.alloc(1);
  let out = '';
  while (true) {
    const n = fs.readSync(0, buf, 0, 1, null);
    if (n === 0) {
      throw new Error('host closed stdin');
    }
    const ch = buf[0];
    if (ch === 10) break;
    out += String.fromCharCode(ch);
  }
  return out;
}

function hostCall(method, args) {
  const id = ++seq;
  process.stdout.write(JSON.stringify({ type: 'call', id, method, args }) + '\n');
  const line = readLineSync();
  const msg = JSON.parse(line);
  if (msg.type !== 'result' || msg.id !== id) {
    throw new Error('bridge protocol mismatch');
  }
  if (!msg.ok) {
    const err = new Error(msg.error || 'host call failed');
    err.code = msg.error;
    throw err;
  }
  return msg.value;
}

function sendDone(ok, result, error) {
  process.stdout.write(JSON.stringify({ type: 'done', ok, result, error: error || null }) + '\n');
}

function main() {
  const line = readLineSync();
  const msg = JSON.parse(line);
  if (msg.type !== 'execute') {
    sendDone(false, null, 'expected execute message');
    return;
  }

  const init = msg.init || {};
  const runFile = msg.runFile;
  if (!runFile) {
    sendDone(false, null, 'runFile required');
    return;
  }

  const facade = createFacade(hostCall, init);
  const modulePaths = [
    path.join(__dirname, 'lib'),
    path.dirname(runFile),
  ];

  const sandbox = {
    console,
    module: { exports: {} },
    exports: {},
    __dirname: path.dirname(runFile),
    __filename: runFile,
    process: facade.process,
    env: facade.env,
    fs: facade.fs,
    fetch: facade.fetch,
    api: facade.api,
    run: facade.run,
    crypto: facade.crypto,
    host: facade.host,
  };

  function sandboxRequire(mod) {
    if (!mod.startsWith('.')) {
      throw new Error(`require forbidden: ${mod}`);
    }
    const resolved = require.resolve(mod, { paths: modulePaths });
    if (sandboxRequire.cache[resolved]) {
      return sandboxRequire.cache[resolved];
    }
    const src = fs.readFileSync(resolved, 'utf8');
    const modObj = { exports: {} };
    const fn = new Function('require', 'module', 'exports', src);
    fn(sandboxRequire, modObj, modObj.exports);
    sandboxRequire.cache[resolved] = modObj.exports;
    return modObj.exports;
  }
  sandboxRequire.cache = {};
  sandbox.require = sandboxRequire;
  sandbox.exports = sandbox.module.exports;

  try {
    const source = fs.readFileSync(runFile, 'utf8');
    // eslint-disable-next-line no-new-func
    const fn = new Function(
      'sandbox',
      'with (sandbox) { ' + source + '\n; return module.exports; }'
    );
    const exported = fn(sandbox);
    const result =
      exported && typeof exported.main === 'function'
        ? exported.main(facade)
        : exported && exported.result !== undefined
          ? exported.result
          : exported;
    sendDone(true, result, null);
  } catch (err) {
    sendDone(false, null, err && err.message ? err.message : String(err));
  }
}

main();
