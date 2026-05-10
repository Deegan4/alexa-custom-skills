---
name: package-lambda
description: Build deployable AWS Lambda + Alexa skill-package zips for a skill in this repo. Use when the user asks to package, zip, deploy, or build a skill, or mentions errors like ModuleNotFoundError in Lambda logs or "package is not supported format" in the Alexa Console.
disable-model-invocation: true
---

# package-lambda

Builds two artifacts per skill, both into `dist/`:

| Artifact | Purpose | Upload target |
|---|---|---|
| `dist/<skill>.zip` | Lambda handler + bundled `requirements.txt` deps, Linux-targeted | AWS Lambda Console → Upload from .zip |
| `dist/<skill>-skill-package.zip` | `skill.json` rooted at zip top-level + `interactionModels/` + `assets/` | Alexa Developer Console → Import skill (or `ask smapi` calls) |

## Usage

```bash
bash .claude/skills/package-lambda/build.sh <skill-name>
```

## What it does

1. Reads `skills/<name>/lambda/lambda_function.py` + `requirements.txt`.
2. If deps exist, runs `pip install -t <build>/ -r requirements.txt` with `--platform manylinux2014_x86_64 --only-binary=:all:` so darwin wheels don't sneak into the Lambda zip.
3. Zips handler + deps → `dist/<skill>.zip`.
4. Zips `skills/<name>/skill-package/` *contents* (cd-into + zip `.`) so `skill.json` lands at the zip root → `dist/<skill>-skill-package.zip`.
5. Verifies `skill.json` exists at the zip root; aborts if not.

## Why this matters here

- `ollama-brain` imports `requests`, which is **not** in the AWS Lambda Python runtime. Uploading `lambda_function.py` alone causes a silent `ModuleNotFoundError: requests` at invocation.
- The Alexa Console rejects skill-package zips whose root is `skill-package/skill.json` instead of `skill.json` with the error **"package is not supported format"**. The `cd skill-package && zip .` pattern in this script avoids that.
- macOS pip pulls darwin `.so` files for `requests`'s deps that fail to import on Lambda's Linux runtime — the platform/wheel flags prevent that.

## Overrides

- `LAMBDA_PY_VER=3.11 bash .claude/skills/package-lambda/build.sh <name>` — target a Lambda Python runtime other than 3.12.
