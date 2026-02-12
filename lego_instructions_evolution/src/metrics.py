"""PDF page counting and part rarity metrics."""

import logging
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from pypdf import PdfReader

logger = logging.getLogger(__name__)


def download_pdf(
    identifier: str, filename: str, out_dir: Path, max_retries: int = 4
) -> Path:
    """Download a single PDF from Internet Archive."""
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_filename = filename.replace("/", "_")
    out_path = out_dir / f"{identifier}__{safe_filename}"
    if out_path.exists():
        return out_path

    url = f"https://archive.org/download/{identifier}/{filename}"
    for attempt in range(max_retries):
        try:
            with requests.get(url, stream=True, timeout=120) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=256 * 1024):
                        if chunk:
                            f.write(chunk)
            return out_path
        except (requests.RequestException, requests.HTTPError) as e:
            wait = 2 ** (attempt + 1)
            logger.warning(f"PDF download attempt {attempt+1} for {identifier}/{filename} failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)
            if out_path.exists():
                out_path.unlink()

    raise RuntimeError(f"Failed to download {identifier}/{filename} after {max_retries} retries")


def pdf_page_count(path: Path) -> int:
    """Count pages in a PDF file."""
    try:
        reader = PdfReader(str(path))
        return len(reader.pages)
    except Exception as e:
        logger.warning(f"Failed to read PDF {path}: {e}")
        return 0


def compute_manual_metrics(
    identifier: str, pdf_files: list[str], manuals_dir: Path
) -> dict:
    """Download PDFs for a set and compute page counts.

    Returns dict with pages_total, booklets, per_booklet_pages.
    """
    per_booklet = []
    for pdf_name in pdf_files:
        try:
            path = download_pdf(identifier, pdf_name, manuals_dir)
            pages = pdf_page_count(path)
            per_booklet.append({"filename": pdf_name, "pages": pages})
        except Exception as e:
            logger.warning(f"Skipping {identifier}/{pdf_name}: {e}")

    pages_total = sum(b["pages"] for b in per_booklet)
    booklets = len(per_booklet)

    return {
        "identifier": identifier,
        "pages_total": pages_total,
        "booklets": booklets,
        "per_booklet_pages": per_booklet,
    }


def estimate_build_pages(pages_total: int, front_matter: int = 2, back_matter: int = 1) -> int:
    """Estimate the number of actual build instruction pages."""
    build_pages = pages_total - front_matter - back_matter
    return max(build_pages, 1)


def compute_derived_metrics(row: pd.Series) -> dict:
    """Compute derived complexity metrics for a single set row.

    Expects row to have: pages_total, total_pieces, unique_parts, booklets.
    """
    pages_total = row.get("pages_total", 0)
    total_pieces = row.get("total_pieces", 0)
    unique_parts = row.get("unique_parts", 0)

    metrics = {}

    if total_pieces > 0:
        metrics["pages_per_100_pieces"] = 100.0 * pages_total / total_pieces
        metrics["unique_ratio"] = unique_parts / total_pieces
    else:
        metrics["pages_per_100_pieces"] = np.nan
        metrics["unique_ratio"] = np.nan

    build_pages = estimate_build_pages(pages_total)
    if build_pages > 0 and total_pieces > 0:
        metrics["pieces_per_page_est"] = total_pieces / build_pages
    else:
        metrics["pieces_per_page_est"] = np.nan

    return metrics


def compute_global_part_freq(
    inv_parts_df: pd.DataFrame, inv_df: pd.DataFrame
) -> pd.Series:
    """Compute how many distinct sets each part appears in.

    Returns a Series indexed by part_num with counts.
    """
    joined = inv_parts_df.merge(
        inv_df[["id", "set_num"]], left_on="inventory_id", right_on="id", how="left"
    )
    part_set_counts = joined.groupby("part_num")["set_num"].nunique()
    return part_set_counts


def set_rarity_scores(
    set_parts: pd.DataFrame, part_set_counts: pd.Series
) -> dict:
    """Compute rarity metrics for a set's parts.

    Args:
        set_parts: DataFrame with columns part_num, quantity
        part_set_counts: Series mapping part_num -> number of sets it appears in

    Returns dict with rarity_wmean and rare_part_share.
    """
    if set_parts.empty:
        return {"rarity_wmean": np.nan, "rare_part_share": np.nan}

    freqs = set_parts["part_num"].map(part_set_counts).fillna(1).astype(float)
    rarity = -np.log(freqs)
    qty = set_parts["quantity"].astype(float)

    total_qty = qty.sum()
    if total_qty > 0:
        w_mean = float((rarity * qty).sum() / total_qty)
    else:
        w_mean = float(rarity.mean())

    # Bottom 10% by frequency = rare
    rare_threshold = part_set_counts.quantile(0.10)
    mapped_freqs = set_parts["part_num"].map(part_set_counts)
    rare_share = float((mapped_freqs <= rare_threshold).mean())

    return {"rarity_wmean": w_mean, "rare_part_share": rare_share}
