import trafilatura
import requests
from readability import Document
from bs4 import BeautifulSoup


# -----------------------------
# Step 1: Fetch HTML safely
# -----------------------------
def fetch_html(url: str):
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )

        if response.status_code == 200:
            return response.text

        return None

    except Exception:
        return None


# -----------------------------
# Step 2: Trafilatura extraction (BEST)
# -----------------------------
def extract_trafilatura(html: str):
    return trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        favor_recall=True
    )


# -----------------------------
# Step 3: Readability fallback
# -----------------------------
def extract_readability(html: str):
    doc = Document(html)
    content_html = doc.summary()
    return BeautifulSoup(content_html, "html.parser").get_text()


# -----------------------------
# Step 4: BeautifulSoup fallback
# -----------------------------
def extract_bs4(html: str):
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")

    text = "\n".join(
        p.get_text(strip=True)
        for p in paragraphs
        if p.get_text(strip=True)
    )

    return text


# -----------------------------
# Step 5: Hybrid extractor
# -----------------------------
def extract_text(html: str):
    if not html:
        return ""

    # 1. Trafilatura (best)
    text = extract_trafilatura(html)
    if text and len(text) > 800:
        return text

    # 2. Readability fallback
    try:
        text = extract_readability(html)
        if text and len(text) > 800:
            return text
    except Exception:
        pass

    # 3. BS4 fallback
    return extract_bs4(html)


# -----------------------------
# Step 6: Main scraper
# -----------------------------
def scrape_url(url: str):
    html = fetch_html(url)
    if not html:
        return ""

    text = extract_text(html)

    # FINAL GUARD (important)
    if not text or len(text.strip()) < 300:
        return ""

    return text