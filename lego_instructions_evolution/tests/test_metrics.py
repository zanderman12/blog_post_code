"""Tests for the metrics module."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd

from src.metrics import (
    pdf_page_count,
    estimate_build_pages,
    compute_derived_metrics,
    compute_global_part_freq,
    set_rarity_scores,
    compute_manual_metrics,
)


class TestPdfPageCount:
    def test_nonexistent_file(self):
        result = pdf_page_count(Path("/nonexistent/file.pdf"))
        assert result == 0

    def test_invalid_file(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            f.write(b"not a real pdf")
            f.flush()
            result = pdf_page_count(Path(f.name))
            # Should return 0 on error rather than raising
            assert result == 0


class TestEstimateBuildPages:
    def test_default_subtraction(self):
        assert estimate_build_pages(50) == 47  # 50 - 2 - 1

    def test_custom_subtraction(self):
        assert estimate_build_pages(50, front_matter=5, back_matter=3) == 42

    def test_clamp_at_one(self):
        assert estimate_build_pages(2) == 1  # 2 - 2 - 1 = -1 -> clamped to 1

    def test_exactly_three(self):
        assert estimate_build_pages(3) == 1  # 3 - 2 - 1 = 0 -> clamped to 1

    def test_four_pages(self):
        assert estimate_build_pages(4) == 1  # 4 - 2 - 1 = 1


class TestComputeDerivedMetrics:
    def test_normal_set(self):
        row = pd.Series({
            "pages_total": 100,
            "total_pieces": 500,
            "unique_parts": 200,
            "booklets": 2,
        })
        result = compute_derived_metrics(row)
        assert result["pages_per_100_pieces"] == pytest.approx(20.0)
        assert result["unique_ratio"] == pytest.approx(0.4)
        assert result["pieces_per_page_est"] == pytest.approx(500 / 97)

    def test_zero_pieces(self):
        row = pd.Series({
            "pages_total": 10,
            "total_pieces": 0,
            "unique_parts": 0,
            "booklets": 1,
        })
        result = compute_derived_metrics(row)
        assert np.isnan(result["pages_per_100_pieces"])
        assert np.isnan(result["unique_ratio"])

    def test_small_set(self):
        row = pd.Series({
            "pages_total": 10,
            "total_pieces": 50,
            "unique_parts": 30,
            "booklets": 1,
        })
        result = compute_derived_metrics(row)
        assert result["pages_per_100_pieces"] == pytest.approx(20.0)
        assert result["unique_ratio"] == pytest.approx(0.6)


class TestComputeGlobalPartFreq:
    def test_frequency_counts(self):
        inv_df = pd.DataFrame({
            "id": [1, 2, 3],
            "set_num": ["A-1", "B-1", "C-1"],
        })
        inv_parts_df = pd.DataFrame({
            "inventory_id": [1, 1, 2, 2, 3],
            "part_num": ["p1", "p2", "p1", "p3", "p1"],
        })

        freq = compute_global_part_freq(inv_parts_df, inv_df)
        assert freq["p1"] == 3  # appears in sets A, B, C
        assert freq["p2"] == 1  # appears in set A only
        assert freq["p3"] == 1  # appears in set B only


class TestSetRarityScores:
    def test_basic_rarity(self):
        set_parts = pd.DataFrame({
            "part_num": ["common", "rare"],
            "quantity": [10, 5],
        })
        part_set_counts = pd.Series({"common": 1000, "rare": 2}, name="count")

        result = set_rarity_scores(set_parts, part_set_counts)
        assert "rarity_wmean" in result
        assert "rare_part_share" in result
        assert not np.isnan(result["rarity_wmean"])
        # -log(freq) is negative for freq > 1; the rare part (freq=2) has higher
        # rarity than the common part (freq=1000), so weighted mean is dominated
        # by the common part's strongly negative value
        assert isinstance(result["rarity_wmean"], float)

    def test_empty_parts(self):
        set_parts = pd.DataFrame(columns=["part_num", "quantity"])
        part_set_counts = pd.Series(dtype=float)

        result = set_rarity_scores(set_parts, part_set_counts)
        assert np.isnan(result["rarity_wmean"])
        assert np.isnan(result["rare_part_share"])

    def test_all_common_parts(self):
        set_parts = pd.DataFrame({
            "part_num": ["p1", "p2", "p3"],
            "quantity": [5, 5, 5],
        })
        # All parts appear in many sets
        part_set_counts = pd.Series({"p1": 5000, "p2": 4000, "p3": 3000})

        result = set_rarity_scores(set_parts, part_set_counts)
        # All common => rarity should be relatively low (large negative log values)
        assert result["rarity_wmean"] < 0  # -log of large numbers is negative


class TestComputeManualMetrics:
    @patch("src.metrics.download_pdf")
    @patch("src.metrics.pdf_page_count")
    def test_multiple_booklets(self, mock_count, mock_download):
        mock_download.return_value = Path("/tmp/fake.pdf")
        mock_count.side_effect = [50, 30]

        result = compute_manual_metrics(
            "test-id", ["book1.pdf", "book2.pdf"], Path("/tmp/manuals")
        )
        assert result["pages_total"] == 80
        assert result["booklets"] == 2
        assert result["identifier"] == "test-id"
        assert len(result["per_booklet_pages"]) == 2

    @patch("src.metrics.download_pdf")
    @patch("src.metrics.pdf_page_count")
    def test_single_booklet(self, mock_count, mock_download):
        mock_download.return_value = Path("/tmp/fake.pdf")
        mock_count.return_value = 100

        result = compute_manual_metrics(
            "test-id", ["instructions.pdf"], Path("/tmp/manuals")
        )
        assert result["pages_total"] == 100
        assert result["booklets"] == 1

    @patch("src.metrics.download_pdf")
    def test_download_failure_skips(self, mock_download):
        mock_download.side_effect = RuntimeError("download failed")

        result = compute_manual_metrics(
            "test-id", ["bad.pdf"], Path("/tmp/manuals")
        )
        assert result["pages_total"] == 0
        assert result["booklets"] == 0
