#!/usr/bin/env bash

_script_dir="$(readlink -f "$0" | xargs dirname)"

user_id="$(id -u)"

homedir="$HOME"

## important thing lerned today: for host volume mounts to work, you need to have global +x on any parent dir, so on default mounting home subdirs does not work!!!

dtag="main"
dimg="ghcr.io/sma-de/docker-jinja2-renderer:${dtag}"

## make sure image is up to date
sudo docker pull "${dimg}"

## open dev env inside container
sudo docker run --rm --userns=host -ti --net host \
  -e http_proxy="$http_proxy" \
  -e HTTP_PROXY="$http_proxy" \
  -e https_proxy="$https_proxy" \
  -e HTTPS_PROXY="$https_proxy" \
  -e HOME="$HOME" \
  -u "$user_id:$user_id" -w "${_script_dir}" \
  -v /etc/passwd:/etc/passwd \
  -v "${homedir}":"${homedir}" \
  --entrypoint /bin/sh \
  "${dimg}" -c sh

