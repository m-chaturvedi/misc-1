#!/usr/bin/env bash
set -euo pipefail
PYTHON=python3.9

rm -rf venv
$PYTHON -m pip install virtualenv
$PYTHON -m virtualenv venv
source $PWD/venv/bin/activate
$PYTHON -m pip install -r requirements.txt
