#!/bin/bash
# Smoke test script for SearXNG service (Milestone 2.4 / Issue #11)
set -e

SEARXNG_URL="${SEARXNG_URL:-http://localhost:8080}"

echo "==> Testing SearXNG liveness at $SEARXNG_URL (no API key required)..."

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SEARXNG_URL" || true)

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "302" ]; then
    echo " SUCCESS: SearXNG answered with HTTP status $HTTP_STATUS!"
    exit 0
else
    echo "❌ FAILURE: SearXNG returned HTTP status '$HTTP_STATUS'."
    exit 1
fi
