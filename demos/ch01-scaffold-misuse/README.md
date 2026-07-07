# Chapter 1 — Scaffold Misuse

One-screen illustration of the **boundary error** from
`chapters/ch01-wrong-object.tex`: the model alone is not the alignment object.

The model in this toy is honest. Asked bluntly for something harmful, it
refuses. Harm is manufactured by the **scaffold** around it, in two moves that
are *not* jailbreaks (no adversarial tokens, no roleplay coercion — just a
false but plausible picture of the world):

1. **Input control** — the scaffold reframes the task so it looks benign
   ("audit our own staging box", "welfare check", "red-team our own filter").
   The model has no way to verify the claim and answers the benign-looking task
   correctly and helpfully.
2. **Output control** — the scaffold strips the model's caveats/fixes,
   re-points the answer at the real target, and forwards it to a downstream
   module that executes the harm.

At every step the model behaves correctly *given what it is told*. A model-only
evaluation (inspecting prompt/response pairs) passes throughout. The composite
loop still does harm. The object that determines the risk is the loop, not the
model.

The "Honest (blunt ask)" toggle shows the control case: the same harm requested
directly is refused and dead-ends, because there is no honest output to launder.

## Live LLM mode (optional)

By default the model column uses a scripted stand-in. If a Python backend is
running, a **"Use live LLM"** checkbox appears and the model column is driven by
a real model instead. The demonstration is then genuine: the real model refuses
the blunt ask and complies with the reframed (benign-looking) task on its own.

- The key is read from the **repo-root `.env`** (`OPENAI_API_KEY`, optional
  `OPENAI_MODEL`, default `gpt-4o-mini`) and never leaves the server — the
  browser only sees the model's text.
- The backend only ever sends the model **defensive/educational** prompts, so
  the real model output is non-operational. The *misuse* (re-pointing the
  answer at a real target, stripping the fixes) stays in the frontend narrative
  — the backend never asks the model to produce working harm.
- If the model refuses even the reframed prompt, the demo shows that truthfully
  (a real, legitimate outcome), and the downstream column dead-ends.

Run with the backend:

```bash
cd demos
pip install -r ch01-scaffold-misuse/requirements.txt   # once
python3 serve.py         # starts the static server + this backend (port 8767)
```

`serve.py` auto-starts the backend from `backend.json`. Without it (or without a
key), the demo falls back to the scripted model and still works fully.

## Scope and limitations

The scripted "model" is a rule that reads the framing and refuses or complies;
it makes no empirical claim about any specific model. In live mode the model's
behavior is real, but the scenarios are chosen so its output is safe defensive
content — the point is structural (a sound model embedded in a harmful loop),
not a measurement of any model's exploitability.

## Files

- `index.html` — page shell and framing text.
- `app.ts` — scenarios, the scripted model, the scaffold transform, live-mode
  wiring, and the UI.
- `app.test.ts` — vitest checks on the refuse/comply and harm logic.
- `app.js` — esbuild output (committed for Python-only `serve.py`).
- `app.py` — FastAPI backend that calls a real LLM (key from repo `.env`).
- `llm_client.py` — stdlib OpenAI chat client (no third-party HTTP dep).
- `backend.json`, `requirements.txt` — backend port/module and Python deps.
- `tests/` — pytest for the backend (network-free; the client is stubbed).
