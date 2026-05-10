# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Collection of self-contained custom Alexa skills. Each skill under `skills/<name>/` is its own ASK CLI v2 project — independently deployable via `cd skills/<name> && ask deploy` from a clone of this repo. There is no shared library or test suite across skills.

## Per-skill layout (ASK CLI v2 standard)

```
skills/<name>/
├── ask-resources.json                                 # ASK CLI config (default profile, lambda-deployer)
├── skill-package/
│   ├── skill.json                                     # manifest (name, category, privacy, endpoint placeholder)
│   ├── interactionModels/custom/en-US.json            # invocation name + intents + slots
│   └── assets/images/                                 # 108x108 + 512x512 icons (currently empty — needed for cert)
├── lambda/
│   ├── lambda_function.py                             # handler (must include `lambda_handler(event, context)`)
│   └── requirements.txt                               # pip deps; package-lambda script reads this
└── README.md
```

This shape is required for `ask deploy` and for the Alexa Console's "Import skill" flow to work.

## Skills currently in the repo

- **`skills/foul-mouth/`** — Static random-response novelty skill. Stdlib only (`random`). Profane responses — won't pass cert without a Mature rating.
- **`skills/ollama-brain/`** — Proxies questions to a self-hosted Ollama LLM. Reads `OLLAMA_URL` (default `http://192.168.1.100:11434/api/chat`) and `OLLAMA_MODEL` (default `llama3.1`). Bundles `requests` via `lambda/requirements.txt`.

## Deployment paths

**Preferred — ASK CLI from a clone:**
```bash
cd skills/<name> && ask deploy
```
Creates the skill in the Amazon developer account, builds the model, zips `lambda/` (with `requirements.txt` deps), uploads to Lambda, and wires the ARN.

**Fallback — manual zip + AWS Console upload:**
```bash
bash .claude/skills/package-lambda/build.sh <name>     # → dist/<name>.zip
```
Then upload the zip yourself and paste `skill-package/interactionModels/custom/en-US.json` into the Console's JSON Editor.

The fallback exists because `ask deploy` requires AWS credentials configured for the Lambda role; the script doesn't.

## Things to know before editing

- **Alexa response envelope contract** — every handler return value must match `{"version": "1.0", "response": {"outputSpeech": {"type": "PlainText"|"SSML", ...}, "shouldEndSession": bool, "reprompt": {...optional...}}}`. Breaking this silently fails the simulator. The `alexa-response-lint` skill (`.claude/skills/alexa-response-lint/`) auto-applies when editing handlers.
- **Five built-in intents are required for cert**: `AMAZON.HelpIntent`, `AMAZON.CancelIntent`, `AMAZON.StopIntent`, `AMAZON.NavigateHomeIntent`, `AMAZON.FallbackIntent`. Both interaction models include them. Don't remove.
- **Sample utterances with slots must reference the slot** — `"tell me about {Query}"` not `"tell me anything"`. Alexa's model validator flags missing references.
- **`ollama-brain` LAN reach** — the default `OLLAMA_URL` points at a private IP. For Lambda to reach it: VPC + NAT, public tunnel (ngrok/Cloudflare), or override `OLLAMA_URL` to a public endpoint.
- **Cross-platform pip wheels** — the `package-lambda` script uses `--platform manylinux2014_x86_64 --only-binary=:all:` so macOS doesn't pull darwin `.so` files that fail on Lambda's Linux runtime. Override the Python version with `LAMBDA_PY_VER=3.11 ...` if your Lambda isn't 3.12.

## Hooks active in this repo

- **`.claude/hooks/guard-interaction-model.sh`** — `PreToolUse` on `Edit|Write|MultiEdit`, blocks edits to any `interactionModels/**/*.json` (and the legacy `interaction_model.json`) so the repo doesn't desync from the Alexa Console without explicit confirmation.

## Conventions

- Each skill is self-contained — don't introduce shared modules across skills without a clear reason.
- Per-skill `README.md` documents that skill's intent and deployment notes.
- The `foul-mouth` tone (profanity) is intentional — preserve it in non-required paths. The required `AMAZON.HelpIntent` / `AMAZON.StopIntent` responses are sanitized so the Mature-rating decision doesn't get worse.
