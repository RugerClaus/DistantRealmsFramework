#!/bin/bash
set -e

DEPLOY=""

if [ "$#" -gt 0 ]; then
    if [ "$1" == "--deploy" ]; then
        DEPLOY="--deploy"
    else
        echo "Usage: $0 [--deploy]"
        exit 1
    fi
fi

./z-build/buildlinux.sh snapshotwindows $DEPLOY

APP_NAME=$(python3 -c "from config import config; print(config['TITLE'])")
VERSION=$(python3 -c "from config import config; print(config['VERSION'])")
OS=$(python3 -c "from config import config; print(config['OS'])")

ARCHIVE="freeze_source/${APP_NAME}-${VERSION}-${OS}.zip"

mkdir -p freeze_source

rm -f "$ARCHIVE"

zip -r "$ARCHIVE" . \
    -x ".git/*" \
    -x "config.py" \
    -x "freeze_source/*" \
    -x "$ARCHIVE"

echo "Created $ARCHIVE"