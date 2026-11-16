#!/bin/sh
# Deploy to production
git pull
uv sync
uv run python -m tablerito
