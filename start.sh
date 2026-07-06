#!/usr/bin/env bash

nginx & uv run uvicorn main:app --host 0.0.0.0 --port 8080