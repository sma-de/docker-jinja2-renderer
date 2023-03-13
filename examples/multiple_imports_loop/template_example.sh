#!/bin/sh

_script_dir="$(readlink -f "$0" | xargs dirname)"

./sma-jinja-renderer.py "${_script_dir}" -r -f -i "${_script_dir}/imports"

cat "${_script_dir}/main.yml"

