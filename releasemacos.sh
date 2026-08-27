#!/bin/bash

set -e

DEPLOY=""

if [ "$1" == "--deploy" ]; then
    DEPLOY="--deploy"
fi

./z-build/buildmacos.sh releasemacos $DEPLOY && \
./z-build/buildmacos.sh updatemacos $DEPLOY

APP_NAME=$(python3 -c "from config import config; print(config['TITLE'])")
VERSION=$(python3 -c "from config import config; print(config['VERSION'])")
OS=$(python3 -c "from config import config; print(config['OS'])")

ARCHIVE="freeze_source/${APP_NAME}-${VERSION}-${OS}.zip"

mkdir -p freeze_source

rm -f "$ARCHIVE"

zip -r "$ARCHIVE" . \
    -x ".git/*" \
    -x "freeze_source/*" \
    -x "$ARCHIVE"

echo "Created $ARCHIVE"