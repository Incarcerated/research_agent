"""Researcher orchestration module.

Provides a high‑level ``research`` function that accepts a query, searches the
web, scrapes each result, summarizes the article and returns a structured list
of findings.
"""

from __future__ import annotations

import sys
import traceback
from typing import List, Dict

from search.search import search_web
from scraper.scraper import scrape_url
from report.summarizer import summarize
import json
from pathlib import Path


def _log(message: str) -> None:
    """Simple console logger.

    Keeping logging minimal makes the MVP easy to run in any environment.
    """
    print(message)


def _safe_scrape(url: str) -> str:
    """Scrape *url* safely, returning an empty string on failure."""
    try:
        return scrape_url(url) or ""
    except Exception as exc:  # pragma: no cover – defensive
        _log(f"[ERROR] Failed to scrape {url}: {exc}")
        traceback.print_exc(file=sys.stderr)
        return ""


def _safe_summarize(text: str) -> str:
    """Summarize *text* safely, returning an empty string on failure."""
    try:
        return summarize(text) or ""
    except Exception as exc:  # pragma: no cover – defensive
        _log(f"[ERROR] Summarization failed: {exc}")
        traceback.print_exc(file=sys.stderr)
        return ""


def research(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """Run the full research pipeline.

    Returns a list of dictionaries with ``title``, ``url`` and ``summary``.
    """
    _log(f"🔎 Starting research for query: {query}")

    # Search the web (fallback handling is inside ``search_web``)
    search_response = search_web(query, max_results=max_results)
    results = (
        search_response.get("results", [])
        if isinstance(search_response, dict)
        else []
    )

    findings: List[Dict[str, str]] = []

    for idx, item in enumerate(results, start=1):
        title = item.get("title") or item.get("href") or "Untitled"
        url = item.get("href") or item.get("url") or ""
        _log(f"\nProcessing source {idx}/{len(results)}: {title}\nURL: {url}")

        if not url:
            _log("[WARN] No URL – skipping.")
            continue

        _log("📄 Scraping URL…")
        raw = _safe_scrape(url)
        if not raw:
            _log("[WARN] Empty content – skipping.")
            continue

        _log("🧠 Summarizing article…")
        summary = _safe_summarize(raw)
        if not summary:
            _log("[WARN] No summary – skipping.")
            continue

        findings.append({
            "title": title,
            "url": url,
            "summary": summary
        })

        _log("✅ Done")

    _log(f"\n🔚 Research completed – {len(findings)} sources collected.")

    # -----------------------------
    # 💾 SAVE TO PROJECT ROOT
    # -----------------------------
    output_path = Path(__file__).resolve().parents[2] / "research_output.json"

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(findings, f, ensure_ascii=False, indent=2)

        _log(f"💾 Results saved to: {output_path}")

    except Exception as e:
        _log(f"[ERROR] Failed to save file: {e}")

    return findings