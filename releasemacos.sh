#!/bin/bash

set -e

DEPLOY=""

if [ "$1" == "--deploy" ]; then
    DEPLOY="--deploy"
fi

./z-build/buildmacos.sh releasemacos $DEPLOY && \
./z-build/buildmacos.sh updatemacos $DEPLOY