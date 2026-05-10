#!/usr/bin/env bash
# Build a deployable Lambda zip for an Alexa skill in this repo.
# Usage: bash .claude/skills/package-lambda/build.sh <skill-name>

set -euo pipefail

SKILL="${1:-}"
if [[ -z "$SKILL" ]]; then
  echo "usage: build.sh <skill-name>" >&2
  ls skills 2>/dev/null | sed 's/^/  /' >&2
  exit 2
fi

LAMBDA_DIR="skills/$SKILL/lambda"
SRC="$LAMBDA_DIR/lambda_function.py"
REQ="$LAMBDA_DIR/requirements.txt"

if [[ ! -f "$SRC" ]]; then
  echo "no lambda_function.py at $SRC" >&2
  exit 1
fi

BUILD="$(mktemp -d)"
DIST="dist"
mkdir -p "$DIST"
trap 'rm -rf "$BUILD"' EXIT

# Install deps from requirements.txt, targeting Lambda's Linux x86_64 runtime.
# Without these flags, pip on macOS pulls darwin wheels that fail to import on Lambda.
if [[ -s "$REQ" ]]; then
  PY_VER="${LAMBDA_PY_VER:-3.12}"
  echo "bundling deps for Lambda python${PY_VER} (linux x86_64) from $REQ"
  python3 -m pip install --quiet --target "$BUILD" \
    --platform manylinux2014_x86_64 \
    --python-version "$PY_VER" \
    --implementation cp \
    --only-binary=:all: \
    -r "$REQ"
fi

# Copy all .py files from the lambda dir (handler + any helper modules).
cp "$LAMBDA_DIR"/*.py "$BUILD/"

OUT="$DIST/$SKILL.zip"
rm -f "$OUT"
( cd "$BUILD" && zip -qr "$OLDPWD/$OUT" . )

echo "built $OUT ($(du -h "$OUT" | cut -f1))"
