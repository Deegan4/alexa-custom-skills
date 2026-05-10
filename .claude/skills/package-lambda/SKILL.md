---
name: package-lambda
description: Build a deployable AWS Lambda zip for an Alexa skill in this repo, bundling third-party dependencies. Use when the user asks to package, zip, deploy, or build a skill, or mentions ModuleNotFoundError in Lambda logs.
disable-model-invocation: true
---

# package-lambda

Builds `dist/<skill-name>.zip` ready to upload to AWS Lambda.

## Usage

```
/package-lambda <skill-name>
```

Examples:
- `/package-lambda foul-mouth`
- `/package-lambda ollama-brain`

## What it does

1. Locates the skill's lambda handler (handles both layouts in this repo: `skills/<name>/lambda_function.py` and `skills/<name>/lambda/lambda_function.py`).
2. Detects third-party imports in the handler (anything not in stdlib).
3. If deps exist, runs `pip install -t <build>/ <deps>` into a build dir.
4. Copies the handler in alongside deps and zips the result to `dist/<skill-name>.zip`.

## Run

Invoke the bundled script:

```bash
bash .claude/skills/package-lambda/build.sh <skill-name>
```

## Why this matters here

`ollama-brain` imports `requests`, which is **not** in the AWS Lambda Python runtime. Uploading `lambda_function.py` alone causes a silent `ModuleNotFoundError: requests` at invocation. This skill is the safe path.

`foul-mouth` is stdlib-only and packaging is trivial — but use the same workflow so deployment is uniform across skills.
