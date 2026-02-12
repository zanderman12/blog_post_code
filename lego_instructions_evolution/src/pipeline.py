"""Main pipeline orchestrator for the LEGO instruction complexity analysis."""

import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from . import ia, rebrickable, metrics, analyze

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MANUALS_DIR = DATA_DIR / "manuals"
RB_DIR = DATA_DIR / "rebrickable_raw"
PLOTS_DIR = BASE_DIR / "plots"


def setup_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )


def stage_a_scrape_ia(force: bool = False) -> pd.DataFrame:
    """Stage A: Scrape IA collection index."""
    cache_path = DATA_DIR / "ia_index.parquet"
    if cache_path.exists() and not force:
        logger.info(f"Loading cached IA index from {cache_path}")
        return pd.read_parquet(cache_path)

    logger.info("Scraping Internet Archive collection...")
    raw_items = ia.ia_scrape_collection()
    index = ia.build_ia_index(raw_items)
    df = pd.DataFrame(index)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_path, index=False)
    logger.info(f"Saved {len(df)} items to {cache_path}")
    return df


def stage_b_fetch_item_metadata(
    ia_index: pd.DataFrame,
    sample_size: int | None = None,
    force: bool = False,
) -> pd.DataFrame:
    """Stage B: Fetch per-item metadata to identify PDFs.

    If sample_size is set, only process that many items (for piloting).
    """
    cache_path = DATA_DIR / "ia_items.parquet"
    if cache_path.exists() and not force:
        logger.info(f"Loading cached IA items from {cache_path}")
        return pd.read_parquet(cache_path)

    # Filter to items with valid set numbers
    valid = ia_index.dropna(subset=["set_number"]).copy()
    # Deduplicate by set_number - keep first identifier per set
    valid = valid.drop_duplicates(subset=["set_number"], keep="first")

    if sample_size and len(valid) > sample_size:
        valid = valid.sample(n=sample_size, random_state=42)

    logger.info(f"Fetching metadata for {len(valid)} items...")
    rows = []
    for i, (_, row) in enumerate(valid.iterrows()):
        ident = row["identifier"]
        if (i + 1) % 50 == 0:
            logger.info(f"  Progress: {i+1}/{len(valid)}")
        try:
            meta = ia.ia_fetch_item_metadata(ident)
            pdfs = ia.list_original_pdfs(meta)
            rows.append({
                "identifier": ident,
                "set_number": row["set_number"],
                "title": row["title"],
                "pdf_count": len(pdfs),
                "pdf_files": "|".join(pdfs),  # store as pipe-separated string
            })
        except Exception as e:
            logger.warning(f"Failed to fetch metadata for {ident}: {e}")

    df = pd.DataFrame(rows)
    df.to_parquet(cache_path, index=False)
    logger.info(f"Saved {len(df)} items with PDF info to {cache_path}")
    return df


def stage_c_compute_manual_metrics(
    ia_items: pd.DataFrame,
    force: bool = False,
) -> pd.DataFrame:
    """Stage C: Download PDFs and compute page counts."""
    cache_path = DATA_DIR / "manual_metrics.parquet"
    if cache_path.exists() and not force:
        logger.info(f"Loading cached manual metrics from {cache_path}")
        return pd.read_parquet(cache_path)

    MANUALS_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    items_with_pdfs = ia_items[ia_items["pdf_count"] > 0]

    logger.info(f"Processing PDFs for {len(items_with_pdfs)} items...")
    for i, (_, row) in enumerate(items_with_pdfs.iterrows()):
        if (i + 1) % 25 == 0:
            logger.info(f"  Progress: {i+1}/{len(items_with_pdfs)}")

        ident = row["identifier"]
        pdf_files = row["pdf_files"].split("|") if row["pdf_files"] else []

        try:
            result = metrics.compute_manual_metrics(ident, pdf_files, MANUALS_DIR)
            result["set_number"] = row["set_number"]
            rows.append(result)
        except Exception as e:
            logger.warning(f"Failed to process PDFs for {ident}: {e}")

    df = pd.DataFrame(rows)
    # Drop the per_booklet_pages list column before saving to parquet
    if "per_booklet_pages" in df.columns:
        df = df.drop(columns=["per_booklet_pages"])
    df.to_parquet(cache_path, index=False)
    logger.info(f"Saved manual metrics for {len(df)} items to {cache_path}")
    return df


def stage_d_rebrickable_enrichment(
    ia_index: pd.DataFrame,
    force: bool = False,
) -> pd.DataFrame:
    """Stage D: Download Rebrickable data and compute set facts."""
    cache_path = DATA_DIR / "set_facts.parquet"
    if cache_path.exists() and not force:
        logger.info(f"Loading cached set facts from {cache_path}")
        return pd.read_parquet(cache_path)

    # Download CSVs if needed
    rebrickable.download_rebrickable_csvs(RB_DIR)

    # Load data
    dfs = rebrickable.load_rebrickable_csvs(RB_DIR)

    # Build set facts
    set_facts = rebrickable.build_set_facts(
        ia_index, dfs["sets"], dfs["inventories"], dfs["inventory_parts"]
    )
    set_facts.to_parquet(cache_path, index=False)
    logger.info(f"Saved set facts for {len(set_facts)} sets to {cache_path}")
    return set_facts


def stage_f_rarity_metrics(
    ia_index: pd.DataFrame,
    force: bool = False,
) -> pd.DataFrame:
    """Stage F: Compute part rarity metrics for each set."""
    cache_path = DATA_DIR / "rarity_metrics.parquet"
    if cache_path.exists() and not force:
        logger.info(f"Loading cached rarity metrics from {cache_path}")
        return pd.read_parquet(cache_path)

    # Load Rebrickable data
    dfs = rebrickable.load_rebrickable_csvs(RB_DIR)
    inv_df = dfs["inventories"]
    inv_parts_df = dfs["inventory_parts"]
    sets_df = dfs["sets"]

    # Compute global part frequencies
    logger.info("Computing global part frequencies...")
    part_freq = metrics.compute_global_part_freq(inv_parts_df, inv_df)

    # For each set in our IA index, compute rarity
    unique_set_numbers = ia_index["set_number"].dropna().unique()
    rows = []

    logger.info(f"Computing rarity for {len(unique_set_numbers)} sets...")
    for i, sn in enumerate(unique_set_numbers):
        if (i + 1) % 200 == 0:
            logger.info(f"  Progress: {i+1}/{len(unique_set_numbers)}")

        matched = rebrickable.match_set(sets_df, sn)
        if matched is None:
            continue

        set_num = matched["set_num"]
        _, _, set_parts = rebrickable.compute_set_inventory_metrics(
            inv_df, inv_parts_df, set_num
        )

        if set_parts.empty:
            continue

        rarity = metrics.set_rarity_scores(set_parts, part_freq)
        rarity["set_number"] = sn
        rows.append(rarity)

    df = pd.DataFrame(rows)
    df.to_parquet(cache_path, index=False)
    logger.info(f"Saved rarity metrics for {len(df)} sets to {cache_path}")
    return df


def stage_g_merge_and_analyze(
    manual_metrics: pd.DataFrame,
    set_facts: pd.DataFrame,
    rarity_metrics: pd.DataFrame,
    force: bool = False,
) -> pd.DataFrame:
    """Stage G: Merge all data sources and compute final derived metrics."""
    cache_path = DATA_DIR / "merged.parquet"
    if cache_path.exists() and not force:
        logger.info(f"Loading cached merged data from {cache_path}")
        return pd.read_parquet(cache_path)

    # Merge manual metrics with set facts
    merged = manual_metrics.merge(set_facts, on="set_number", how="inner")
    logger.info(f"After merging manual + set facts: {len(merged)} rows")

    # Merge rarity metrics
    if not rarity_metrics.empty:
        merged = merged.merge(rarity_metrics, on="set_number", how="left")
        logger.info(f"After merging rarity: {len(merged)} rows")
    else:
        merged["rarity_wmean"] = np.nan
        merged["rare_part_share"] = np.nan

    # Filter out sets with no pages or pieces
    merged = merged[(merged["pages_total"] > 0) & (merged["total_pieces"] > 0)]
    logger.info(f"After filtering: {len(merged)} rows with valid data")

    # Add derived columns
    merged = analyze.add_derived_columns(merged)

    merged.to_parquet(cache_path, index=False)
    logger.info(f"Saved merged dataset to {cache_path}")
    return merged


def stage_h_validate(merged: pd.DataFrame) -> str:
    """Stage H: Run validation and sanity checks."""
    lines = []
    lines.append("\n=== VALIDATION REPORT ===\n")

    # Basic counts
    lines.append(f"Total rows: {len(merged)}")
    lines.append(f"Year range: {merged['year'].min()} - {merged['year'].max()}")

    # Missingness
    lines.append("\nMissingness:")
    for col in ["pages_total", "total_pieces", "unique_parts", "rarity_wmean"]:
        if col in merged.columns:
            pct = merged[col].isna().mean() * 100
            lines.append(f"  {col}: {pct:.1f}% missing")

    # Coverage by decade
    lines.append("\nSets per decade:")
    by_decade = merged.groupby("decade").size()
    for decade, count in by_decade.items():
        lines.append(f"  {int(decade)}s: {count} sets")

    # Outlier check
    lines.append("\nOutlier check (pages_per_100_pieces):")
    p99 = merged["pages_per_100_pieces"].quantile(0.99)
    p01 = merged["pages_per_100_pieces"].quantile(0.01)
    lines.append(f"  1st percentile: {p01:.2f}")
    lines.append(f"  99th percentile: {p99:.2f}")

    # Sensitivity check
    lines.append("\nSensitivity: Median pieces/page under different assumptions:")
    for subtract in [2, 3, 4, 5]:
        bp = (merged["pages_total"] - subtract).clip(lower=1)
        ppp = merged["total_pieces"] / bp
        lines.append(f"  Subtract {subtract}: median pieces/page = {ppp.median():.2f}")

    report = "\n".join(lines)
    return report


def run_full_pipeline(
    sample_size: int | None = None,
    force: bool = False,
    log_level: str = "INFO",
) -> pd.DataFrame:
    """Run the complete pipeline end-to-end using live API data.

    Args:
        sample_size: If set, only process this many IA items (for piloting).
        force: If True, re-run all stages even if cached data exists.
        log_level: Logging level.

    Returns:
        The final merged DataFrame.
    """
    setup_logging(log_level)

    logger.info("=== Stage A: Scrape IA collection ===")
    ia_index = stage_a_scrape_ia(force=force)
    logger.info(f"IA index: {len(ia_index)} items, {ia_index['set_number'].notna().sum()} with set numbers")

    logger.info("=== Stage B: Fetch item metadata ===")
    ia_items = stage_b_fetch_item_metadata(ia_index, sample_size=sample_size, force=force)

    logger.info("=== Stage C: Compute manual metrics ===")
    manual_metrics = stage_c_compute_manual_metrics(ia_items, force=force)

    logger.info("=== Stage D: Rebrickable enrichment ===")
    set_facts = stage_d_rebrickable_enrichment(ia_index, force=force)

    logger.info("=== Stage F: Rarity metrics ===")
    rarity_metrics = stage_f_rarity_metrics(ia_index, force=force)

    logger.info("=== Stage G: Merge and analyze ===")
    merged = stage_g_merge_and_analyze(manual_metrics, set_facts, rarity_metrics, force=force)

    # Generate plots
    logger.info("=== Generating plots ===")
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    analyze.generate_all_plots(merged, PLOTS_DIR)

    # Print summary
    summary = analyze.print_summary_stats(merged)
    logger.info(summary)

    # Validation
    validation = stage_h_validate(merged)
    logger.info(validation)

    return merged


def run_synthetic_pipeline(
    n_sets: int = 2000,
    seed: int = 42,
    log_level: str = "INFO",
) -> pd.DataFrame:
    """Run the analysis pipeline using synthetic data.

    Use this when the Internet Archive and Rebrickable APIs are not accessible
    (e.g., in sandboxed environments). Produces realistic synthetic data based
    on known LEGO set trends and runs the full merge/analyze/plot pipeline.

    Args:
        n_sets: Number of synthetic sets to generate.
        seed: Random seed for reproducibility.
        log_level: Logging level.

    Returns:
        The final merged DataFrame.
    """
    setup_logging(log_level)
    from . import synthetic_data

    logger.info("=== Generating synthetic data (API access unavailable) ===")
    data = synthetic_data.generate_all_synthetic_data(n_sets=n_sets, seed=seed)

    ia_index = data["ia_index"]
    set_facts = data["set_facts"]
    manual_metrics = data["manual_metrics"]
    rarity_metrics = data["rarity_metrics"]

    logger.info(f"Generated {len(ia_index)} synthetic sets")

    # Save intermediate parquets for inspection
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ia_index.to_parquet(DATA_DIR / "ia_index.parquet", index=False)
    set_facts.to_parquet(DATA_DIR / "set_facts.parquet", index=False)
    manual_metrics.to_parquet(DATA_DIR / "manual_metrics.parquet", index=False)
    rarity_metrics.to_parquet(DATA_DIR / "rarity_metrics.parquet", index=False)

    logger.info("=== Stage G: Merge and analyze ===")
    merged = stage_g_merge_and_analyze(
        manual_metrics, set_facts, rarity_metrics, force=True
    )

    # Generate plots
    logger.info("=== Generating plots ===")
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    analyze.generate_all_plots(merged, PLOTS_DIR)

    # Print summary
    summary = analyze.print_summary_stats(merged)
    print(summary)

    # Validation
    validation = stage_h_validate(merged)
    print(validation)

    return merged


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LEGO Instruction Complexity Pipeline")
    parser.add_argument("--sample", type=int, default=None, help="Pilot sample size")
    parser.add_argument("--force", action="store_true", help="Force re-run all stages")
    parser.add_argument("--synthetic", action="store_true",
                        help="Use synthetic data (when APIs are not accessible)")
    parser.add_argument("--n-sets", type=int, default=2000,
                        help="Number of synthetic sets (only with --synthetic)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING"])
    args = parser.parse_args()

    if args.synthetic:
        merged = run_synthetic_pipeline(
            n_sets=args.n_sets,
            log_level=args.log_level,
        )
    else:
        merged = run_full_pipeline(
            sample_size=args.sample,
            force=args.force,
            log_level=args.log_level,
        )
    print(f"\nDone! {len(merged)} sets in final dataset.")
