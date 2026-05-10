#!/usr/bin/env bash
# Build deployable artifacts for an Alexa skill in this repo.
# Produces:
#   dist/<skill>.zip                 -- Lambda code + bundled deps (upload to AWS Lambda)
#   dist/<skill>-skill-package.zip   -- skill.json rooted at zip top-level
#                                       (upload via Alexa Console "Import skill" or
#                                        ASK CLI, never via "Upload skill package"
#                                        with a nested skill-package/ folder)
#
# Usage: bash .claude/skills/package-lambda/build.sh <skill-name>

set -euo pipefail

SKILL="${1:-}"
if [[ -z "$SKILL" ]]; then
  echo "usage: build.sh <skill-name>" >&2
  ls skills 2>/dev/null | sed 's/^/  /' >&2
  exit 2
fi

LAMBDA_DIR="skills/$SKILL/lambda"
PKG_DIR="skills/$SKILL/skill-package"
SRC="$LAMBDA_DIR/lambda_function.py"
REQ="$LAMBDA_DIR/requirements.txt"

if [[ ! -f "$SRC" ]]; then
  echo "no lambda_function.py at $SRC" >&2; exit 1
fi
if [[ ! -f "$PKG_DIR/skill.json" ]]; then
  echo "no skill-package/skill.json at $PKG_DIR" >&2; exit 1
fi

DIST="dist"
mkdir -p "$DIST"

# ----- 1) Lambda zip -----
LAMBDA_BUILD="$(mktemp -d)"
trap 'rm -rf "$LAMBDA_BUILD" "${PKG_BUILD:-}"' EXIT

if [[ -s "$REQ" ]]; then
  PY_VER="${LAMBDA_PY_VER:-3.12}"
  echo "bundling deps for Lambda python${PY_VER} (linux x86_64) from $REQ"
  python3 -m pip install --quiet --target "$LAMBDA_BUILD" \
    --platform manylinux2014_x86_64 \
    --python-version "$PY_VER" \
    --implementation cp \
    --only-binary=:all: \
    -r "$REQ"
fi
cp "$LAMBDA_DIR"/*.py "$LAMBDA_BUILD/"

LAMBDA_OUT="$DIST/$SKILL.zip"
rm -f "$LAMBDA_OUT"
( cd "$LAMBDA_BUILD" && zip -qr "$OLDPWD/$LAMBDA_OUT" . )
echo "built $LAMBDA_OUT ($(du -h "$LAMBDA_OUT" | cut -f1))"

# ----- 2) Skill-package zip (rooted at skill.json) -----
# The Alexa Console "Import skill" / ASK SMAPI rejects zips whose first entry
# is "skill-package/skill.json" with "package is not supported format". The zip
# MUST start at "skill.json" — we cd into skill-package/ and zip "." so the
# resulting archive has skill.json, interactionModels/, assets/ at its root.
PKG_OUT="$DIST/$SKILL-skill-package.zip"
rm -f "$PKG_OUT"
# Add skill.json first so it appears at the top of the archive, then the rest.
# What the Console actually validates is "skill.json exists at the zip root",
# regardless of order — but listing it first makes manual inspection obvious.
( cd "$PKG_DIR" && zip -q  "$OLDPWD/$PKG_OUT" skill.json \
                && zip -qr "$OLDPWD/$PKG_OUT" . -x skill.json )
echo "built $PKG_OUT ($(du -h "$PKG_OUT" | cut -f1))"

# Sanity check: skill.json must exist at the zip root (no nested directory).
# Read entries into a variable to avoid SIGPIPE under `set -o pipefail`.
ENTRIES="$(unzip -Z1 "$PKG_OUT")"
if ! grep -qx 'skill.json' <<<"$ENTRIES"; then
  echo "ERROR: $PKG_OUT has no top-level skill.json — Console will reject with 'package is not supported format'" >&2
  exit 1
fi
