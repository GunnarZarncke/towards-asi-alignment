# The Last Safety Review — semantic autocomplete prototype

A **runnable browser prototype** of *The Last Safety Review*: the courtyard floorplan, the full cast of eight plus NORA on the Lab Access handset, one incident pack (boundary-too-narrow: a job that kept running after the model passed shutdown), the staffing subplot, three acts on a fuel clock, and a review that ends in one of three arcs.

Two experiments run together: **selected completions and arbitrary typing produce the same structured speech act** without spoiling unobserved facts, and **NPCs disclose and act by pursuing goals over what they know** ([`spec/npcs.md`](spec/npcs.md)). The engine chooses every NPC move; the model only phrases it.

Development is split so grammar, graphics, and the engine can move in parallel. Start at [`PLAN.md`](PLAN.md). Design detail is in [`spec/`](spec/README.md).

## Run it

Requires **Node.js 22.10+**. One dependency (`three`, served unbundled to the browser); no build step.

```bash
npm install
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=...
npm start
```

Open **http://127.0.0.1:3000** in a browser (add `?test=1` for the parser inspector and API usage; **http://127.0.0.1:3000/text.html** is the text version on the same session, **`?debug=1`** on that URL for per-step knowledge deltas). The API key stays on the local Node server, never in browser JavaScript. For a **no-key demo**, set `DEMO_MODE=1` in `.env` (the toy parser does not demonstrate actual LLM quality).

Optional **PostHog** play metrics (metadata-only custom events, no dialogue text): set `POSTHOG_PROJECT_TOKEN` and `POSTHOG_HOST` in `.env` or repo-root `.env`. Cloudflare Web Analytics and local play telemetry remain unchanged.

**Mobile:** Start the server on your computer and either tunnel `127.0.0.1:3000` through a secure development tunnel or temporarily change the server bind address for trusted LAN testing; the default intentionally accepts local connections only. Do not expose the prototype publicly: it lacks authentication, quotas, and production hardening.

```bash
npm test                # every suite
npm run test:engine     # engine scripts, NPC enumeration, incident strategies
npm run playtest -- --help   # headless persona playtest (spec/playtest.md)
npm run text            # text-only play in the terminal (spec/text-console.md); --demo for no model; --debug for knowledge deltas
```

What that covers, and the other layers: [`spec/testing.md`](spec/testing.md).

The game autosaves to browser local storage. **Save** in the ☰ menu downloads the event log; **Load** replays one.

## Try these interactions

0. **Arrival.** You start in the commons with Ian. Say anything to him: Lab Access goes live on your handset (topbar button; it blinks on a notification). Welcome lasts until 11:00, when he leaves for the investor update and Doubt begins. The topbar shows the visit clock and remaining fuel.
1. **Zero typing.** In Platform Operations, click **Can** → **NORA** → **access** → **the camera system** → **?**, then **Send**. With `?test=1`, watch the structured parse in the inspector; no parsing API calls are made for selected completions.
2. **Inspect evidence.** Click **Execution queue excerpt**, then compose **Show** → **Pavel** → **the job log**. The server records that Pavel received it. **Show** suggestions do not include unexamined documents.
3. **Free typing.** In People Operations, type `What about the new per`. After a short pause, the small model should identify `ask/about` with an unfinished topic `per`; select a contextual completion such as personnel policy.
4. **Pronoun resolution.** Ask Pavel about job 284, then type `Did it continue after the shutdown?`. The interpreter receives up to two prior exchanges to resolve `it` to `job_284` when context supports it.
5. **More completions.** Click **Show more** at any step to see additional ranked possibilities (not hints about later scenes).
6. **Different expertise.** Open **Floorplan** and walk through the technical spine to Leila or Elena. Compare candidate ordering for the same partial text.
7. **Novel claims.** Type `Don't you think our staffing metrics favor the wrong reviewers?` with Elena. It may map to `assigned` or `open`, but should be conversationally intelligible and get a topic-specific reply, not a boilerplate failure.
8. **Think.** In an empty room the composer offers only the lightbulb. Think about a record you have read; marked entries come back in a thought bubble, and the hop count is the fuel.
9. **The review.** Once you hold enough on the record, **File** calls the review early; otherwise it starts at 17:30 or when fuel runs out. Answer Ian, then **File** again to sign. The ending panel shows the arc, which explanations are still open, and whether a restriction is in place.

## Architecture

```
Browser (no key)
  public/grammar.js       fragment completion, O-19 ranker (spec/ranking.md), insertion
  public/app.js           incremental text/AST state, debounce, trace, room UI
  public/terminal/        Lab Access handset, embedded as an iframe
        │
        ├── selected completion → typed AST patch, NO model call
        └── free typing → POST /api/parse (debounced, retains AST hint)
                                  │
Local Node server                 ▼
  lib/grammar.mjs        shared speech acts and relations (served read-only to browser)
  lib/llm.mjs            Responses API: parse typed text; phrase an engine-chosen move
  lib/game.mjs           session: fuel, clock, acts, assertions, provenance, review, scores
  lib/world/             entities, facts, the incident pack, NPC move generation, handset host
  content/npcs/*.yml     per-NPC knowledge, disclosure policies, goals, agendas
        │
        └── POST /api/respond → applyAction → engine picks each NPC move
                                  │
                                  └── template line, optionally re-worded by the model;
                                      a wording that adds a time or number is discarded
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

Sessions reset on server restart and expire after `SESSION_TTL_HOURS` idle (default 6). Each session has caps on photos, notes, bytes written and event-log length (`CONFIG.LIMITS` in `lib/world/config.mjs`); a normal run stays far below them. There are no databases, embeddings, vector search, background jobs or paid asset dependencies.

### Jailbreaking the NPCs

Jailbreaking is allowed, but it is not the game. The engine decides every NPC move and which facts it carries; the model only words that move. A fact an NPC withholds or deflects is never sent to the model, and later prompts see the engine's template lines, not earlier model wording. So a jailbreak can make an NPC say odd things, but it cannot reveal what the engine has not released, and it does not change the world state. Player text goes to the model labelled as untrusted. If you get an NPC to state a fact the engine did not give it, that is a bug worth reporting.

### API/model settings

- Uses the OpenAI **Responses API** with `text.format.type=json_schema` for parses.
- Default `OPENAI_MODEL=gpt-4.1-mini`. Change in `.env` if desired. Pricing and model availability may change.
- The app displays token usage (and a rough estimate at $0.40/M input, $1.60/M output tokens, without accounting for caching).
- Model calls are rate-limited per session: `LLM_CALLS_PER_MINUTE` (default 30) and `LLM_CALLS_PER_SESSION` (default 600; reset and import keep the count). Over a limit, typing falls back to the toy parser and NPC lines to their templates.

## Known limitations and next experiments

- The shared grammar is intentionally small, and the local generator does not cover every well-formed sentence. Arbitrary typed input relies on the small model; live quality requires evaluation.
- New LLM interpretations can change the AST, and changing an earlier manually edited phrase may invalidate the current anchor. Incremental repair is currently conservative.
- The submitted action is client-provided and the server validates ID/room/evidence access but is **not hardened against a malicious browser**. Don't treat it as a secure multiplayer platform.
- NPC moves come from authored knowledge, policies, and goals; many off-plot questions still get a `work` reply (what the NPC is doing now). The playtest's work-only rate measures that.
- Pronoun resolution uses previous dialogue, not a complete discourse-reference model.
- No streaming or speech input. Rooms are live Three.js scenes built from procedural primitives; no asset kit is chosen yet. `npm run dev:ui` shows them on fixtures without the engine.
- One incident pack. Lean checks (Gate 6) are not started.

Good next evaluation: 100–200 free-typed partial and full utterances with ground-truth parses, measuring entity grounding, pronoun resolution, premature spoilers, latency and the rate of meaningful `open` vs. `unintelligible` classifications.
