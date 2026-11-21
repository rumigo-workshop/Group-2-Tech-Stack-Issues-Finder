# Group 2: Tech Stack Issues Finder

A developer enters a stack and versions and gets public advisories, CVEs, end-of-life dates and upgrade paths.

---

## Services & Infrastructure

### 1. SearXNG Search Service (Milestone 2.4 / Issue #11)
SearXNG handles the web search phase of the research pipeline. It queries the public web and requires **no API key**.

- **Port:** `8080`
- **Start:** `docker compose up -d searxng`
- **Smoke test with curl:**
  ```bash
  curl -i http://localhost:8080
  ```

---

### 2. Crawl4AI Scraper Service (Milestone 2.5 / Issue #12)
Crawl4AI handles the scraping phase of the research pipeline, extracting clean web content without needing an API key.

- **Port:** `11235`
- **Start:** `docker compose up -d crawl4ai`
- **Smoke test with curl:**
  ```bash
  curl -i http://localhost:11235/health
  ```

---

### Running Both Services Together
```bash
docker compose up -d
```

### Automated Smoke Tests
```bash
# On Linux/macOS
./scripts/smoke_test_searxng.sh
./scripts/smoke_test_crawl4ai.sh

# On Windows PowerShell
.\scripts\smoke_test_searxng.ps1
.\scripts\smoke_test_crawl4ai.ps1
```
