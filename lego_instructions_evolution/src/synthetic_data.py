"""Generate realistic synthetic LEGO data for demonstration.

Used when the real Internet Archive and Rebrickable APIs are not accessible.
All the real pipeline code (ia.py, rebrickable.py, metrics.py) works with actual
API data when run locally with internet access. This module produces realistic
synthetic data that mimics the statistical patterns of LEGO sets across decades
to allow the analysis/visualization pipeline to run end-to-end.

The synthetic data encodes known trends:
- LEGO sets have gotten larger (more pieces) over time, especially since ~2000.
- Instruction page counts have grown, both in absolute terms and per-piece.
- Multi-booklet instructions became common for large sets around ~2005+.
- Part specialization (variety of unique molds) has increased over time.
"""

import numpy as np
import pandas as pd


def generate_synthetic_ia_index(n_sets: int = 2000, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic IA collection index.

    Produces a DataFrame mimicking the output of Stage A (ia_scrape_collection),
    with realistic set number distributions across years.
    """
    rng = np.random.default_rng(seed)

    # Distribute sets across years 1966-2024, with more sets in recent decades
    year_weights = []
    for y in range(1966, 2025):
        if y < 1980:
            w = 0.3
        elif y < 1990:
            w = 0.6
        elif y < 2000:
            w = 1.0
        elif y < 2010:
            w = 1.8
        else:
            w = 3.0
        year_weights.append((y, w))

    years_pool, weights = zip(*year_weights)
    weights = np.array(weights)
    weights /= weights.sum()

    years = rng.choice(years_pool, size=n_sets, p=weights)

    # Generate set numbers that increase with year (roughly)
    set_numbers = []
    for y in years:
        if y < 1980:
            sn = rng.integers(100, 999)
        elif y < 1990:
            sn = rng.integers(1000, 9999)
        elif y < 2000:
            sn = rng.integers(4000, 19999)
        elif y < 2010:
            sn = rng.integers(7000, 39999)
        else:
            sn = rng.integers(10000, 99999)
        set_numbers.append(str(sn))

    # Ensure uniqueness
    seen = set()
    unique_set_numbers = []
    unique_years = []
    for sn, y in zip(set_numbers, years):
        if sn not in seen:
            seen.add(sn)
            unique_set_numbers.append(sn)
            unique_years.append(y)

    n = len(unique_set_numbers)

    identifiers = [f"lego-building-instructions-{sn}" for sn in unique_set_numbers]
    titles = [f"Set {sn} Building Instructions" for sn in unique_set_numbers]

    return pd.DataFrame({
        "identifier": identifiers,
        "title": titles,
        "set_number": unique_set_numbers,
        "date": [""] * n,
        "publicdate": [""] * n,
        "_year": unique_years,  # carry year for downstream use
    })


def generate_synthetic_set_facts(ia_index: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic Rebrickable-like set facts.

    Encodes realistic trends: sets get larger over time, with more unique parts.
    """
    rng = np.random.default_rng(seed)

    rows = []
    for _, item in ia_index.iterrows():
        year = int(item["_year"])
        sn = item["set_number"]

        # Base piece count increases over time
        if year < 1980:
            base_pieces = rng.lognormal(mean=4.0, sigma=0.7)  # ~55 median
        elif year < 1990:
            base_pieces = rng.lognormal(mean=4.5, sigma=0.8)  # ~90 median
        elif year < 2000:
            base_pieces = rng.lognormal(mean=5.0, sigma=0.9)  # ~150 median
        elif year < 2010:
            base_pieces = rng.lognormal(mean=5.3, sigma=1.0)  # ~200 median
        else:
            base_pieces = rng.lognormal(mean=5.6, sigma=1.1)  # ~270 median

        total_pieces = max(int(base_pieces), 10)

        # Unique parts: increases over time as a fraction of total
        if year < 1990:
            unique_frac = rng.uniform(0.15, 0.35)
        elif year < 2005:
            unique_frac = rng.uniform(0.20, 0.45)
        else:
            unique_frac = rng.uniform(0.25, 0.55)

        unique_parts = max(int(total_pieces * unique_frac), 1)

        rows.append({
            "set_number": sn,
            "set_num": f"{sn}-1",
            "year": year,
            "name": f"LEGO Set {sn}",
            "total_pieces": total_pieces,
            "unique_parts": unique_parts,
            "num_parts_rb": total_pieces,
        })

    return pd.DataFrame(rows)


def generate_synthetic_manual_metrics(
    ia_index: pd.DataFrame, set_facts: pd.DataFrame, seed: int = 42
) -> pd.DataFrame:
    """Generate synthetic instruction manual metrics.

    Encodes trends:
    - Pages per piece increases over time (instructions got more detailed)
    - Multi-booklet instructions for large sets, more common after 2005
    - Absolute page counts correlate with piece count but with era-dependent ratio
    """
    rng = np.random.default_rng(seed)

    # Merge to get year and pieces
    merged = ia_index[["set_number", "_year"]].merge(
        set_facts[["set_number", "total_pieces"]], on="set_number", how="inner"
    )

    rows = []
    for _, item in merged.iterrows():
        year = int(item["_year"])
        pieces = int(item["total_pieces"])
        sn = item["set_number"]

        # Pages per piece ratio increases over time
        if year < 1980:
            ppp_ratio = rng.uniform(0.04, 0.10)
        elif year < 1990:
            ppp_ratio = rng.uniform(0.06, 0.14)
        elif year < 2000:
            ppp_ratio = rng.uniform(0.10, 0.20)
        elif year < 2010:
            ppp_ratio = rng.uniform(0.14, 0.28)
        else:
            ppp_ratio = rng.uniform(0.18, 0.35)

        pages_total = max(int(pieces * ppp_ratio) + rng.integers(2, 6), 4)

        # Booklet count: larger sets more likely multi-booklet, esp. after 2005
        if pieces > 500 and year >= 2005:
            booklets = min(int(pages_total / 80) + 1, 6)
            booklets = max(booklets, rng.choice([1, 2, 2, 3]))
        elif pieces > 800:
            booklets = rng.choice([1, 2, 2])
        else:
            booklets = 1

        rows.append({
            "identifier": f"lego-building-instructions-{sn}",
            "set_number": sn,
            "pages_total": pages_total,
            "booklets": booklets,
        })

    return pd.DataFrame(rows)


def generate_synthetic_rarity_metrics(
    set_facts: pd.DataFrame, seed: int = 42
) -> pd.DataFrame:
    """Generate synthetic part rarity metrics.

    Encodes: parts become more specialized over time (higher rarity scores).
    """
    rng = np.random.default_rng(seed)

    rows = []
    for _, item in set_facts.iterrows():
        year = int(item["year"])

        # Base rarity increases over time
        if year < 1985:
            base_rarity = rng.normal(-6.0, 0.8)
        elif year < 1995:
            base_rarity = rng.normal(-5.5, 0.9)
        elif year < 2005:
            base_rarity = rng.normal(-5.0, 1.0)
        elif year < 2015:
            base_rarity = rng.normal(-4.3, 1.1)
        else:
            base_rarity = rng.normal(-3.5, 1.2)

        # Rare part share increases over time
        if year < 1990:
            rare_share = rng.uniform(0.01, 0.06)
        elif year < 2005:
            rare_share = rng.uniform(0.03, 0.10)
        else:
            rare_share = rng.uniform(0.06, 0.18)

        rows.append({
            "set_number": item["set_number"],
            "rarity_wmean": base_rarity,
            "rare_part_share": rare_share,
        })

    return pd.DataFrame(rows)


def generate_all_synthetic_data(n_sets: int = 2000, seed: int = 42) -> dict[str, pd.DataFrame]:
    """Generate a complete synthetic dataset for all pipeline stages.

    Returns dict with keys: ia_index, set_facts, manual_metrics, rarity_metrics.
    """
    ia_index = generate_synthetic_ia_index(n_sets=n_sets, seed=seed)
    set_facts = generate_synthetic_set_facts(ia_index, seed=seed)
    manual_metrics = generate_synthetic_manual_metrics(ia_index, set_facts, seed=seed)
    rarity_metrics = generate_synthetic_rarity_metrics(set_facts, seed=seed)

    return {
        "ia_index": ia_index,
        "set_facts": set_facts,
        "manual_metrics": manual_metrics,
        "rarity_metrics": rarity_metrics,
    }
