# LLM Engineer Handbook Twin

A lightweight ETL + Crawling + DB scaffold to build an LLM-powered "twin" from personal/professional data sources (e.g., GitHub, LinkedIn). This is an early, concise README; we’ll expand it as more code lands.

**Status:** Work in progress. Interfaces and scripts may change.

## Overview
- **ETL:** Orchestrates steps to crawl links, fetch profiles/repos, and persist normalized documents.
- **Crawlers:** Pluggable crawlers (GitHub, LinkedIn, Custom) via a simple base interface and dispatcher.
- **DB:** MongoDB integration with simple document models for storage and retrieval.
- **Experiments:** Scratch space for encoders and LinkedIn export tooling.

## Repo Structure
- `ETL/`: Pipeline runner and steps
	- `pipeline.py`, `run.py`
	- `Steps/`: `crawl_links.py`, `get_or_create_user.py`
	- `Crawlers/`: `githubCrawler.py`, `linkedinCrawler.py`, `customCrawler.py`, `crawlerDispatcher.py`, `baseCrawler.py`
- `DB/`: Database layer
	- `mongo.py`, `models/` (e.g., `documents.py`, `noSqlBaseDocument.py`), `types/`
- `experiments/`: Prototypes (e.g., `Encoders/educational.py`, `LinkedinCrawling/` Node script)
- `utils/`: Helpers like `exceptions.py`, `strings.py`

## Quickstart
Prerequisites:
- Python 3.10+
- MongoDB (local or cloud URI)
- Node.js 18+ (only for LinkedIn experiment under `experiments/LinkedinCrawling`)

Setup (Python):
```bash
python -m venv .venv
source .venv/Scripts/activate
# Requirements file will be added soon
pip install -r requirements.txt || echo "(requirements.txt pending)"
```

Environment (examples; adjust as needed):
```bash
export MONGO_URI="mongodb://localhost:27017/llm_twin"
# export GITHUB_TOKEN="<optional>"
# export LINKEDIN_COOKIES="<optional>"
```

Run ETL (placeholder entrypoint):
```bash
python ETL/run.py
```

LinkedIn experiment (optional):
```bash
cd experiments/LinkedinCrawling
pnpm install
node export.js
```

## Roadmap (Short)
- Add `requirements.txt` and `.env.example`
- Finalize ETL steps and crawler configs
- Document data schemas and examples
- Add tests and CI hooks

## Contributing
Issues and PRs are welcome. Since this is evolving, please keep changes small and focused.

