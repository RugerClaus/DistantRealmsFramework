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

./z-build/buildlinux.sh snapshotmacos $DEPLOY