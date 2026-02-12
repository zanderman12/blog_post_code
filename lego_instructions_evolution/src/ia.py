"""Internet Archive scraping and metadata retrieval for LEGO instruction PDFs."""

import re
import time
import logging
import requests

logger = logging.getLogger(__name__)

IA_SCRAPE = "https://archive.org/services/search/v1/scrape"
IA_META = "https://archive.org/metadata/{}"
SETNO_RE = re.compile(r"(\d{3,7})")


def ia_scrape_collection(
    query: str = "collection:lego-set-instructions",
    fields: list[str] | None = None,
    count: int = 1000,
    max_retries: int = 4,
) -> list[dict]:
    """Scrape all items from an IA collection using the scraping API.

    Paginates through results using cursors and returns all items.
    """
    if fields is None:
        fields = ["identifier", "title", "date", "publicdate"]

    params = {
        "q": query,
        "fields": ",".join(fields),
        "count": count,
        "sorts": "identifier",
    }
    cursor = None
    session = requests.Session()
    all_items = []

    while True:
        if cursor:
            params["cursor"] = cursor

        resp = None
        for attempt in range(max_retries):
            try:
                resp = session.get(IA_SCRAPE, params=params, timeout=60)
                resp.raise_for_status()
                break
            except (requests.RequestException, requests.HTTPError) as e:
                wait = 2 ** (attempt + 1)
                logger.warning(f"IA scrape attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
        if resp is None:
            raise RuntimeError("Failed to scrape IA after retries")

        obj = resp.json()
        items = obj.get("items", [])
        all_items.extend(items)
        logger.info(f"Fetched {len(items)} items (total: {len(all_items)})")

        cursor = obj.get("cursor")
        if not cursor:
            break

    return all_items


def parse_set_number(identifier: str, title: str = "") -> str | None:
    """Extract a LEGO set number from an IA identifier or title.

    Looks for 3-7 digit numbers, preferring the identifier.
    """
    m = SETNO_RE.search(identifier)
    if m:
        return m.group(1)
    m = SETNO_RE.search(title or "")
    return m.group(1) if m else None


def ia_fetch_item_metadata(identifier: str, max_retries: int = 4) -> dict:
    """Fetch full metadata JSON for a single IA item."""
    for attempt in range(max_retries):
        try:
            r = requests.get(IA_META.format(identifier), timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, requests.HTTPError) as e:
            wait = 2 ** (attempt + 1)
            logger.warning(f"Metadata fetch attempt {attempt+1} for {identifier} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError(f"Failed to fetch metadata for {identifier} after retries")


def list_original_pdfs(item_meta: dict) -> list[str]:
    """From item metadata, return filenames of original PDF files."""
    pdfs = []
    for f in item_meta.get("files", []):
        name = f.get("name", "")
        if f.get("source") == "original" and name.lower().endswith(".pdf"):
            pdfs.append(name)
    return pdfs


def build_ia_index(items: list[dict]) -> list[dict]:
    """From raw scraped items, build an index with parsed set numbers."""
    index = []
    for item in items:
        identifier = item.get("identifier", "")
        title = item.get("title", "")
        set_number = parse_set_number(identifier, title)
        index.append({
            "identifier": identifier,
            "title": title,
            "set_number": set_number,
            "date": item.get("date", ""),
            "publicdate": item.get("publicdate", ""),
        })
    return index
