#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Create a virtual environment if it doesn't exist. Otherwise, activate it.
if [[ ! -d "${SCRIPT_DIR}/.venv" ]]; then
    python3 -m venv "${SCRIPT_DIR}/.venv"
    source "${SCRIPT_DIR}/.venv/bin/activate"
    python -m pip install --upgrade pip
    pip install -U -r ${SCRIPT_DIR}/requirements_dev.txt
else
    source "${SCRIPT_DIR}/.venv/bin/activate"
fi

# Run the app using the port specified in the PORT environment variable.
python -m debugpy --listen localhost:5678 --wait-for-client -m uvicorn "main:app" --port "${PORT:-8000}"