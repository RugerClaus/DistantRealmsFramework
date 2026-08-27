#!/bin/bash
set -e

CONFIG_NAME="$1"
DEPLOY=false

if [ "$2" == "--deploy" ]; then
  DEPLOY=true
fi

if [ -z "$CONFIG_NAME" ]; then
  echo "Usage: $0 <config> [--deploy]"
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/z-build_configuration/${CONFIG_NAME}.json"

if [ ! -f "$CONFIG" ]; then
  echo "Configuration not found: $CONFIG"
  exit 1
fi

APP_NAME=$(jq -r '.app_name' "$CONFIG")
MAIN=$(jq -r '.main' "$CONFIG")
UPDATER_MAIN=$(jq -r '.updater_main' "$CONFIG")
UPDATER_NAME=$(jq -r '.updater_name' "$CONFIG")

DIST_ROOT="$ROOT/$(jq -r '.paths.dist' "$CONFIG")"
WORK_ROOT="$ROOT/$(jq -r '.paths.build' "$CONFIG")"
SPEC_ROOT="$ROOT/$(jq -r '.paths.specs' "$CONFIG")"

BUILD_MODE=$(jq -r '.build.mode' "$CONFIG")
WINDOWED=$(jq -r '.build.windowed' "$CONFIG")
NOCONSOLE=$(jq -r '.build.noconsole' "$CONFIG")
DEBUG=$(jq -r '.build.debug' "$CONFIG")

UPDATER_ENABLED=$(jq -r '.updater.enabled' "$CONFIG")
UPDATER_MODE=$(jq -r '.updater.mode' "$CONFIG")
UPDATER_CONSOLE=$(jq -r '.updater.console' "$CONFIG")

ARCHIVE_ENABLED=$(jq -r '.archive.enabled' "$CONFIG")
ARCHIVE_NAME=$(jq -r '.archive.name' "$CONFIG")
ARCHIVE_DIRECTORY=$(jq -r '.archive.directory' "$CONFIG")

SERVER=$(jq -r '.deployment.server' "$CONFIG")
REMOTE_DIR=$(jq -r '.deployment.remote_dir' "$CONFIG")


function convert_to_windows_path() {
  local unix_path="$1"
  echo "$(cygpath -w "$unix_path")"
}


function copy_assets() {
  TARGET="$1"

  echo "Copying application files..."

  while IFS= read -r FILE; do
    cp -r "$ROOT/$FILE" "$TARGET"
  done < <(jq -r '.assets[]' "$CONFIG")

  while IFS= read -r FILE; do
    cp -r "$ROOT/$FILE" "$TARGET"
  done < <(jq -r '.copy[]' "$CONFIG")

  mkdir -p "$TARGET/logs"
}


function cleanup_internal() {
  INTERNAL_DIR="$1/_internal"

  if [ -d "$INTERNAL_DIR" ]; then
    echo "Cleaning up _internal directory..."

    while IFS= read -r FILE; do
      rm -rf "$INTERNAL_DIR/$FILE"
    done < <(jq -r '.cleanup_internal[]' "$CONFIG")
  fi
}


function build_main() {
  echo "Building $APP_NAME Windows executable..."

  TMP_DIST="$DIST_ROOT/${APP_NAME}_tmp"
  FINAL_DIST="$DIST_ROOT/$APP_NAME"

  rm -rf "$TMP_DIST"

  ASSETS_PATH_WIN=$(convert_to_windows_path "$ROOT/assets")
  SAVES_PATH_WIN=$(convert_to_windows_path "$ROOT/saves")
  ENVIRONMENT_PATH_WIN=$(convert_to_windows_path "$ROOT/environment")

  pyinstaller "$ROOT/$MAIN" \
    "--$BUILD_MODE" \
    --icon="$ASSETS_PATH_WIN/images/build/${APP_NAME}.png" \
    --clean \
    --name "$APP_NAME" \
    --contents-directory distantrealms \
    --add-data "$ASSETS_PATH_WIN;assets" \
    --add-data "$SAVES_PATH_WIN;saves" \
    --add-data "$ENVIRONMENT_PATH_WIN;environment" \
    --add-data "$(convert_to_windows_path "$ROOT/logs");logs" \
    $(if [ "$WINDOWED" == "true" ]; then echo "--windowed"; fi) \
    $(if [ "$NOCONSOLE" == "true" ]; then echo "--noconsole"; fi) \
    $(if [ "$DEBUG" == "true" ]; then echo "--debug all"; fi) \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/$APP_NAME" \
    --specpath "$SPEC_ROOT/$APP_NAME"

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"

  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/
  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
  cleanup_internal "$FINAL_DIST"
}


function build_updater() {
  if [ "$UPDATER_ENABLED" != "true" ]; then
    echo "Updater disabled."
    return
  fi

  echo "Building Windows updater executable..."

  TMP_DIST="$DIST_ROOT/updater_tmp"
  FINAL_DIST="$DIST_ROOT/$APP_NAME"

  rm -rf "$TMP_DIST"

  pyinstaller "$ROOT/$UPDATER_MAIN" \
    "--$UPDATER_MODE" \
    --clean \
    --name "$UPDATER_NAME" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/updater" \
    --specpath "$SPEC_ROOT/updater" \
    $(if [ "$UPDATER_CONSOLE" == "true" ]; then echo "--console"; fi)

  mv "$TMP_DIST/$UPDATER_NAME.exe" "$FINAL_DIST/$UPDATER_NAME.exe"

  rm -rf "$TMP_DIST"
}


function zip_build() {
  if [ "$ARCHIVE_ENABLED" != "true" ]; then
    return
  fi

  FINAL_DIST="$DIST_ROOT/$APP_NAME"
  ZIP_FILE="$DIST_ROOT/$ARCHIVE_NAME"
  UPDATE_TMP="$DIST_ROOT/update_tmp"

  echo "Creating $ZIP_FILE..."

  rm -f "$ZIP_FILE"
  rm -rf "$UPDATE_TMP"

  mkdir -p "$UPDATE_TMP/$ARCHIVE_DIRECTORY"

  cp -r "$FINAL_DIST"/. "$UPDATE_TMP/$ARCHIVE_DIRECTORY"/

  cd "$UPDATE_TMP"
  zip -r "$ZIP_FILE" "$ARCHIVE_DIRECTORY"

  cd "$ROOT"

  rm -rf "$UPDATE_TMP"

  echo "Archive created."
}


function deploy_build() {
  if [ "$ARCHIVE_ENABLED" != "true" ]; then
    echo "Deployment requires an archive."
    exit 1
  fi

  ZIP_FILE="$DIST_ROOT/$ARCHIVE_NAME"

  if [ ! -f "$ZIP_FILE" ]; then
    echo "Archive not found: $ZIP_FILE"
    exit 1
  fi

  echo "Deploying $ARCHIVE_NAME to $SERVER:$REMOTE_DIR..."

  sftp "$SERVER" <<EOF
cd $REMOTE_DIR
put $ZIP_FILE
EOF

  echo "Deployment completed."
}


build_main

build_updater

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"

if [ "$ARCHIVE_ENABLED" == "true" ]; then
  zip_build
fi

rm -rf "$DIST_ROOT/_internal/assets"

if [ "$DEPLOY" = true ]; then
  deploy_build
else
  echo "Skipping deployment."
fi

echo "Build completed."