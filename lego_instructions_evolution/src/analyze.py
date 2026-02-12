"""Analysis and visualization of LEGO instruction complexity trends."""

import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add all derived metric columns to the merged dataset."""
    df = df.copy()

    # Pages per 100 pieces
    df["pages_per_100_pieces"] = np.where(
        df["total_pieces"] > 0,
        100.0 * df["pages_total"] / df["total_pieces"],
        np.nan,
    )

    # Unique ratio
    df["unique_ratio"] = np.where(
        df["total_pieces"] > 0,
        df["unique_parts"] / df["total_pieces"],
        np.nan,
    )

    # Estimated build pages (subtract 3 for front/back matter)
    df["build_pages_est"] = (df["pages_total"] - 3).clip(lower=1)

    # Pieces per page estimate
    df["pieces_per_page_est"] = np.where(
        df["build_pages_est"] > 0,
        df["total_pieces"] / df["build_pages_est"],
        np.nan,
    )

    # Size band for stratified analysis
    df["size_band"] = pd.cut(
        df["total_pieces"],
        bins=[0, 100, 300, 700, 1500, float("inf")],
        labels=["Tiny (<100)", "Small (100-300)", "Medium (300-700)", "Large (700-1500)", "Huge (1500+)"],
    )

    # Decade bins
    df["decade"] = (df["year"] // 10) * 10

    return df


def compute_yearly_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute yearly aggregated statistics."""
    yearly = df.groupby("year").agg(
        n_sets=("set_number", "count"),
        median_pages=("pages_total", "median"),
        median_pieces=("total_pieces", "median"),
        median_pages_per_100=("pages_per_100_pieces", "median"),
        median_pieces_per_page=("pieces_per_page_est", "median"),
        median_unique_ratio=("unique_ratio", "median"),
        median_booklets=("booklets", "median"),
        mean_pages=("pages_total", "mean"),
        mean_pieces=("total_pieces", "mean"),
        mean_pages_per_100=("pages_per_100_pieces", "mean"),
    ).reset_index()
    return yearly


def compute_decade_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute decade-level aggregated statistics."""
    decade = df.groupby("decade").agg(
        n_sets=("set_number", "count"),
        median_pages=("pages_total", "median"),
        median_pieces=("total_pieces", "median"),
        median_pages_per_100=("pages_per_100_pieces", "median"),
        median_pieces_per_page=("pieces_per_page_est", "median"),
        median_unique_ratio=("unique_ratio", "median"),
        median_booklets=("booklets", "median"),
        mean_rarity=("rarity_wmean", lambda x: x.median()),
        mean_rare_share=("rare_part_share", lambda x: x.median()),
    ).reset_index()
    return decade


def plot_pages_vs_year(df: pd.DataFrame, out_dir: Path) -> Path:
    """Scatter plot of total pages vs year, colored by size band."""
    fig, ax = plt.subplots(figsize=(12, 7))

    size_bands = df["size_band"].cat.categories if hasattr(df["size_band"], "cat") else df["size_band"].unique()
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(size_bands)))

    for band, color in zip(size_bands, colors):
        mask = df["size_band"] == band
        subset = df[mask]
        ax.scatter(
            subset["year"], subset["pages_total"],
            c=[color], alpha=0.3, s=15, label=str(band),
        )

    # Rolling median trend
    yearly = df.groupby("year")["pages_total"].median()
    ax.plot(yearly.index, yearly.values, color="red", linewidth=2.5, label="Yearly median")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Total Instruction Pages", fontsize=12)
    ax.set_title("LEGO Instruction Page Count Over Time", fontsize=14)
    ax.legend(fontsize=9, loc="upper left")
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "pages_vs_year.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_pages_per_100_pieces(df: pd.DataFrame, out_dir: Path) -> Path:
    """Scatter + trend of pages per 100 pieces over time."""
    fig, ax = plt.subplots(figsize=(12, 7))

    valid = df.dropna(subset=["pages_per_100_pieces"])
    ax.scatter(
        valid["year"], valid["pages_per_100_pieces"],
        alpha=0.2, s=12, c="steelblue",
    )

    # Rolling median trend line
    yearly = valid.groupby("year")["pages_per_100_pieces"].median()
    ax.plot(yearly.index, yearly.values, color="red", linewidth=2.5, label="Yearly median")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Pages per 100 Pieces", fontsize=12)
    ax.set_title("Instruction Density: Pages per 100 Pieces Over Time", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "pages_per_100_pieces.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_rarity_vs_year(df: pd.DataFrame, out_dir: Path) -> Path:
    """Scatter + trend of part rarity over time."""
    fig, ax = plt.subplots(figsize=(12, 7))

    valid = df.dropna(subset=["rarity_wmean"])
    ax.scatter(
        valid["year"], valid["rarity_wmean"],
        alpha=0.2, s=12, c="darkorange",
    )

    yearly = valid.groupby("year")["rarity_wmean"].median()
    ax.plot(yearly.index, yearly.values, color="red", linewidth=2.5, label="Yearly median")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Weighted Mean Part Rarity (-log freq)", fontsize=12)
    ax.set_title("Part Specialization Over Time", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "rarity_vs_year.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_booklets_vs_year(df: pd.DataFrame, out_dir: Path) -> Path:
    """Box/violin plot of booklet count by decade."""
    fig, ax = plt.subplots(figsize=(12, 7))

    decades = sorted(df["decade"].dropna().unique())
    data_by_decade = [df[df["decade"] == d]["booklets"].dropna().values for d in decades]

    bp = ax.boxplot(
        data_by_decade, tick_labels=[str(int(d)) + "s" for d in decades],
        patch_artist=True, showfliers=False,
    )
    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")

    ax.set_xlabel("Decade", fontsize=12)
    ax.set_ylabel("Number of Instruction Booklets", fontsize=12)
    ax.set_title("Instruction Booklet Count by Decade", fontsize=14)
    ax.grid(True, alpha=0.3, axis="y")

    out_path = out_dir / "booklets_by_decade.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_pieces_per_page_vs_year(df: pd.DataFrame, out_dir: Path) -> Path:
    """Scatter + trend of estimated pieces per page over time."""
    fig, ax = plt.subplots(figsize=(12, 7))

    valid = df.dropna(subset=["pieces_per_page_est"])
    ax.scatter(
        valid["year"], valid["pieces_per_page_est"],
        alpha=0.2, s=12, c="seagreen",
    )

    yearly = valid.groupby("year")["pieces_per_page_est"].median()
    ax.plot(yearly.index, yearly.values, color="red", linewidth=2.5, label="Yearly median")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Pieces per Page (est.)", fontsize=12)
    ax.set_title("Build Density: Estimated Pieces per Page Over Time", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "pieces_per_page_vs_year.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_unique_ratio_vs_year(df: pd.DataFrame, out_dir: Path) -> Path:
    """Scatter + trend of unique part ratio over time."""
    fig, ax = plt.subplots(figsize=(12, 7))

    valid = df.dropna(subset=["unique_ratio"])
    ax.scatter(
        valid["year"], valid["unique_ratio"],
        alpha=0.2, s=12, c="mediumpurple",
    )

    yearly = valid.groupby("year")["unique_ratio"].median()
    ax.plot(yearly.index, yearly.values, color="red", linewidth=2.5, label="Yearly median")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Unique Parts / Total Pieces", fontsize=12)
    ax.set_title("Part Variety: Unique Ratio Over Time", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "unique_ratio_vs_year.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_sensitivity_analysis(df: pd.DataFrame, out_dir: Path) -> Path:
    """Show pieces_per_page_est trend under different page subtraction assumptions."""
    fig, ax = plt.subplots(figsize=(12, 7))

    for subtract in [2, 3, 4, 5]:
        build_pages = (df["pages_total"] - subtract).clip(lower=1)
        ppp = df["total_pieces"] / build_pages
        yearly = ppp.groupby(df["year"]).median()
        ax.plot(yearly.index, yearly.values, linewidth=2, label=f"Subtract {subtract} pages")

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Pieces per Page (est.)", fontsize=12)
    ax.set_title("Sensitivity: Pieces per Page Under Different Front/Back Matter Assumptions", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "sensitivity_pieces_per_page.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def plot_size_band_trends(df: pd.DataFrame, out_dir: Path) -> Path:
    """Pages per 100 pieces trend, broken out by size band."""
    fig, ax = plt.subplots(figsize=(12, 7))

    size_bands = df["size_band"].cat.categories if hasattr(df["size_band"], "cat") else sorted(df["size_band"].dropna().unique())
    colors = plt.cm.tab10(np.linspace(0, 0.8, len(size_bands)))

    for band, color in zip(size_bands, colors):
        subset = df[df["size_band"] == band].dropna(subset=["pages_per_100_pieces"])
        if len(subset) < 5:
            continue
        yearly = subset.groupby("year")["pages_per_100_pieces"].median()
        # Smooth with rolling window
        smoothed = yearly.rolling(3, center=True, min_periods=1).mean()
        ax.plot(smoothed.index, smoothed.values, linewidth=2, label=str(band), color=color)

    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Pages per 100 Pieces", fontsize=12)
    ax.set_title("Instruction Density by Set Size Band Over Time", fontsize=14)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    out_path = out_dir / "size_band_trends.png"
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved {out_path}")
    return out_path


def generate_all_plots(df: pd.DataFrame, out_dir: Path) -> list[Path]:
    """Generate all analysis plots. Returns list of saved paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    plots = []

    plots.append(plot_pages_vs_year(df, out_dir))
    plots.append(plot_pages_per_100_pieces(df, out_dir))
    plots.append(plot_rarity_vs_year(df, out_dir))
    plots.append(plot_booklets_vs_year(df, out_dir))
    plots.append(plot_pieces_per_page_vs_year(df, out_dir))
    plots.append(plot_unique_ratio_vs_year(df, out_dir))
    plots.append(plot_sensitivity_analysis(df, out_dir))
    plots.append(plot_size_band_trends(df, out_dir))

    return plots


def print_summary_stats(df: pd.DataFrame) -> str:
    """Generate a text summary of key findings."""
    lines = []
    lines.append("=" * 60)
    lines.append("LEGO INSTRUCTION COMPLEXITY ANALYSIS - SUMMARY")
    lines.append("=" * 60)
    lines.append(f"\nTotal sets analyzed: {len(df)}")
    lines.append(f"Year range: {int(df['year'].min())} - {int(df['year'].max())}")
    lines.append(f"\nMedian pages total: {df['pages_total'].median():.0f}")
    lines.append(f"Median total pieces: {df['total_pieces'].median():.0f}")
    lines.append(f"Median booklets: {df['booklets'].median():.0f}")

    # Decade comparison
    lines.append("\n--- Decade Comparison ---")
    decade_stats = compute_decade_stats(df)
    for _, row in decade_stats.iterrows():
        if row["n_sets"] >= 5:
            lines.append(
                f"  {int(row['decade'])}s: {int(row['n_sets'])} sets, "
                f"median pages={row['median_pages']:.0f}, "
                f"median pieces={row['median_pieces']:.0f}, "
                f"pages/100pc={row['median_pages_per_100']:.1f}, "
                f"booklets={row['median_booklets']:.1f}"
            )

    # Early vs recent comparison
    early = df[df["year"] <= 2000]
    recent = df[df["year"] >= 2015]
    if len(early) > 10 and len(recent) > 10:
        lines.append("\n--- Early (<=2000) vs Recent (>=2015) ---")
        lines.append(f"  Early: median pages/100pc = {early['pages_per_100_pieces'].median():.2f}")
        lines.append(f"  Recent: median pages/100pc = {recent['pages_per_100_pieces'].median():.2f}")
        lines.append(f"  Early: median pieces/page = {early['pieces_per_page_est'].median():.2f}")
        lines.append(f"  Recent: median pieces/page = {recent['pieces_per_page_est'].median():.2f}")

        if "rarity_wmean" in df.columns:
            e_rar = early["rarity_wmean"].median()
            r_rar = recent["rarity_wmean"].median()
            if not np.isnan(e_rar) and not np.isnan(r_rar):
                lines.append(f"  Early: median rarity = {e_rar:.2f}")
                lines.append(f"  Recent: median rarity = {r_rar:.2f}")

    summary = "\n".join(lines)
    return summary
