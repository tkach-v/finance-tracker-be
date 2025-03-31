#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

uv run manage.py migrate
uv run manage.py runserver 0.0.0.0:8000