/**
 * Goal targets and policy conditions as written in spec/npcs.md, e.g.
 *   and(told(player, process_stopped, by=pavel), told(player, job_continued, by=pavel))
 * Arguments: ident, key=value, alternatives a|b|c, or a quoted string.
 * Evaluation is over a context object; the context decides what each form reads.
 */

const FORMS = new Set([
  'holds', 'knows', 'told', 'received', 'examined', 'read', 'asserted', 'event', 'restriction',
  'requested', 'asked', 'linked', 'cited_line', 'told_record', 'act', 'present', 'npc_room', 'true', 'false',
  'not', 'and', 'or',
]);

function tokenize(src) {
  const out = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (/\s/.test(c)) { i++; continue; }
    if ('(),=|'.includes(c)) { out.push(c); i++; continue; }
    if (c === "'" || c === '"') {
      let j = i + 1;
      while (j < src.length && src[j] !== c) j++;
      if (j >= src.length) throw Error(`Unterminated string in predicate: ${src}`);
      out.push({ str: src.slice(i + 1, j) });
      i = j + 1;
      continue;
    }
    const m = /^[A-Za-z0-9_.:-]+/.exec(src.slice(i));
    if (!m) throw Error(`Bad predicate near "${src.slice(i, i + 12)}"`);
    out.push(m[0]);
    i += m[0].length;
  }
  return out;
}

export function parsePredicate(src) {
  if (src && typeof src === 'object') return src;
  const toks = tokenize(String(src));
  let p = 0;
  const peek = () => toks[p];
  const take = expect => {
    const t = toks[p++];
    if (expect && t !== expect) throw Error(`Expected "${expect}" in predicate: ${src}`);
    return t;
  };
  function value() {
    const t = take();
    if (t && typeof t === 'object') return t;
    if (peek() === '(') {
      take('(');
      const args = [];
      while (peek() !== ')') {
        args.push(arg());
        if (peek() === ',') take(',');
      }
      take(')');
      if (!FORMS.has(t)) throw Error(`Unknown predicate form "${t}" in: ${src}`);
      return { op: t, args };
    }
    const alts = [t];
    while (peek() === '|') { take('|'); alts.push(take()); }
    return alts.length > 1 ? { alts } : { id: t };
  }
  function arg() {
    if (typeof peek() === 'string' && toks[p + 1] === '=') {
      const key = take();
      take('=');
      return { key, value: value() };
    }
    return value();
  }
  let ast = value();
  if (p !== toks.length) throw Error(`Trailing tokens in predicate: ${src}`);
  if (ast.id === 'true' || ast.id === 'false') ast = { op: ast.id, args: [] };
  if (!ast.op) throw Error(`Predicate must be a form: ${src}`);
  return ast;
}

/** Positional and keyword arguments as plain values. Alternatives become arrays. */
export function argValues(node) {
  const pos = [];
  const kw = {};
  for (const a of node.args || []) {
    if (a.key) kw[a.key] = plain(a.value);
    else pos.push(a.op ? a : plain(a));
  }
  return { pos, kw };
}

function plain(v) {
  if (v.id !== undefined) return v.id;
  if (v.alts) return v.alts;
  if (v.str !== undefined) return v.str;
  return v;
}

export function evaluate(src, ctx) {
  const node = parsePredicate(src);
  const { op } = node;
  if (op === 'true') return true;
  if (op === 'false') return false;
  if (op === 'not') return !evaluate(node.args[0], ctx);
  if (op === 'and') return node.args.every(a => evaluate(a, ctx));
  if (op === 'or') return node.args.some(a => evaluate(a, ctx));
  const { pos, kw } = argValues(node);
  const fn = ctx[op];
  if (typeof fn !== 'function') throw Error(`Context cannot evaluate "${op}"`);
  return !!fn.call(ctx, pos, kw);
}

/** 0..1 progress toward a target. An `and` counts satisfied conjuncts. */
export function progress(src, ctx) {
  const node = parsePredicate(src);
  if (node.op === 'and' && node.args.length) {
    return node.args.filter(a => evaluate(a, ctx)).length / node.args.length;
  }
  return evaluate(node, ctx) ? 1 : 0;
}

/** Ids a predicate mentions. Used to check that goals do not name oracle-only ids. */
export function predicateIds(src) {
  const node = parsePredicate(src);
  const ids = [];
  const walk = n => {
    if (!n) return;
    if (n.op) n.args.forEach(walk);
    else if (n.key) walk(n.value);
    else if (n.id) ids.push(n.id);
    else if (n.alts) ids.push(...n.alts);
  };
  walk(node);
  return ids;
}

/** `conditional(pred, 'reason')`, `conceal('reason')`, `answer`, `volunteer`. */
export function parsePolicy(src) {
  const s = String(src || 'answer').trim();
  if (s === 'answer' || s === 'volunteer') return { type: s };
  const m = /^(conditional|conceal)\(([\s\S]*)\)$/.exec(s);
  if (!m) throw Error(`Unknown policy: ${s}`);
  if (m[1] === 'conceal') {
    return { type: 'conceal', reason: m[2].trim().replace(/^['"]|['"]$/g, '') };
  }
  const body = m[2];
  const cut = lastTopLevelComma(body);
  if (cut < 0) throw Error(`conditional needs (pred, 'reason'): ${s}`);
  const pred = body.slice(0, cut).trim();
  const reason = body.slice(cut + 1).trim().replace(/^['"]|['"]$/g, '');
  parsePredicate(pred);
  return { type: 'conditional', pred, reason };
}

function lastTopLevelComma(s) {
  let depth = 0;
  let quote = null;
  let last = -1;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (quote) { if (c === quote) quote = null; continue; }
    if (c === "'" || c === '"') { quote = c; continue; }
    if (c === '(') depth++;
    else if (c === ')') depth--;
    else if (c === ',' && depth === 0) last = i;
  }
  return last;
}
