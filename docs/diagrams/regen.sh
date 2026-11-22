#!/bin/sh
# Rebuild playbook-map.svg/.png from the plugin's playbooks. Run from anywhere.
set -e
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d); cd "$tmp"
python3 "$here/graph_data.py" graph.json
python3 "$here/build_map.py"            # writes map.data.json and map2.html (interactive page)
python3 "$here/export_map.py" map.data.json "$here"
