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

ASSETS_PATH="$ROOT/assets"
LOGS_PATH="$ROOT/logs"
SAVES_PATH="$ROOT/saves"
ENVIRONMENT_PATH="$ROOT/environment"

convert_to_windows_path() {
  local unix_path="$1"
  echo "$(cygpath -w "$unix_path")"
}

ASSETS_PATH_WIN=$(convert_to_windows_path "$ASSETS_PATH")
LOGS_PATH_WIN=$(convert_to_windows_path "$LOGS_PATH")
SAVES_PATH_WIN=$(convert_to_windows_path "$SAVES_PATH")
ENVIRONMENT_PATH_WIN=$(convert_to_windows_path "$ENVIRONMENT_PATH")

function copy_assets() {
  TARGET="$1"
  cp -r "$ASSETS_PATH" "$TARGET"
  cp -r "$LOGS_PATH" "$TARGET"
  cp -r "$SAVES_PATH" "$TARGET"
  cp -r "$ENVIRONMENT_PATH" "$TARGET"
  cp  "changelog.txt" "$TARGET"
  cp  "README.md" "$TARGET"
  cp  "instructions.md" "$TARGET"
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
  echo "Building Windows game executable..."

  TMP_DIST="$DIST_ROOT/windows_tmp"
  FINAL_DIST="$DIST_ROOT/windows"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --noconsole \
    --windowed \
    --clean \
    --name "$APP_NAME" \
    --add-data "$ASSETS_PATH_WIN;assets" \
    --add-data "$LOGS_PATH_WIN;logs" \
    --add-data "$SAVES_PATH_WIN;saves" \
    --add-data "$ENVIRONMENT_PATH_WIN/environment:environment" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/windows" \
    --specpath "$SPEC_ROOT/windows"

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"
  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/
  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
  cleanup_internal "$FINAL_DIST"
}

function build_updater() {
  echo "Building Windows updater executable..."

  TMP_DIST="$DIST_ROOT/updater_tmp"
  FINAL_DIST="$DIST_ROOT/windows"

  pyinstaller "$ROOT/$UPDATER_MAIN" \
    --onefile \
    --console \
    --clean \
    --name "$UPDATER_NAME" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/updater" \
    --specpath "$SPEC_ROOT/updater"

  mv "$TMP_DIST/$UPDATER_NAME.exe" "$FINAL_DIST/$UPDATER_NAME.exe"

  rm -rf "$TMP_DIST"
}

build_main

build_updater

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"

echo "Build completed."
rm -rf "$DIST_ROOT/_internal/assets"
