"""Report generator for the research agent.

Accepts the original query and a list of per‑source summaries, then asks the
LLM to produce a final markdown report with the required sections.
"""

from __future__ import annotations

from typing import List, Dict

from llm.ollama_client import generate


def _build_prompt(query: str, research_data: List[Dict[str, str]]) -> str:
    """Construct the LLM prompt.

    The prompt includes the query and a compact representation of each source
    (title, URL and its summary). The LLM is instructed to output the report in
    markdown with exact headings.
    """
    sources = "\n\n".join(
        f"Title: {item['title']}\nURL: {item['url']}\nSummary:\n{item['summary']}"
        for item in research_data
    )

    # The prompt now asks the model to elaborate, cite sources inline, and ensure depth.
    return f"""
You are an expert researcher tasked with producing a **detailed, accurate, and extensive** research report.

Use the information provided below. For each section, expand on the findings, provide analysis, and where appropriate include direct quotations or data points from the sources. Cite sources inline using the format `[Title](URL)`.

**Query:** {query}

**Sources (title, URL and summary):**
{sources}

**Report format (use exactly these markdown headings and maintain this order):**

# Executive Summary
Summarize the overall answer to the query, highlighting the most critical insights.

# Key Findings
List the top 5‑7 findings, each with a brief explanation and inline citation.

# Common Themes
Identify patterns or recurring ideas across sources, providing synthesis.

# Recommendations
Offer actionable recommendations based on the findings.

# Conclusion
Conclude with a concise wrap‑up that ties back to the original query.

# References
List full citations for each source used, formatted as `- Title (URL)`.

Provide the report **as plain markdown** without any additional commentary or pre‑amble.
"""


def generate_report(query: str, research_data: List[Dict[str, str]]) -> str:
    """Generate the final report using the LLM.

    Returns a markdown string. If ``research_data`` is empty a fallback message
    is returned.
    """
    if not research_data:
        return "No research data available to generate a report."

    prompt = _build_prompt(query, research_data)
    try:
        return generate(prompt)
    except Exception as exc:  # pragma: no cover – defensive
        return f"Report generation failed: {exc}"
