#!/usr/bin/env bash


nginx & 

exec uv run uvicorn main:app --host 0.0.0.0 --port 8080