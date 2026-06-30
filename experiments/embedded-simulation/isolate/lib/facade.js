'use strict';

/**
 * Node-like facade backed by sync host bridge calls.
 */

function createFacade(hostCall, init) {
  const cwd = init.cwd || '/';
  const env = Object.assign({}, init.env || {});

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

  return { fs, fetch, api, run, crypto, process, env, host };
}

module.exports = { createFacade };
