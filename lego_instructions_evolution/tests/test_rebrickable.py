"""Tests for the Rebrickable module."""

import pytest
import pandas as pd

from src.rebrickable import match_set, compute_set_inventory_metrics, build_set_facts


@pytest.fixture
def sets_df():
    return pd.DataFrame({
        "set_num": ["10000-1", "10001-1", "10001-2", "20200-1", "375-1"],
        "name": ["Set A", "Set B", "Set B Variant", "Set C", "Castle"],
        "year": [2000, 2001, 2001, 2020, 1978],
        "num_parts": [100, 200, 210, 500, 50],
    })


@pytest.fixture
def inv_df():
    return pd.DataFrame({
        "id": [1, 2, 3, 4],
        "set_num": ["10000-1", "10001-1", "20200-1", "375-1"],
        "version": [1, 1, 1, 1],
    })


@pytest.fixture
def inv_parts_df():
    return pd.DataFrame({
        "inventory_id": [1, 1, 1, 2, 2, 3, 3, 3, 3, 4],
        "part_num": ["3001", "3002", "3003", "3001", "3004", "3001", "3005", "3006", "3007", "3001"],
        "quantity": [10, 20, 5, 30, 10, 100, 50, 75, 25, 10],
        "color_id": [0] * 10,
        "is_spare": ["f"] * 10,
    })


class TestMatchSet:
    def test_exact_match(self, sets_df):
        result = match_set(sets_df, "10000")
        assert result is not None
        assert result["set_num"] == "10000-1"
        assert result["year"] == 2000

    def test_fallback_first_variant(self, sets_df):
        result = match_set(sets_df, "10001")
        assert result is not None
        assert result["set_num"] == "10001-1"

    def test_no_match(self, sets_df):
        result = match_set(sets_df, "99999")
        assert result is None

    def test_three_digit_number(self, sets_df):
        result = match_set(sets_df, "375")
        assert result is not None
        assert result["set_num"] == "375-1"


class TestComputeSetInventoryMetrics:
    def test_basic_metrics(self, inv_df, inv_parts_df):
        total, unique, parts = compute_set_inventory_metrics(
            inv_df, inv_parts_df, "10000-1"
        )
        assert total == 35  # 10 + 20 + 5
        assert unique == 3  # 3001, 3002, 3003
        assert len(parts) == 3

    def test_missing_set(self, inv_df, inv_parts_df):
        total, unique, parts = compute_set_inventory_metrics(
            inv_df, inv_parts_df, "99999-1"
        )
        assert total == 0
        assert unique == 0
        assert parts.empty

    def test_larger_set(self, inv_df, inv_parts_df):
        total, unique, parts = compute_set_inventory_metrics(
            inv_df, inv_parts_df, "20200-1"
        )
        assert total == 250  # 100 + 50 + 75 + 25
        assert unique == 4  # 3001, 3005, 3006, 3007


class TestBuildSetFacts:
    def test_builds_facts(self, sets_df, inv_df, inv_parts_df):
        ia_index = pd.DataFrame({
            "set_number": ["10000", "20200", "99999"],
            "identifier": ["id1", "id2", "id3"],
        })

        result = build_set_facts(ia_index, sets_df, inv_df, inv_parts_df)
        assert len(result) == 2  # 99999 shouldn't match
        assert "10000" in result["set_number"].values
        assert "20200" in result["set_number"].values

        row_10000 = result[result["set_number"] == "10000"].iloc[0]
        assert row_10000["year"] == 2000
        assert row_10000["total_pieces"] == 35

    def test_uses_num_parts_fallback(self, sets_df):
        # Empty inventory data -> should fall back to num_parts
        ia_index = pd.DataFrame({
            "set_number": ["10000"],
            "identifier": ["id1"],
        })
        empty_inv = pd.DataFrame(columns=["id", "set_num", "version"])
        empty_inv_parts = pd.DataFrame(columns=["inventory_id", "part_num", "quantity", "color_id", "is_spare"])

        result = build_set_facts(ia_index, sets_df, empty_inv, empty_inv_parts)
        assert len(result) == 1
        assert result.iloc[0]["total_pieces"] == 100  # num_parts from sets_df
