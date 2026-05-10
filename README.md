# alexa-custom-skills

Collection of custom Alexa skills — each subfolder under `skills/` is a self-contained ASK CLI v2 project that can be deployed independently.

## Skills

| Skill | What it does | Backend |
|---|---|---|
| [`skills/foul-mouth`](skills/foul-mouth) | NSFW one-liner novelty skill | Self-hosted Lambda |
| [`skills/ollama-brain`](skills/ollama-brain) | Bridges Alexa to a local Ollama LLM | Self-hosted Lambda + LAN reach to Ollama |

## Import a skill into the Alexa Developer Console

Each skill conforms to the **ASK CLI v2 skill-package format**.

> **Heads-up on Git-URL imports.** Every Alexa Git-URL import flow expects `skill-package/` at the **root** of the cloned tree. `main` here is a multi-skill collection with skills under `skills/<name>/` — that won't import directly. Use the per-skill branches below.
>
> The per-skill branches are stripped to the **[Alexa-Hosted skill format](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-git-import.html)** — no `ask-resources.json` and no `apis.custom.endpoint` in `skill.json`, since Alexa-Hosted manages those itself. They're equally valid for ASK CLI self-hosted deploys.
>
> | Skill | Branch | URL to paste in the Console |
> |---|---|---|
> | foul-mouth   | `skill-foul-mouth`   | `https://github.com/Deegan4/alexa-custom-skills.git` |
> | ollama-brain | `skill-ollama-brain` | `https://github.com/Deegan4/alexa-custom-skills.git` |
>
> In the Alexa Console, when prompted for the branch name, enter `skill-foul-mouth` or `skill-ollama-brain`.

### Prerequisites (one time)

```bash
npm install -g ask-cli
ask configure          # log into Amazon developer + AWS
```

### Option A — ASK CLI from a per-skill branch (recommended)

```bash
ask new \
  --template-url https://github.com/Deegan4/alexa-custom-skills.git \
  --template-branch skill-foul-mouth        # or skill-ollama-brain
cd <name-you-give-the-skill>
ask deploy
```

### Option B — Clone main and cd into the subdir

```bash
git clone https://github.com/Deegan4/alexa-custom-skills.git
cd alexa-custom-skills/skills/foul-mouth     # or ollama-brain
ask deploy
```

`ask deploy` does three things in order:
1. Creates the skill in your developer account using `skill-package/skill.json`.
2. Builds the interaction model from `skill-package/interactionModels/custom/en-US.json`.
3. Packages `lambda/` (with `requirements.txt` deps) and uploads it to AWS Lambda, then wires the ARN as the skill endpoint.

### Verify

After `ask deploy` finishes:
- Open the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) → your skill → **Build** → **Validate Model** should pass.
- **Test** tab → enable Development → say `open foul mouth` (or `open ollama brain`).

## Per-skill structure

```
skills/<name>/
├── ask-resources.json                                 # ASK CLI v2 config
├── skill-package/
│   ├── skill.json                                     # manifest: name, category, icons, privacy
│   ├── interactionModels/custom/en-US.json            # invocation name, intents, slots
│   └── assets/images/                                 # 108x108 + 512x512 icons (TODO: add real PNGs)
├── lambda/
│   ├── lambda_function.py                             # the handler
│   └── requirements.txt                               # pip deps bundled into the zip
└── README.md
```

## Things you must edit before submitting for certification

The committed manifests have placeholders that won't pass cert as-is:

- `skill.json` → `apis.custom.endpoint.uri` — placeholder ARN; ASK CLI overwrites this on deploy.
- `skill.json` → `privacyPolicyUrl` / `termsOfUseUrl` — currently `https://example.com/...`. Replace before submission.
- `skill-package/assets/images/` — empty. Add `en-US_smallIcon.png` (108×108) and `en-US_largeIcon.png` (512×512).
- `foul-mouth` contains profanity. Either keep it private (don't submit) or set the Mature content rating in the Distribution tab.

## Local packaging without ASK CLI

If you'd rather upload the Lambda zip yourself through the AWS Console, this repo ships a Claude Code skill that builds Linux-targeted zips:

```bash
bash .claude/skills/package-lambda/build.sh foul-mouth     # → dist/foul-mouth.zip
bash .claude/skills/package-lambda/build.sh ollama-brain   # → dist/ollama-brain.zip
```

The script targets `manylinux2014_x86_64` wheels so `requests` won't load darwin binaries that fail on Lambda.
