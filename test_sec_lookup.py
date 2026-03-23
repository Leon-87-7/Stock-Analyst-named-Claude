import subprocess, json, os
from datetime import datetime, timedelta

SCRIPT = os.path.join(os.path.dirname(__file__), "sec-lookup.py")
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
