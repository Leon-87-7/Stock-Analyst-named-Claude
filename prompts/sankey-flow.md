You are a data visualization designer. Using all relevant sources in this NotebookLM project, design a clear Sankey flow infographic that shows how [COMPANY NAME]'s revenue flows from its main sources through major cost categories to final net income.

First, extract a table of flows with three columns: source, target, and value (numerical, in millions of currency units). Include nodes like:

- Revenue sources (e.g., subscriptions, product sales, ads, services)
- Intermediate buckets (e.g., COGS, R&D, marketing, G&A, taxes)
- Final nodes (e.g., net profit, retained earnings, dividends).

Then, propose a Sankey diagram spec using that table, describing:

- Node list and groupings
- Link list (source → target → value)
- Recommended colors (e.g., green for revenue, orange for costs, blue for profit)
- Suggested labels and short annotations for key flows.

Return your answer in this structure so I can feed it directly into a diagram tool:

1. Brief textual description of the story the Sankey should tell (3–5 sentences).
2. Markdown table of the flows with columns: source, target, value.
3. A JSON-like block with nodes, links, and colors suitable for a Sankey chart library.

Make sure the flows balance (total inflows ≈ total outflows for each node), flag any assumptions you had to make, and keep labels concise enough to fit in a chart.
