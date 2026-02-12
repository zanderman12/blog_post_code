"""Rebrickable CSV data loading and set matching."""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

REBRICKABLE_BASE_URL = "https://cdn.rebrickable.com/media/downloads/"
NEEDED_FILES = [
    "sets.csv.gz",
    "inventories.csv.gz",
    "inventory_parts.csv.gz",
    "parts.csv.gz",
    "themes.csv.gz",
]


def download_rebrickable_csvs(out_dir: Path, max_retries: int = 4) -> None:
    """Download all needed Rebrickable CSV files to out_dir."""
    import time
    import requests

    out_dir.mkdir(parents=True, exist_ok=True)

    for fname in NEEDED_FILES:
        out_path = out_dir / fname
        if out_path.exists():
            logger.info(f"Already have {fname}, skipping download")
            continue

        url = REBRICKABLE_BASE_URL + fname
        logger.info(f"Downloading {url}...")

        for attempt in range(max_retries):
            try:
                r = requests.get(url, stream=True, timeout=120)
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=256 * 1024):
                        if chunk:
                            f.write(chunk)
                logger.info(f"Downloaded {fname} ({out_path.stat().st_size / 1e6:.1f} MB)")
                break
            except (requests.RequestException, requests.HTTPError) as e:
                wait = 2 ** (attempt + 1)
                logger.warning(f"Download attempt {attempt+1} for {fname} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
                if out_path.exists():
                    out_path.unlink()
        else:
            raise RuntimeError(f"Failed to download {fname} after {max_retries} retries")


def load_rebrickable_csvs(root: Path) -> dict[str, pd.DataFrame]:
    """Load downloaded Rebrickable CSV files into DataFrames."""
    dfs = {}
    dfs["sets"] = pd.read_csv(root / "sets.csv.gz")
    dfs["inventories"] = pd.read_csv(root / "inventories.csv.gz")
    dfs["inventory_parts"] = pd.read_csv(root / "inventory_parts.csv.gz")
    dfs["parts"] = pd.read_csv(root / "parts.csv.gz")
    dfs["themes"] = pd.read_csv(root / "themes.csv.gz")

    for name, df in dfs.items():
        logger.info(f"Loaded {name}: {len(df)} rows")

    return dfs


def match_set(sets_df: pd.DataFrame, set_number: str) -> pd.Series | None:
    """Match an IA-derived set number to a Rebrickable set_num.

    Tries '{set_number}-1' first (most common), then falls back to
    any variant starting with '{set_number}-'.
    """
    target = f"{set_number}-1"
    exact = sets_df[sets_df["set_num"] == target]
    if len(exact) >= 1:
        return exact.iloc[0]
    # Fallback: first variant
    cand = sets_df[sets_df["set_num"].str.startswith(f"{set_number}-", na=False)]
    if len(cand) >= 1:
        return cand.sort_values("set_num").iloc[0]
    return None


def compute_set_inventory_metrics(
    inv_df: pd.DataFrame, inv_parts_df: pd.DataFrame, set_num: str
) -> tuple[int, int, pd.DataFrame]:
    """Compute total pieces and unique parts for a given set_num.

    Returns (total_pieces, unique_parts, parts_detail_df).
    """
    inv_ids = inv_df.loc[inv_df["set_num"] == set_num, "id"]
    if inv_ids.empty:
        return 0, 0, pd.DataFrame(columns=["part_num", "quantity"])

    parts_rows = inv_parts_df[inv_parts_df["inventory_id"].isin(inv_ids)]

    total_pieces = int(parts_rows["quantity"].sum())
    unique_parts = int(parts_rows["part_num"].nunique())

    return total_pieces, unique_parts, parts_rows[["part_num", "quantity"]].copy()


def build_set_facts(
    ia_index: pd.DataFrame, sets_df: pd.DataFrame,
    inv_df: pd.DataFrame, inv_parts_df: pd.DataFrame,
) -> pd.DataFrame:
    """Match IA sets to Rebrickable and compute per-set facts.

    Returns a DataFrame with set_number, set_num, year, name,
    total_pieces, unique_parts.
    """
    rows = []
    unique_set_numbers = ia_index["set_number"].dropna().unique()
    logger.info(f"Matching {len(unique_set_numbers)} unique set numbers to Rebrickable...")

    for sn in unique_set_numbers:
        matched = match_set(sets_df, sn)
        if matched is None:
            continue

        set_num = matched["set_num"]
        year = int(matched["year"])
        name = matched.get("name", "")
        num_parts_rb = int(matched.get("num_parts", 0))

        total_pieces, unique_parts, _ = compute_set_inventory_metrics(
            inv_df, inv_parts_df, set_num
        )

        # Use Rebrickable's num_parts as fallback if inventory data is missing
        if total_pieces == 0 and num_parts_rb > 0:
            total_pieces = num_parts_rb

        rows.append({
            "set_number": sn,
            "set_num": set_num,
            "year": year,
            "name": name,
            "total_pieces": total_pieces,
            "unique_parts": unique_parts,
            "num_parts_rb": num_parts_rb,
        })

    df = pd.DataFrame(rows)
    logger.info(f"Matched {len(df)} sets to Rebrickable")
    return df
