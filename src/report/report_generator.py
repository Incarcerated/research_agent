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

    return f"""
You are an expert researcher. Using the information below, write a comprehensive research report.

Query: {query}

Sources (title, URL and summary):
{sources}

Report format (use exactly these markdown headings):

# Executive Summary

# Key Findings

# Common Themes

# Recommendations

# Conclusion

# References

Provide the report in plain markdown text without any extra commentary.
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

