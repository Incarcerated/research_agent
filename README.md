# Research Agent

An **AI Research Agent** that can take a natural‑language query, search the web,
scrape the top results, summarise each article and finally generate a structured
research report using a local Ollama LLM.

## Project Structure

```
src/
├── main.py                 # Entry point – prompts for a query and runs the workflow
├── config.py               # (placeholder for future configuration)
├── llm/
│   └── ollama_client.py    # Thin wrapper around the Ollama `/generate` API
├── search/
│   └── search.py           # Web search – Tavily primary, DuckDuckGo fallback
├── scraper/
│   └── scraper.py          # Fetch HTML and extract clean text (Trafilatura → Readability → BS4)
├── report/
│   ├── summarizer.py       # Chunk‑wise summarisation of a single article
│   └── report_generator.py # Combine per‑source summaries into a final markdown report
└── research/
    └── researcher.py       # Orchestrates search → scrape → summarise for many sources
```

## How It Works

1. **User Input** – `main.py` asks for a research query.
2. **Search** – `researcher.research` calls `search.search_web` to obtain up to 10
   relevant URLs.
3. **Scrape** – Each URL is fetched with `scraper.scrape_url`. Errors are logged
   and the pipeline continues.
4. **Summarise** – The article text is split into 4 k‑character chunks and each
   chunk is summarised via the Ollama LLM (`summarizer.summarize`).
5. **Collect** – For every successful source we keep `title`, `url` and the
   generated `summary`.
6. **Report Generation** – `report.report_generator.generate_report` builds a
   prompt that includes all source summaries and asks the LLM to produce a final
   markdown report with the sections:

   * Executive Summary
   * Key Findings
   * Common Themes
   * Recommendations
   * Conclusion
   * References

7. **Output** – The final report is printed to stdout.

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd research_agent

# Create a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

You also need a running Ollama server with the `llama3` model available:

```bash
ollama serve &
ollama pull llama3
```

If you want to use Tavily for the primary search, add a `TAVILY_API_KEY` to a
`.env` file in the project root:

```
TAVILY_API_KEY=your_key_here
```

## Usage

```bash
python src/main.py
```

Enter a research question when prompted, e.g.:

```
Research React Native performance optimization
```

The script will display progress logs and finally output a markdown report.

## Extending the Project

* **Configuration** – Populate `src/config.py` with constants such as default
  `MAX_RESULTS` or custom LLM parameters.
* **Logging** – Replace the simple `print` statements with the `logging` module
  for more control over log levels and output destinations.
* **Tests** – Add unit tests for each module under a `tests/` directory.

## License

This project is provided under the MIT License.

