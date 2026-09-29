#!/bin/sh
set -eu
repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$target"
for d in "$repo_dir/skills"/*; do [ -d "$d" ] || continue; n=$(basename "$d"); if [ -e "$target/$n" ]; then echo "skip: $n"; else cp -R "$d" "$target/$n"; echo "installed: $n"; fi; done
echo "Restart Codex to load restored skills."
