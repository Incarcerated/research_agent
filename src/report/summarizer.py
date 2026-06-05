from llm.ollama_client import generate


# -----------------------------
# Step 1: Chunk text safely
# -----------------------------
def chunk_text(text: str, chunk_size: int = 4000):
    if not text:
        return []

    text = text.strip()
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


# -----------------------------
# Step 2: Summarize a single chunk
# -----------------------------
def summarize_chunk(chunk: str):
    prompt = f"""
You are a professional summarizer.

Summarize this section of an article.

Rules:
- Only key information
- Bullet points only
- No fluff

Text:
{chunk}
"""

    try:
        return generate(prompt)
    except Exception:
        return ""


# -----------------------------
# Step 3: Combine summaries
# -----------------------------
def combine_summaries(summaries: list):
    combined_text = "\n".join(summaries)

    prompt = f"""
You are an expert editor.

Combine these partial summaries into one clean final summary.

Return format:

MAIN POINTS:
- ...

IMPORTANT FACTS:
- ...

INSIGHTS:
- ...

Rules:
- Remove duplicates
- Keep it concise
- Do not add new info

Summaries:
{combined_text}
"""

    try:
        return generate(prompt)
    except Exception:
        return combined_text


# -----------------------------
# Step 4: Main function
# -----------------------------
def summarize(content: str):
    if not content:
        return "No content to summarize."

    chunks = chunk_text(content, chunk_size=4000)

    if not chunks:
        return "No valid chunks generated."

    # Step A: summarize each chunk
    partial_summaries = []

    for chunk in chunks:
        summary = summarize_chunk(chunk)
        if summary:
            partial_summaries.append(summary)

    if not partial_summaries:
        return "Failed to generate chunk summaries."

    # Step B: combine summaries
    final_summary = combine_summaries(partial_summaries)

    return final_summary