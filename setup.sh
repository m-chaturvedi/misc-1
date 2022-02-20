#!/usr/bin/env bash
set -euo pipefail
PYTHON=python3.9

$PYTHON -m pip install virtualenv
rm -rf venv
$PYTHON -m virtualenv venv
source $PWD/venv/bin/activate
$PYTHON -m pip install -r requirements.txt
