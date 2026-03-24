# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SANC (Stock Analyst Named Claude) — a toolkit that combines SEC EDGAR filings with financial APIs to produce structured equity research (bull/bear cases, industry primers, quarterly updates). Follows a source-discipline methodology where all claims must cite specific documents.

## Commands

```bash
# Fetch 5 years of 10-K filings for a ticker
python sanc.py filings <TICKER>

# Fetch last 4 quarterly 10-Q filings for a ticker
python sanc.py quarterly <TICKER>

# Gather supplementary research (analyst ratings, news, earnings)
python sanc.py research <TICKER>

# Run tests (integration tests hitting live APIs)
pytest test_sanc.py -v
```

## Architecture

**`sanc.py`** — CLI tool with three subcommands:
- `filings`: SEC EDGAR CIK lookup → 10-K filing metadata (URLs, dates, SIC code). Hardcoded 5-year filter.
- `quarterly`: SEC EDGAR → last 4 10-Q quarterly filing metadata.
- `research`: Aggregates data from Finnhub (analyst recs, peers, earnings), MarketAux (news sentiment), and Alpha Vantage (financials, quarterly earnings). Graceful degradation — succeeds if at least one API returns data.

**Per-ticker directories** (e.g., `FANG/`, `TRGP/`):
- `filings.json` / `quarterly-filings.json` / `research-data.json` — raw API outputs
- `bull-case.md` — Peter Lynch 8-part investment pitch
- `bear-case.md` — Charlie Munger inversion analysis
- Media artifacts: `podcast.mp3`, `infographic.png`, `business-structure.png`, `sankey-flow.png`, `slides.pptx` (from NotebookLM)

**`prompts/`** — NotebookLM prompt templates for infographic generation (business-structure, sankey-flow).

**`industries/`** — Sector fundamentals documents that establish baseline context for company analysis.

**`build-your-own-stock-analyst-with-claude.md`** — Strategy guide defining the 5-phase analysis pipeline and prompt templates for bull/bear cases.

## Environment

API keys loaded from `.env` (gitignored):
- `FINNHUB_API_KEY`
- `MARKETAUX_API_TOKEN`
- `ALPHAVANTAGE_API_KEY`

`PYTHONIOENCODING=utf-8` is set in `.claude/settings.local.json` for Unicode output.

## Exit Codes (sanc.py)

- 0: Success
- 1: All research APIs failed
- 2: Unknown ticker

## Analysis Methodology

The project enforces **source discipline**: every claim cites its document (10-K, transcript, article), quotes come before interpretation, and inferences are explicitly marked. This is core to how analysis documents should be written.
