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
  cp -R "$ROOT/assets" "$TARGET"
  cp -R "$ROOT/logs" "$TARGET"
  cp -R "$ROOT/saves" "$TARGET"
  cp -R "$ROOT/environment" "$TARGET"
  cp "$ROOT/changelog.txt" "$TARGET"
}

function build_main() {
  echo "Building macOS game application..."

  TMP_DIST="$DIST_ROOT/macos_tmp"
  FINAL_DIST="$DIST_ROOT/macos"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --windowed \
    --icon="$ROOT/assets/images/build/mac.icns" \
    --clean \
    --name "$APP_NAME" \
    --add-data "$ROOT/assets:assets" \
    --add-data "$ROOT/logs:logs" \
    --add-data "$ROOT/saves:saves" \
    --add-data "$ROOT/environment:environment" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/macos" \
    --specpath "$SPEC_ROOT/macos"

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"

  mv "$TMP_DIST/$APP_NAME.app" "$FINAL_DIST/$APP_NAME.app"

  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"

  echo "Main macOS app built successfully."
}

function build_updater() {
  echo "Building macOS updater..."

  TMP_DIST="$DIST_ROOT/updater_tmp"
  FINAL_DIST="$DIST_ROOT/macos"

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

  echo "Updater built successfully."
}

build_main
build_updater

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"

echo "macOS build completed successfully."
