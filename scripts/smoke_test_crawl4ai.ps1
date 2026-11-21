# Windows PowerShell smoke test for Crawl4AI service (Milestone 2.5 / Issue #12)
$url = if ($env:CRAWL4AI_URL) { $env:CRAWL4AI_URL } else { "http://localhost:11235/health" }

Write-Host "==> Testing Crawl4AI liveness at $url (no API key required)..."
try {
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
    Write-Host " SUCCESS: Crawl4AI responded with status code $($response.StatusCode)!" -ForegroundColor Green
} catch {
    Write-Host "❌ Crawl4AI is unreachable at $url. Ensure 'docker compose up crawl4ai' is running." -ForegroundColor Red
}
