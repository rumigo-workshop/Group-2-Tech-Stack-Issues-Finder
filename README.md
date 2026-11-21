# Group 2: Tech Stack Issues Finder

A developer enters a stack and versions and gets public advisories, CVEs, end-of-life dates and upgrade paths.

---

## Services & Infrastructure

### SearXNG Search Service (Milestone 2.4 / Issue #11)
SearXNG handles the web search phase of the research pipeline. It queries the public web and requires **no API key**.

#### Start SearXNG via Docker Compose:
```bash
docker compose up -d searxng
```

#### Smoke Test with curl:
```bash
curl -i http://localhost:8080
```
Or execute the automated smoke test script:
```bash
# On Linux/macOS
./scripts/smoke_test_searxng.sh

# On Windows PowerShell
.\scripts\smoke_test_searxng.ps1
```
