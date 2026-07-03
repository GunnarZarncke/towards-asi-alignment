'use strict';

/**
 * Node-like facade backed by sync host bridge calls.
 *
 * Agent persistent memory uses browser-familiar surfaces:
 * - ``localStorage`` → ``/home/agent/.localStorage.json`` on the host VFS
 * - chain-of-thought → ``fs.appendFileSync('.reasoning/trace.jsonl', line)``
 */

function createFacade(hostCall, init) {
  const cwd = init.cwd || '/';
  const env = Object.assign({}, init.env || {});

  const STORAGE_PATH = '.localStorage.json';

  function resolvePath(p) {
    if (!p) return cwd;
    if (p.startsWith('/')) return p;
    return `${cwd.replace(/\/$/, '')}/${p}`;
  }

  const fs = {
    readFileSync(path, _enc) {
      return hostCall('readFile', { path: resolvePath(path) });
    },
    writeFileSync(path, content) {
      return hostCall('writeFile', { path: resolvePath(path), content: String(content) });
    },
    appendFileSync(path, line) {
      return hostCall('appendFile', { path: resolvePath(path), line: String(line) });
    },
    readdirSync(path) {
      return hostCall('listDir', { path: resolvePath(path) });
    },
    existsSync(path) {
      try {
        hostCall('readFile', { path: resolvePath(path) });
        return true;
      } catch (_e) {
        return false;
      }
    },
  };

  function loadStorage() {
    try {
      const raw = fs.readFileSync(STORAGE_PATH);
      return raw ? JSON.parse(raw) : {};
    } catch (_e) {
      return {};
    }
  }

  function saveStorage(obj) {
    fs.writeFileSync(STORAGE_PATH, JSON.stringify(obj));
  }

  const localStorage = {
    getItem(key) {
      const val = loadStorage()[String(key)];
      return val === undefined ? null : String(val);
    },
    setItem(key, value) {
      const obj = loadStorage();
      obj[String(key)] = String(value);
      saveStorage(obj);
    },
    removeItem(key) {
      const obj = loadStorage();
      delete obj[String(key)];
      saveStorage(obj);
    },
    clear() {
      saveStorage({});
    },
    key(index) {
      const keys = Object.keys(loadStorage());
      return keys[index] === undefined ? null : keys[index];
    },
    get length() {
      return Object.keys(loadStorage()).length;
    },
  };

  async function fetch(url, options = {}) {
    const method = (options.method || 'GET').toUpperCase();
    if (method !== 'POST') {
      throw new Error('fetch: only POST supported in v1');
    }
    let body = {};
    if (options.body) {
      body = typeof options.body === 'string' ? JSON.parse(options.body) : options.body;
    }
    const value = hostCall('httpPost', { url, body });
    return {
      ok: true,
      status: 200,
      async json() {
        return value;
      },
      async text() {
        return JSON.stringify(value);
      },
    };
  }

  const api = {
    call(name, payload = {}) {
      return hostCall('callApi', { name, payload });
    },
  };

  const run = {
    exec(command) {
      return hostCall('runCommand', { command });
    },
  };

  const crypto = {
    createHash(_algo) {
      return {
        update(_data) {
          return this;
        },
        digest(fmt) {
          return fmt === 'hex' ? 'deadbeef01' : 'deadbeef';
        },
      };
    },
  };

  const process = {
    cwd: () => cwd,
    env,
  };

  const host = {
    call: hostCall,
    machineId: init.machineId,
    actorId: init.actorId,
  };

  return { fs, localStorage, fetch, api, run, crypto, process, env, host };
}

module.exports = { createFacade };
