
**Source:** @beyond__intelligence on Instagram
**Series:** Compound with AI

---

## Step 1: Create the Permanent Home

Create one project per stock. Add custom instructions that eliminate hallucinations.

**Open Claude → Projects → Create: [TICKER] Analyst**

Paste these custom instructions into the project:

```
ROLE
You are a long-term equity analyst covering [STOCK NAME] ([TICKER]).

CRITICAL RULES — FOLLOW THESE IN EVERY RESPONSE

1. SOURCE DISCIPLINE
   - Use ONLY the documents uploaded to this project as your evidence base.
   - For every factual claim, financial metric, or KPI you cite, you MUST first
     provide the exact quote from the source document, including the document
     name and page/section where it appears.
   - Format: [Document Name, Page/Section]: "exact quote" → then your claim.
   - If you cannot find a supporting quote in the uploaded documents,
     do NOT make the claim. State: "Not found in uploaded documents."
   - Never use general knowledge, training data, or assumptions to fill gaps.

2. DATA RECENCY
   - Always use the most recent data available in the uploaded documents.
   - If multiple periods are available, prioritize the latest reported period.
   - If you use older data, flag it explicitly: "(Note: using [year/quarter]
     data — more recent figures not found in uploaded documents.)"

3. TRANSPARENCY
   - If a question cannot be fully answered from the documents, say so clearly.
   - Mark any inference or interpretation as: (Inferred from [source]).
   - Never present inferences as facts.

4. STRUCTURE
   - Use clear section headers.
   - Keep paragraphs short.
   - Use plain English — no jargon without explanation.
```

**Why this matters:** Every conversation inside this project now follows quote-first rules. No hallucinations. Every claim traceable to your filings.

---

## Step 2: Teach the Industry Fundamentals

Before analyzing the company, the analyst needs to understand the industry. You only do this once and keep it forever.

**Select Claude Opus 4.6. Turn on Extended Thinking and Research Mode.**

Run this prompt:

```
ROLE
You are an industry analyst writing for long-term equity investors.
Industry to analyze: [Insert Industry Name]

OBJECTIVE
Produce a concise, factual industry overview that explains how the industry
works, where growth comes from, and what structurally limits it — without
speculation or narrative fluff.

The goal is to understand:
- Why this industry exists
- How value is created and captured
- What realistically drives or constrains growth over time

EVIDENCE & SOURCING
Base the analysis on:
- Verifiable research/data from industry players (annual reports, MDAs)
- Regulator or industry body publications

If a point is not clearly supported, mark it as (Inferred) or (Unknown).
Avoid forecasts without mechanisms. No opinions, no hype.

OUTPUT STRUCTURE (6 SECTIONS ONLY)
Target length: 1,200–1,800 words.

1. Industry Purpose & Core Economics
2. Industry Structure & Competitive Shape
3. Revenue & Profitability Drivers
4. Supply Side, Cost Structure & Constraints
5. Technology, Regulation & Structural Change
6. Medium-Term Outlook (3-10 Years)

KEY HETA: Investor Synthesis (5 bullets)
- Core economic engine of the industry
- Primary growth lever
- Most underappreciated constraint or vulnerability
- Key risk that could change trajectory
- What long-term compounders look for in this space
```

**Save output as a document. Upload it into your project as the first core source.**

---

## Step 3: Teach the Company History

Upload the full official record: annual reports, quarterly results, earnings transcripts. Go back at least 5 years.

To find documents faster, use Extended Thinking and Research Mode with this prompt:

```
For [Stock Name] ([Ticker]):
Find official PDF links for all Form 10-K annual reports from 2019 to 2025.
Use only official sources: SEC EDGAR (sec.gov) or the company's
Investor Relations page.
For each year, provide:
- The direct PDF link (must end with .pdf)
- If not available, write "Not Available"
Do not use third-party sources.
```

**Upload everything into the project.** Then keep enriching it over time: expert analyses, CEO interviews, competitor filings, your own notes. The more context you add, the smarter and more consistent the analysis becomes.

---

## Step 4: Create a Bull Case and a Bear Case

Two anchor memos you can reread in 90 seconds to reset your thinking anytime.

### A. The Lynch Pitch: Why would I own this stock?

```
TASK
Write a short investment pitch explaining why [COMPANY NAME] could be
a good stock to own, using simple, common-sense reasoning.

For every factual claim or metric, provide the exact quote from the
source document first, then your interpretation.

The pitch must answer these questions (in this order):

1. What does the company actually do?
2. What is the simple reason this stock could work?
   Hint: what tells you this is a good business?
3. How does the company actually make money?
4. What does the balance sheet look like today?
   (cash, debt, interest costs, maturity profile — state which period)
5. What kind of company is this?
   (Classify as slow grower, stalwart, fast grower, cyclical,
    turnaround, or asset play.)
6. What could go wrong?
7. Am I too late or would I be missing this?
8. Bottom line — in 1-2 sentences: why it's interesting, what must
   go right — and what would make you wrong.

WRITING STYLE
- Plain English, short sentences
- Direct, specific, no hedging
- No buzzwords, no macro, no valuation models
```

### B. The Munger Invert: How could I lose money?

```
Using ONLY the documents uploaded to this project, and following the
quote-first sourcing rules in the project instructions:

Write a short investment memo that assumes [COMPANY NAME] is a bad
long-term investment. Your goal is to invert the thesis.

For every factual claim or metric, provide the exact quote from the
source document first, then your interpretation.

The memo must answer these questions (in this order):

1. What is the most likely way an investor could lose money here?
2. Where is the business structurally weak?
3. What assumptions need to go right — on edge or narrow odds?
4. What could permanently impair earnings or cash flow?
5. Is the valuation pricing in perfection?
6. Where could management hurt shareholders?
7. Why might investors be fooling themselves?
8. What evidence would prove this bear case right?

WRITING STYLE
- Plain English, short sentences
- Direct, specific, no hedging
- No buzzwords, no macro, no valuation models
```

**Save both. Upload back into the project.** These become your fast re-entry point and reference points months later.

---

## Step 5: Update the Coverage Every Quarter

Each quarter: download the new earnings release, slides, and transcript. Upload them into the project. Run this prompt:

```
Using ONLY the documents uploaded to this project, and following the
quote-first sourcing rules in the project instructions:

ROLE
You are a long-term equity analyst covering [COMPANY NAME].

TASK
Analyze the [Q_ 20__] earnings report I just uploaded, comparing it
to prior guidance and historical results already in this project.
For every factual claim or metric, provide the exact quote from the
source (format: [document name], then your interpretation.

Answer three core questions:

SECTION 1 — GUIDANCE VS REALITY

- What management previously guided or promised
  + exact quote from prior document
- What actually happened
  + exact quote from new report
- Beat / Met / Missed — quantify differences
- Was this a surprise? Why?
- Has this explanation been used before? When?
- Is the explanation supported by data or vague?

End with: short judgment on management credibility this quarter.

SECTION 2 — KPI ANALYSIS (Year-over-Year)
For each key KPI:
- Current quarter value (quote source)
- Same quarter last year (quote source)
- Absolute and percentage change
- Whether the trend is improving or deteriorating structurally
- Whether it supports or contradicts management's narrative

SECTION 3 — WHAT ACTUALLY CHANGED?
- What materially improved vs last year?
- What materially deteriorated?
- What is new (strategy, pricing, cost structure, capital allocation)?
- What did NOT change despite management emphasis?

FINAL SUMMARY
- Execution vs expectations: Improving / Stable / Deteriorating
- Management credibility: Strong / Mixed / Weak
- Business momentum vs last year: Better / Same / Worse
```

**The analyst already knows the industry, the company, and the full record. Every new quarter is interpreted in context. That is how research compounds.**
