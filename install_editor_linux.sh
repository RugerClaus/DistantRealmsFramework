#!/bin/bash
set -e

wget -O DR_Editor_Linux.zip https://snowblitz.net/downloads/dreditor/DR_Editor_Linux.zip

mkdir -p tools
echo "made directory tools"
echo "unzipping package"

unzip -d tools DR_Editor_Linux.zip

echo "package installed"
rm DR_Editor_Linux.zip

read -r -p "Would you like to run the editor now? [y/N] " answer

if [[ "$answer" =~ ^[Yy]$ ]]; then
    echo "opening editor..."
    ./run_editor.sh
else
    echo "run ```bash run_editor.sh``` to start the editor"
fi