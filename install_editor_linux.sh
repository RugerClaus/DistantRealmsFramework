#!/bin/bash
set -e

wget -O DR_Editor_Linux.zip https://snowblitz.net/downloads/dreditor/DR_Editor_Linux.zip

mkdir -p tools
echo "made directory tools"
echo "unzipping package"

unzip -d tools DR_Editor_Linux.zip

echo "package installed"
rm DR_Editor_Linux.zip