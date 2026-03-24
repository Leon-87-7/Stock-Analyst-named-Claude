import subprocess, json, os
from datetime import datetime, timedelta

SCRIPT = os.path.join(os.path.dirname(__file__), "sanc.py")
BASE = os.path.dirname(__file__)

def run(cmd):
    result = subprocess.run(
        ["python", SCRIPT] + cmd,
        capture_output=True, text=True, cwd=BASE
    )
    return result

def test_filings_returns_valid_json_for_known_ticker():
    result = run(["filings", "AAPL"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["ticker"] == "AAPL"
    assert data["cik"] == "320193"
    assert data["companyName"] != ""
    assert data["sic"] != ""
    assert data["sicDescription"] != ""
    assert len(data["filings"]) <= 5
    assert len(data["filings"]) > 0
    cutoff = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
    for f in data["filings"]:
        assert f["form"] == "10-K"
        assert f["url"].startswith("https://www.sec.gov/Archives/")
        assert f["date"] >= cutoff, f"Filing date {f['date']} is older than 5 years"

def test_filings_unknown_ticker_exits_2():
    result = run(["filings", "ZZZZZNOTREAL"])
    assert result.returncode == 2

def test_research_returns_valid_json_for_known_ticker():
    result = run(["research", "AAPL"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["ticker"] == "AAPL"
    # At least one API section should have data
    has_data = any(data.get(k) is not None for k in ["finnhub", "marketaux", "alphavantage"])
    assert has_data, "All API sections returned null"

def test_research_partial_failure_still_exits_0():
    """If at least one API works, exit 0 even if others fail."""
    result = run(["research", "AAPL"])
    assert result.returncode == 0
    data = json.loads(result.stdout)
    # Verify structure: each section is either a dict/list or null
    for key in ["finnhub", "marketaux", "alphavantage"]:
        assert key in data

def test_quarterly_returns_valid_json_for_known_ticker():
    result = run(["quarterly", "AAPL"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
    data = json.loads(result.stdout)
    assert data["ticker"] == "AAPL"
    assert data["companyName"] != ""
    assert len(data["filings"]) <= 4
    assert len(data["filings"]) > 0
    for f in data["filings"]:
        assert f["form"] == "10-Q"
        assert f["url"].startswith("https://www.sec.gov/Archives/")

def test_quarterly_unknown_ticker_exits_2():
    result = run(["quarterly", "ZZZZZNOTREAL"])
    assert result.returncode == 2
