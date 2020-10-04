#!/usr/bin/env bash

CURRENT_DIR="$(dirname "$0")"
ROOT_DIR="$CURRENT_DIR/../packages/database/"

(cd $ROOT_DIR && pipenv run python . "$@")
