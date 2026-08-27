#!/bin/bash

set -e

DEPLOY=""

if [ "$1" == "--deploy" ]; then
    DEPLOY="--deploy"
fi

./z-build/buildwindows.sh releasewindows $DEPLOY && \
./z-build/buildwindows.sh updatewindows $DEPLOY