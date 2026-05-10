#!/usr/bin/env bash
# PreToolUse hook: block silent edits to interaction_model.json.
# These files are the source of truth shared with the Alexa Developer Console;
# editing them in the repo without re-uploading desyncs console state.
#
# Hook input is JSON on stdin from Claude Code. We extract the file path and,
# if it targets an interaction_model.json, exit 2 (block) with a stderr message
# instructing Claude to confirm with the user first.

set -euo pipefail

# jq is the cleanest way; fall back to grep if missing.
if command -v jq >/dev/null 2>&1; then
  PATH_ARG="$(jq -r '.tool_input.file_path // empty' 2>/dev/null || true)"
else
  INPUT="$(cat)"
  PATH_ARG="$(printf '%s' "$INPUT" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')"
fi

# Match both the legacy flat path and the ASK CLI v2 path
# (skill-package/interactionModels/custom/<locale>.json).
if [[ "${PATH_ARG:-}" == *"/interaction_model.json" \
   || "${PATH_ARG:-}" == *"/interactionModels/"*".json" ]]; then
  cat >&2 <<'MSG'
BLOCKED: edits to interaction_model.json are guarded.

This file is the source of truth shared with the Alexa Developer Console.
Editing it in the repo without re-uploading to the Console will desync state.

Before proceeding, confirm with the user:
  1. They want the schema change in BOTH places.
  2. They will re-import the JSON to the Alexa Console after merge.

If approved, ask the user to re-run the edit and skip this hook for the turn,
or temporarily disable the hook in .claude/settings.json.
MSG
  exit 2
fi

exit 0
