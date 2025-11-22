# LLM Engineer Handbook Twin

A lightweight ETL + Crawling + DB scaffold to build an LLM-powered "twin" from personal/professional data sources (e.g., GitHub, LinkedIn). This is an early, concise README; we’ll expand it as more code lands.

**Status:** Work in progress. Interfaces and scripts may change.

## Overview
- **ETL:** a pipeline composed of steps to crawl links, fetch profiles/repos, and persist normalized documents.
- **DB:** MongoDB with simple document models for storage and retrieval and Qdrant as a vector DB.
- **Experiments:** random space for experimenting while learning.
- **Feature:** the pipeline to extract features from the data warehouse and store them to the feature store

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


Run ETL (placeholder entrypoint):
```bash
PYTHONPATH=. python ETL/run.py
```

## Contributing
Issues and PRs are welcome. Since this is evolving, please keep changes small and focused.

