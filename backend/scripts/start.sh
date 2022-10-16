#!/usr/bin/env bash

set -e

uvicorn --host=0.0.0.0 --port="${PORT}" app.__main__:app