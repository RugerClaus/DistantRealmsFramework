#!/bin/bash
set -e

APP_NAME="snowblitz"
MAIN="main.py"
UPDATER_MAIN="updater.py"
UPDATER_NAME="updater"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_ROOT="$ROOT/executable"
WORK_ROOT="$ROOT/build"
SPEC_ROOT="$ROOT/specs"

function copy_assets() {
  TARGET="$1"
  cp -r "$ROOT/assets" "$TARGET"
  cp -r "$ROOT/logs" "$TARGET"
  cp -r "$ROOT/saves" "$TARGET"
  cp -r "$ROOT/environment" "$TARGET"
  cp "$ROOT/changelog.txt" "$TARGET"
  cp "$ROOT/README.md" "$TARGET"
  cp "$ROOT/LICENSE" "$TARGET"
  cp "$ROOT/instructions.md" "$TARGET"
}

function cleanup_internal() {
  INTERNAL_DIR="$1/_internal"

  if [ -d "$INTERNAL_DIR" ]; then
    echo "Cleaning up _internal directory..."
    rm -rf "$INTERNAL_DIR/assets"
    rm -rf "$INTERNAL_DIR/logs"
    rm -rf "$INTERNAL_DIR/saves"
    rm -rf "$INTERNAL_DIR/environment"
  fi
}

function build_main() {
  echo "Building Linux game executable..."

  TMP_DIST="$DIST_ROOT/linux_tmp"
  FINAL_DIST="$DIST_ROOT/linux"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --icon="assets/images/build/linux.png" \
    --noconsole \
    --windowed \
    --clean \
    --name "$APP_NAME" \
    --add-data "$ROOT/assets:assets" \
    --add-data "$ROOT/logs:logs" \
    --add-data "$ROOT/saves:saves" \
    --add-data "$ROOT/environment:environment" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/linux" \
    --specpath "$SPEC_ROOT/linux" \
    --debug all

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"
  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/
  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
  cleanup_internal "$FINAL_DIST"
}

function build_updater() {
  echo "Building Linux updater executable..."

  TMP_DIST="$DIST_ROOT/updater_tmp"
  FINAL_DIST="$DIST_ROOT/linux"

  pyinstaller "$ROOT/$UPDATER_MAIN" \
    --onefile \
    --console \
    --clean \
    --name "$UPDATER_NAME" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/updater" \
    --specpath "$SPEC_ROOT/updater"

  mv "$TMP_DIST/$UPDATER_NAME" "$FINAL_DIST/$UPDATER_NAME"

  rm -rf "$TMP_DIST"
}

build_main

build_updater

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"

echo "Build completed."
rm -rf "$DIST_ROOT/_internal/assets"
