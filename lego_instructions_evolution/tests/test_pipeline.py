"""Tests for the pipeline module."""

import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pandas as pd
import pytest

from src.pipeline import (
    stage_g_merge_and_analyze,
    stage_h_validate,
)


@pytest.fixture
def manual_metrics():
    return pd.DataFrame({
        "identifier": ["id1", "id2", "id3"],
        "set_number": ["10000", "20200", "30300"],
        "pages_total": [50, 100, 200],
        "booklets": [1, 2, 3],
    })


@pytest.fixture
def set_facts():
    return pd.DataFrame({
        "set_number": ["10000", "20200", "30300"],
        "set_num": ["10000-1", "20200-1", "30300-1"],
        "year": [1990, 2010, 2022],
        "name": ["Set A", "Set B", "Set C"],
        "total_pieces": [200, 800, 2000],
        "unique_parts": [80, 300, 700],
        "num_parts_rb": [200, 800, 2000],
    })


@pytest.fixture
def rarity_metrics():
    return pd.DataFrame({
        "set_number": ["10000", "20200", "30300"],
        "rarity_wmean": [2.5, 3.0, 4.0],
        "rare_part_share": [0.05, 0.10, 0.15],
    })


class TestStageGMergeAndAnalyze:
    def test_merge(self, manual_metrics, set_facts, rarity_metrics):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.pipeline.DATA_DIR", Path(tmpdir)):
                result = stage_g_merge_and_analyze(
                    manual_metrics, set_facts, rarity_metrics, force=True
                )

        assert len(result) == 3
        assert "pages_per_100_pieces" in result.columns
        assert "rarity_wmean" in result.columns
        assert "size_band" in result.columns

    def test_merge_empty_rarity(self, manual_metrics, set_facts):
        empty_rarity = pd.DataFrame(columns=["set_number", "rarity_wmean", "rare_part_share"])
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.pipeline.DATA_DIR", Path(tmpdir)):
                result = stage_g_merge_and_analyze(
                    manual_metrics, set_facts, empty_rarity, force=True
                )

        assert len(result) == 3
        assert all(result["rarity_wmean"].isna())

    def test_filters_zero_pieces(self, manual_metrics, set_facts, rarity_metrics):
        # Add a row with zero pieces
        set_facts_with_zero = pd.concat([set_facts, pd.DataFrame({
            "set_number": ["40000"],
            "set_num": ["40000-1"],
            "year": [2020],
            "name": ["Empty"],
            "total_pieces": [0],
            "unique_parts": [0],
            "num_parts_rb": [0],
        })], ignore_index=True)
        manual_with_extra = pd.concat([manual_metrics, pd.DataFrame({
            "identifier": ["id4"],
            "set_number": ["40000"],
            "pages_total": [10],
            "booklets": [1],
        })], ignore_index=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.pipeline.DATA_DIR", Path(tmpdir)):
                result = stage_g_merge_and_analyze(
                    manual_with_extra, set_facts_with_zero, rarity_metrics, force=True
                )

        # Row with 0 pieces should be filtered out
        assert "40000" not in result["set_number"].values


class TestStageHValidate:
    def test_validation_report(self, manual_metrics, set_facts, rarity_metrics):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("src.pipeline.DATA_DIR", Path(tmpdir)):
                merged = stage_g_merge_and_analyze(
                    manual_metrics, set_facts, rarity_metrics, force=True
                )

        report = stage_h_validate(merged)
        assert "VALIDATION REPORT" in report
        assert "Total rows:" in report
        assert "Sets per decade" in report
        assert "Sensitivity" in report
