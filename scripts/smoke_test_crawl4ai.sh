#!/bin/bash
# Smoke test script for Crawl4AI service (Milestone 2.5 / Issue #12)
set -e

CRAWL4AI_URL="${CRAWL4AI_URL:-http://localhost:11235}"

echo "==> Testing Crawl4AI liveness at $CRAWL4AI_URL (no API key required)..."

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$CRAWL4AI_URL/health" || curl -s -o /dev/null -w "%{http_code}" "$CRAWL4AI_URL" || true)

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "302" ]; then
    echo " SUCCESS: Crawl4AI answered with HTTP status $HTTP_STATUS!"
    exit 0
else
    echo "❌ FAILURE: Crawl4AI returned HTTP status '$HTTP_STATUS'."
    exit 1
fi
