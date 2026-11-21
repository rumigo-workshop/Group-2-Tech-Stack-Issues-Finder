# Group 2: Tech Stack Issues Finder

Tech Stack Issues Finder audits declared dependencies and versions against public CVE advisories, end-of-life timelines, and upgrade paths.

## Monorepo Layout

- `packages/web`: Frontend application (React + Vite)
- `packages/api`: Backend application (FastAPI)
- `packages/tests`: Integration tests and evaluation suites
- `packages/shared`: Shared types and data contracts
- `packages/db`: Database migrations and schema definitions
- `infra`: Infrastructure and container orchestration

## Services

### SearXNG (Search)
Web search component used during intelligence gathering.
- Port: `8080`
- Command: `docker compose up -d searxng`
- Test: `curl -i http://localhost:8080`

## Quickstart

Start service:
```bash
docker compose up -d searxng
```

Run service check:
```bash
# bash
./scripts/smoke_test_searxng.sh

# powershell
.\scripts\smoke_test_searxng.ps1
```
