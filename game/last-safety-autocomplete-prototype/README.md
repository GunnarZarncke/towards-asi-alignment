# The Last Safety Review — semantic autocomplete prototype

A **runnable browser prototype** of the conversation interface proposed for *The Last Safety Review*. It is deliberately ~10% of the proposed game: **three rooms, three NPCs, one persistent-job incident, one staffing subplot, three evidence records**, and a shared semantic grammar.

The primary experiment is **how selected completions and arbitrary typing produce the same structured speech act**, without spoiling unobserved facts.

Development is split so grammar, graphics, and the engine can move in parallel. Start at [`PLAN.md`](PLAN.md). Design detail is in [`spec/`](spec/README.md).

## Run it

Requires **Node.js 22.10+**. One dependency (`three`, served unbundled to the browser); no build step.

```bash
npm install
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=...
npm start
```

Open **http://127.0.0.1:3000** in a browser. The API key stays on the local Node server, never in browser JavaScript. For a **no-key demo**, set `DEMO_MODE=1` in `.env` (the toy parser does not demonstrate actual LLM quality).

**Mobile:** Start the server on your computer and either tunnel `127.0.0.1:3000` through a secure development tunnel or temporarily change the server bind address for trusted LAN testing; the default intentionally accepts local connections only. Do not expose the prototype publicly: it lacks authentication, quotas, and production hardening.

```bash
npm test
```

## Try these interactions

1. **Zero typing.** In Platform Operations, click **Can** → **NORA** → **access** → **the camera system** → **?**, then **Send**. Watch the right-hand structured parse; no parsing API calls are made for selected completions.
2. **Inspect evidence.** Click **Execution queue excerpt**, then compose **Show** → **Pavel** → **the job log**. The server records that Pavel received it. **Show** suggestions do not include unexamined documents.
3. **Free typing.** In People Operations, type `What about the new per`. After a short pause, the small model should identify `ask/about` with an unfinished topic `per`; select a contextual completion such as personnel policy.
4. **Pronoun resolution.** Ask Pavel about job 017, then type `Did it continue after the shutdown?`. The interpreter receives up to two prior exchanges to resolve `it` to `job_017` when context supports it.
5. **More completions.** Click **Show more** at any step to see additional ranked possibilities (not hints about future storylets).
6. **Different expertise.** Switch from Pavel to Leila or Elena and compare candidate ordering for the same partial text.
7. **Novel claims.** Type `Don't you think our staffing metrics favor the wrong reviewers?` with Elena. It may map to `assigned` or `open`, but should be conversationally intelligible and get a topic-specific reply, not a boilerplate failure.

## Architecture

```
Browser (no key)
  public/grammar.js       deterministic fragment completion, ranking, insertion
  public/app.js           incremental text/AST state, debounce, trace, UI
        │
        ├── selected completion → typed AST patch, NO model call
        └── free typing → POST /api/parse (debounced, retains AST hint)
                                  │
Local Node server                 ▼
  lib/grammar.mjs       shared speech acts and relations (served read-only to browser)
  lib/llm.mjs           Responses API, JSON Schema, compact player-visible vocabulary
  lib/game.mjs          oracle facts, NPC beliefs, evidence, room state, validated actions
        │
        └── POST /api/respond → validate structured speech act and update world
                                  │
                                  └── deterministic response for recognized facts/actions,
                                      grounded LLM dialogue for other intelligible input
```

### One semantic grammar

All inputs use the same `kind/relation/subject/object/topic/recipient/evidence` representation. Completions are pre-grounded and applied directly. Typed language is interpreted into the same shape with a small LLM; the returned structure is reused on submission. `open` is for meaningful but unmodeled language. `unintelligible` should be rare and reserved for genuinely unrecoverable speech.

The parser's user-visible vocabulary is sourced from the player's knowledge, **not from oracle-only facts**. It receives the most recent **four speaker messages (= up to two exchanges)**, compact ID/alias listings, the grammar, and the retained partial structure. The player may ask a false or speculative question; parsing it never makes it true.

### Autocomplete and spoiler safeguards

- Up to **five** completions; **Show more** paginates a stable ranking.
- Candidate relevance uses public NPC expertise, recent dialogue, known concepts, and examined evidence.
- Evidence suggestions for `Show` require that the player actually inspected the item.
- Relations are separated: `has_access` is not `authorized` or `did_use`.
- A newly hypothesized relationship is normally supplied by the **player's verb**; the engine offers known entities that fit the open slot.
- The current design is an experiment, **not a guarantee** against subtle semantic spoilers. Human testing is required.

### Where the game state lives

The server maintains one in-memory session per browser via an HttpOnly cookie. It knows additional facts that the browser does not. The browser receives a deliberately filtered list of known entities, examined evidence, and observed findings.

Sessions reset on server restart. There are no databases, embeddings, vector search, background jobs or paid asset dependencies.

### API/model settings

- Uses the OpenAI **Responses API** with `text.format.type=json_schema` for parses.
- Default `OPENAI_MODEL=gpt-4.1-mini`. Change in `.env` if desired. Pricing and model availability may change.
- The app displays token usage (and a rough estimate at $0.40/M input, $1.60/M output tokens, without accounting for caching).
- **No live model request was made during preparation** because the authoring environment had no API key. The demo parser and deterministic behavior were exercised, and the API path is implemented against the published Responses API shape.

## Known limitations and next experiments

- The shared grammar is intentionally small, and the local generator does not cover every well-formed sentence. Arbitrary typed input relies on the small model; live quality requires evaluation.
- New LLM interpretations can change the AST, and changing an earlier manually edited phrase may invalidate the current anchor. Incremental repair is currently conservative.
- The submitted action is client-provided and the server validates ID/room/evidence access but is **not hardened against a malicious browser**. Don't treat it as a secure multiplayer platform.
- The NPC response layer is partly scripted for reproducibility and partly generated for open conversation. It doesn't attempt full social-state simulation.
- Pronoun resolution uses previous dialogue, not a complete discourse-reference model.
- No streaming or speech input. Rooms are live Three.js scenes built from procedural primitives; no asset kit is chosen yet. `npm run dev:ui` shows them on fixtures without the engine.
- Storylets, Lean checks, formal causality and release outcomes are **out of prototype scope**.

Good next evaluation: 100–200 free-typed partial and full utterances with ground-truth parses, measuring entity grounding, pronoun resolution, premature spoilers, latency and the rate of meaningful `open` vs. `unintelligible` classifications.
