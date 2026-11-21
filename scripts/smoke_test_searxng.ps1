# Windows PowerShell smoke test for SearXNG service (Milestone 2.4 / Issue #11)
$url = if ($env:SEARXNG_URL) { $env:SEARXNG_URL } else { "http://localhost:8080" }

Write-Host "==> Testing SearXNG liveness at $url (no API key required)..."
try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
    Write-Host " SUCCESS: SearXNG responded with status code $($response.StatusCode)!" -ForegroundColor Green
} catch {
    Write-Host "❌ SearXNG is unreachable at $url. Ensure 'docker compose up searxng' is running." -ForegroundColor Red
}
