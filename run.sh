#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Run the app using the port specified in the PORT environment variable.
env $(grep -v '^#' .env | xargs) python -m debugpy --listen localhost:5678 --wait-for-client -m uvicorn "main:app" --port "${PORT:-8000}"