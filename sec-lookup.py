#!/usr/bin/env python3
"""SEC EDGAR + financial API lookup tool for stock analyst agent."""

import sys
import json
import os
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

USER_AGENT = "StockAnalyst contact@example.com"
SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

def load_env():
    """Load .env file from script directory."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

def sec_request(url):
    """Make a request to SEC API with required User-Agent."""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def ticker_to_cik(ticker):
    """Look up CIK from ticker using SEC company_tickers.json."""
    data = sec_request(SEC_TICKERS_URL)
    ticker_upper = ticker.upper()
    for entry in data.values():
        if entry.get("ticker") == ticker_upper:
            return str(entry["cik_str"])
    return None

def title_case_name(name):
    """Title-case a company name if it's ALL CAPS."""
    if name == name.upper():
        return name.title()
    return name

def get_filings(ticker, max_filings=5):
    """Get last N 10-K filings for a ticker."""
    cik = ticker_to_cik(ticker)
    if cik is None:
        print(f"Ticker '{ticker}' not found in SEC database", file=sys.stderr)
        sys.exit(2)

    padded_cik = cik.zfill(10)
    submissions = sec_request(SEC_SUBMISSIONS_URL.format(cik=padded_cik))

    company_name = title_case_name(submissions.get("name", ""))
    sic = submissions.get("sic", "")
    sic_desc = submissions.get("sicDescription", "")

    recent = submissions.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])

    cutoff = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

    filings = []
    for i in range(len(forms)):
        if forms[i] == "10-K" and dates[i] >= cutoff and len(filings) < max_filings:
            acc_clean = accessions[i].replace("-", "")
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_clean}/{primary_docs[i]}"
            filings.append({
                "form": "10-K",
                "date": dates[i],
                "url": url,
            })

    result = {
        "ticker": ticker.upper(),
        "cik": cik,
        "sic": sic,
        "sicDescription": sic_desc,
        "companyName": company_name,
        "filings": filings,
    }
    print(json.dumps(result, indent=2))

def get_research(ticker):
    """Placeholder — implemented in Task 2."""
    print('{"error": "not implemented"}', file=sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: sec-lookup.py <command> <TICKER>", file=sys.stderr)
        print("Commands: filings, research", file=sys.stderr)
        sys.exit(1)

    load_env()
    command = sys.argv[1]
    ticker = sys.argv[2]

    if command == "filings":
        get_filings(ticker)
    elif command == "research":
        get_research(ticker)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
