"""Tests for the analysis module."""

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.analyze import (
    add_derived_columns,
    compute_yearly_stats,
    compute_decade_stats,
    print_summary_stats,
    generate_all_plots,
)


@pytest.fixture
def sample_df():
    """Create a sample merged dataset for testing."""
    np.random.seed(42)
    n = 100
    years = np.random.choice(range(1970, 2025), size=n)
    pieces = np.random.randint(10, 3000, size=n)
    pages = (pieces * np.random.uniform(0.05, 0.4, size=n)).astype(int).clip(min=4)
    unique = (pieces * np.random.uniform(0.2, 0.8, size=n)).astype(int).clip(min=1)
    booklets = np.random.choice([1, 1, 1, 2, 2, 3], size=n)

    df = pd.DataFrame({
        "set_number": [str(10000 + i) for i in range(n)],
        "year": years,
        "pages_total": pages,
        "total_pieces": pieces,
        "unique_parts": unique,
        "booklets": booklets,
        "rarity_wmean": np.random.uniform(-2, 5, size=n),
        "rare_part_share": np.random.uniform(0, 0.5, size=n),
    })
    return df


class TestAddDerivedColumns:
    def test_adds_all_columns(self, sample_df):
        result = add_derived_columns(sample_df)
        assert "pages_per_100_pieces" in result.columns
        assert "unique_ratio" in result.columns
        assert "build_pages_est" in result.columns
        assert "pieces_per_page_est" in result.columns
        assert "size_band" in result.columns
        assert "decade" in result.columns

    def test_pages_per_100_pieces_calc(self, sample_df):
        result = add_derived_columns(sample_df)
        row = result.iloc[0]
        expected = 100.0 * row["pages_total"] / row["total_pieces"]
        assert row["pages_per_100_pieces"] == pytest.approx(expected)

    def test_size_bands_correct(self, sample_df):
        result = add_derived_columns(sample_df)
        # Check that a tiny set is categorized correctly
        tiny = result[result["total_pieces"] < 100]
        if len(tiny) > 0:
            assert all(tiny["size_band"] == "Tiny (<100)")

    def test_decade_calculation(self, sample_df):
        result = add_derived_columns(sample_df)
        # Year 2020 -> decade 2020
        row_2020 = result[result["year"] == 2020]
        if len(row_2020) > 0:
            assert all(row_2020["decade"] == 2020)

    def test_zero_pieces_produces_nan(self):
        df = pd.DataFrame({
            "set_number": ["1"],
            "year": [2020],
            "pages_total": [10],
            "total_pieces": [0],
            "unique_parts": [0],
            "booklets": [1],
            "rarity_wmean": [0.0],
            "rare_part_share": [0.0],
        })
        result = add_derived_columns(df)
        assert np.isnan(result.iloc[0]["pages_per_100_pieces"])
        assert np.isnan(result.iloc[0]["unique_ratio"])


class TestComputeYearlyStats:
    def test_aggregation(self, sample_df):
        df = add_derived_columns(sample_df)
        yearly = compute_yearly_stats(df)
        assert "year" in yearly.columns
        assert "n_sets" in yearly.columns
        assert "median_pages" in yearly.columns
        assert yearly["n_sets"].sum() == len(sample_df)


class TestComputeDecadeStats:
    def test_aggregation(self, sample_df):
        df = add_derived_columns(sample_df)
        decade = compute_decade_stats(df)
        assert "decade" in decade.columns
        assert "n_sets" in decade.columns
        assert decade["n_sets"].sum() == len(sample_df)


class TestPrintSummaryStats:
    def test_returns_string(self, sample_df):
        df = add_derived_columns(sample_df)
        summary = print_summary_stats(df)
        assert isinstance(summary, str)
        assert "Total sets analyzed: 100" in summary
        assert "Decade Comparison" in summary


class TestGenerateAllPlots:
    def test_generates_plots(self, sample_df):
        df = add_derived_columns(sample_df)
        with tempfile.TemporaryDirectory() as tmpdir:
            plots = generate_all_plots(df, Path(tmpdir))
            assert len(plots) == 8
            for p in plots:
                assert p.exists()
                assert p.suffix == ".png"
