"""Entry point for the AI Research Agent MVP.

The script prompts the user for a research query, runs the full pipeline and
prints the final markdown report.
"""

from __future__ import annotations

import sys

from research.researcher import research
from report.report_generator import generate_report


def _prompt_query() -> str:
    """Read a research query from stdin.

    ``input`` works both interactively and when the program is piped.
    """
    try:
        return input("Enter research query: ").strip()
    except EOFError:
        sys.exit("No query provided – exiting.")


def main() -> None:
    query = _prompt_query()
    if not query:
        sys.exit("Empty query – exiting.")

    # Phase 1 – gather per‑source findings
    findings = research(query)

    # Phase 2 – generate the final report
    report = generate_report(query, findings)

    # Persist the report using the storage layer
    from storage.storage import save_report

    try:
        saved_path = save_report(query, report, findings)
        print("Research completed.")
        print("Report saved:")
        print(saved_path)
    except Exception as e:
        print(f"Failed to write report {e}")


if __name__ == "__main__":
    main()
