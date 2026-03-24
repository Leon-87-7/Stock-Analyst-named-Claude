# SANC Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename CLI to `sanc`, add 10-Q quarterly filings, make the agentic pipeline fully hands-free, and add two new infographic prompts (business structure + Sankey flow).

**Architecture:** Rename `sec-lookup.py` → `sanc.py` and update all references across agents, tests, settings, and CLAUDE.md. Extend the SEC filings function with a `quarterly` command for 10-Q reports. Add new prompts and wire them into the stock-ticker-agent's Phase 4. Update permissions so the full pipeline runs without approval prompts.

**Tech Stack:** Python 3 stdlib, pytest, NotebookLM CLI, Claude Code agents

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `sec-lookup.py` → `sanc.py` | Rename + modify | CLI tool: add `quarterly` command |
| `test_sec_lookup.py` → `test_sanc.py` | Rename + modify | Tests: update imports, add 10-Q tests |
| `.claude/settings.local.json` | Modify | Permissions: rename refs, add `python sanc.py:*`, broaden for hands-free |
| `CLAUDE.md` | Modify | Update command references |
| `.claude/agents/stock-analyst.md` | Modify | Update `sec-lookup.py` → `sanc.py` refs |
| `.claude/agents/stock-ticker-agent.md` | Modify | Update CLI refs, add Phase 4 infographics |
| `prompts/business-structure.md` | Create | New prompt: 5-year business structure infographic |
| `prompts/sankey-flow.md` | Already exists | Sankey flow infographic prompt |

---

### Task 1: Rename `sec-lookup.py` to `sanc.py`

**Files:**
- Rename: `sec-lookup.py` → `sanc.py`
- Modify: `sanc.py` (update usage string)

- [ ] **Step 1: Git-rename the file**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git mv sec-lookup.py sanc.py
```

- [ ] **Step 2: Update the usage string inside sanc.py**

In `sanc.py`, change:
```python
print("Usage: sec-lookup.py <command> <TICKER>", file=sys.stderr)
```
to:
```python
print("Usage: sanc <command> <TICKER>", file=sys.stderr)
```

Also update the module docstring from:
```python
"""SEC EDGAR + financial API lookup tool for stock analyst agent."""
```
to:
```python
"""SANC — Stock Analyst Named Claude. SEC EDGAR + financial API CLI."""
```

- [ ] **Step 3: Verify the renamed script runs**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && python sanc.py filings AAPL 2>&1 | head -5
```
Expected: JSON output starting with `{` containing `"ticker": "AAPL"`

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git add sanc.py && git commit -m "refactor: rename sec-lookup.py to sanc.py"
```

---

### Task 2: Rename and update tests

**Files:**
- Rename: `test_sec_lookup.py` → `test_sanc.py`
- Modify: `test_sanc.py` (update SCRIPT reference)

- [ ] **Step 1: Git-rename the test file**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git mv test_sec_lookup.py test_sanc.py
```

- [ ] **Step 2: Update the SCRIPT path inside test_sanc.py**

Change:
```python
SCRIPT = os.path.join(os.path.dirname(__file__), "sec-lookup.py")
```
to:
```python
SCRIPT = os.path.join(os.path.dirname(__file__), "sanc.py")
```

- [ ] **Step 3: Run existing tests to verify nothing broke**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && pytest test_sanc.py -v
```
Expected: All 4 tests PASS

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git add test_sanc.py && git commit -m "refactor: rename test file to test_sanc.py"
```

---

### Task 3: Add `quarterly` command (10-Q filings)

**Files:**
- Modify: `sanc.py` (add `get_quarterly` function, update `main`)
- Modify: `test_sanc.py` (add 10-Q tests)

- [ ] **Step 1: Write the failing test for quarterly command**

Append to `test_sanc.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && pytest test_sanc.py::test_quarterly_returns_valid_json_for_known_ticker -v
```
Expected: FAIL — unknown command "quarterly"

- [ ] **Step 3: Add `get_quarterly` function to sanc.py**

Add this function after `get_filings`:

```python
def get_quarterly(ticker, max_filings=4):
    """Get last 4 10-Q quarterly filings for a ticker."""
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

    filings = []
    for i in range(len(forms)):
        if forms[i] == "10-Q" and len(filings) < max_filings:
            acc_clean = accessions[i].replace("-", "")
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_clean}/{primary_docs[i]}"
            filings.append({
                "form": "10-Q",
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
```

Update the `main()` function — add the `quarterly` branch and update usage:

```python
def main():
    if len(sys.argv) < 3:
        print("Usage: sanc <command> <TICKER>", file=sys.stderr)
        print("Commands: filings, quarterly, research", file=sys.stderr)
        sys.exit(1)

    load_env()
    command = sys.argv[1]
    ticker = sys.argv[2]

    if command == "filings":
        get_filings(ticker)
    elif command == "quarterly":
        get_quarterly(ticker)
    elif command == "research":
        get_research(ticker)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 4: Run all tests**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && pytest test_sanc.py -v
```
Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git add sanc.py test_sanc.py && git commit -m "feat: add quarterly command for 10-Q filings"
```

---

### Task 4: Create business structure infographic prompt

**Files:**
- Create: `prompts/business-structure.md`

- [ ] **Step 1: Write the prompt**

Create `prompts/business-structure.md`:

```markdown
You are a business analyst and data visualization designer. Using all relevant sources in this NotebookLM project, create a comprehensive business structure infographic for [COMPANY NAME] covering the last 5 fiscal years, with detailed focus on the most recent year broken down by quarter.

The infographic should include:

## 5-Year Overview (Annual)
- Revenue and net income trend (5 years)
- Business segment breakdown and how it evolved
- Key acquisitions, divestitures, or structural changes
- Headcount or operational scale markers
- Debt/equity structure changes

## Recent Year Deep Dive (Quarterly)
- Quarter-by-quarter revenue, operating income, and margins
- Segment performance by quarter — which segments accelerated or decelerated
- Capital allocation decisions each quarter (capex, buybacks, dividends, M&A)
- Management guidance vs. actual results per quarter
- Any one-time items, restructuring charges, or unusual events

## Visual Structure
- Top section: 5-year timeline with key milestones and annual metrics
- Bottom section: 4-panel quarterly breakdown of the most recent fiscal year
- Use consistent color coding: one color per business segment across all views
- Annotate inflection points (e.g., "Acquired X in Q2", "New segment reporting in FY2023")

Keep all numbers sourced from the uploaded documents. Flag any estimates or inferences. Use concise labels suitable for an infographic layout.
```

- [ ] **Step 2: Commit**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git add prompts/business-structure.md && git commit -m "feat: add business structure infographic prompt"
```

---

### Task 5: Update stock-ticker-agent to use `sanc.py`, add 10-Q, add new infographics

**Files:**
- Modify: `C:\Users\leone\.claude\agents\stock-ticker-agent.md`

- [ ] **Step 1: Update all `sec-lookup.py` references to `sanc.py`**

In `stock-ticker-agent.md`:
- Phase 1 step 1: `python sec-lookup.py filings {ticker}` → `python sanc.py filings {ticker}`
- Phase 3 step 1: `python sec-lookup.py research {ticker}` → `python sanc.py research {ticker}`

- [ ] **Step 2: Add Phase 1.5 — Quarterly Filing Lookup**

After Phase 1 step 4 (save filings.json), add:

```markdown
## Phase 1.5: Quarterly Filing Lookup (10-Q)

1. Run: `cd "{base_dir}" && python sanc.py quarterly {ticker}`
2. Parse the JSON output. Extract the 10-Q filings list.
3. Save to `{base_dir}/{ticker}/quarterly-filings.json`
4. Add each 10-Q filing URL as a source to the notebook:
   ```bash
   notebooklm source add "{url}" --notebook {notebook_id} --json
   ```
   Capture each `source_id`.
5. Wait for all sources to be indexed:
   ```bash
   notebooklm source wait {source_id} --notebook {notebook_id} --timeout 600
   ```
   If a source fails, log a warning and continue.
```

- [ ] **Step 3: Add new infographic generations to Phase 4**

In Phase 4, after the existing 3 `notebooklm generate` commands, add:

```markdown
4. Business Structure Infographic:
   Read the prompt from `{base_dir}/prompts/business-structure.md`. Substitute `[COMPANY NAME]` with `companyName`.
   ```bash
   notebooklm generate infographic --prompt "{business_structure_prompt}" --detail detailed --style professional --notebook {notebook_id} --json
   ```

5. Sankey Flow Infographic:
   Read the prompt from `{base_dir}/prompts/sankey-flow.md`. Substitute `[COMPANY NAME]` with `companyName`.
   ```bash
   notebooklm generate infographic --prompt "{sankey_flow_prompt}" --detail detailed --style professional --notebook {notebook_id} --json
   ```
```

- [ ] **Step 4: Commit**

```bash
cd "C:\Users\leone\.claude\agents" && git -C "C:\Users\leone\Documents\Stock Analyst named Claude" add "C:\Users\leone\.claude\agents\stock-ticker-agent.md" && git -C "C:\Users\leone\Documents\Stock Analyst named Claude" commit -m "feat: update ticker agent — sanc.py, 10-Q, new infographics"
```

Note: The agents directory is outside the main repo. If it's not tracked by this repo's git, commit separately or skip.

---

### Task 6: Update stock-download-agent for new artifacts

**Files:**
- Modify: `C:\Users\leone\.claude\agents\stock-download-agent.md`

- [ ] **Step 1: Add new artifact inputs and downloads**

Add to the Input section:
```markdown
- `biz_structure_artifact_id`: Artifact ID for the business structure infographic
- `sankey_artifact_id`: Artifact ID for the Sankey flow infographic
```

Add to Download Commands:
```bash
notebooklm download infographic "{output_dir}/business-structure.png" -a {biz_structure_artifact_id} --notebook {notebook_id}
notebooklm download infographic "{output_dir}/sankey-flow.png" -a {sankey_artifact_id} --notebook {notebook_id}
```

Update the status JSON template to include:
```json
"business_structure": {"status": "success|failed|timeout", "path": "business-structure.png"},
"sankey_flow": {"status": "success|failed|timeout", "path": "sankey-flow.png"}
```

- [ ] **Step 2: Commit**

```bash
git -C "C:\Users\leone\Documents\Stock Analyst named Claude" add "C:\Users\leone\.claude\agents\stock-download-agent.md" && git -C "C:\Users\leone\Documents\Stock Analyst named Claude" commit -m "feat: download agent handles new infographic artifacts"
```

---

### Task 7: Update stock-analyst orchestrator

**Files:**
- Modify: `C:\Users\leone\.claude\agents\stock-analyst.md`

- [ ] **Step 1: Update sec-lookup.py reference to sanc.py**

Change the pre-flight check:
```bash
python "C:\Users\leone\Documents\Stock Analyst named Claude\sanc.py" --help 2>&1 || echo "MISSING"
```

- [ ] **Step 2: Commit**

```bash
git -C "C:\Users\leone\Documents\Stock Analyst named Claude" add "C:\Users\leone\.claude\agents\stock-analyst.md" && git -C "C:\Users\leone\Documents\Stock Analyst named Claude" commit -m "refactor: orchestrator references sanc.py"
```

---

### Task 8: Update permissions for hands-free flow

**Files:**
- Modify: `.claude/settings.local.json`

- [ ] **Step 1: Update permissions**

Replace the current permissions with broader allow rules so the full pipeline runs without prompts:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(python sanc.py:*)",
      "Bash(python \"C:\\Users\\leone\\Documents\\Stock Analyst named Claude\\sanc.py\":*)",
      "Bash(python:*)",
      "Bash(PYTHONIOENCODING=utf-8 notebooklm:*)",
      "Bash(notebooklm:*)",
      "Bash(export PYTHONIOENCODING:*)",
      "Bash(export:*)",
      "Bash(mkdir:*)",
      "Bash(ls:*)",
      "Bash(cd:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(pytest:*)",
      "Read",
      "Write",
      "Edit",
      "Glob",
      "Grep",
      "Agent"
    ],
    "additionalDirectories": [
      "C:\\Users\\leone\\.claude\\agents"
    ]
  },
  "env": {
    "PYTHONIOENCODING": "utf-8"
  }
}
```

- [ ] **Step 2: Verify no old sec-lookup.py references remain**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && grep -r "sec-lookup" --include="*.py" --include="*.md" --include="*.json" . 2>/dev/null
```
Expected: No matches (or only in git history)

- [ ] **Step 3: Commit**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git add .claude/settings.local.json && git commit -m "feat: broaden permissions for hands-free agentic flow"
```

---

### Task 9: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update all command references**

Replace `sec-lookup.py` with `sanc.py` in commands section. Add the `quarterly` command:

```markdown
## Commands

\```bash
# Fetch 5 years of 10-K filings for a ticker
python sanc.py filings <TICKER>

# Fetch last 4 quarterly 10-Q filings for a ticker
python sanc.py quarterly <TICKER>

# Gather supplementary research (analyst ratings, news, earnings)
python sanc.py research <TICKER>

# Run tests (integration tests hitting live APIs)
pytest test_sanc.py -v
\```
```

Update architecture section to reference `sanc.py` and mention the `quarterly` command.

- [ ] **Step 2: Commit**

```bash
cd "C:\Users\leone\Documents\Stock Analyst named Claude" && git add CLAUDE.md && git commit -m "docs: update CLAUDE.md for sanc rename and quarterly command"
```
