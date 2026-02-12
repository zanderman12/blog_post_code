"""Tests for the synthetic data generation module."""

import numpy as np
import pandas as pd
import pytest

from src.synthetic_data import (
    generate_synthetic_ia_index,
    generate_synthetic_set_facts,
    generate_synthetic_manual_metrics,
    generate_synthetic_rarity_metrics,
    generate_all_synthetic_data,
)


class TestGenerateSyntheticIaIndex:
    def test_correct_size(self):
        df = generate_synthetic_ia_index(n_sets=100)
        # May be slightly less than 100 due to deduplication
        assert len(df) > 80
        assert len(df) <= 100

    def test_has_required_columns(self):
        df = generate_synthetic_ia_index(n_sets=50)
        assert "identifier" in df.columns
        assert "title" in df.columns
        assert "set_number" in df.columns
        assert "_year" in df.columns

    def test_set_numbers_unique(self):
        df = generate_synthetic_ia_index(n_sets=200)
        assert df["set_number"].is_unique

    def test_year_range(self):
        df = generate_synthetic_ia_index(n_sets=500)
        assert df["_year"].min() >= 1966
        assert df["_year"].max() <= 2024

    def test_reproducible(self):
        df1 = generate_synthetic_ia_index(n_sets=50, seed=123)
        df2 = generate_synthetic_ia_index(n_sets=50, seed=123)
        pd.testing.assert_frame_equal(df1, df2)


class TestGenerateSyntheticSetFacts:
    def test_correct_size(self):
        ia = generate_synthetic_ia_index(n_sets=100)
        facts = generate_synthetic_set_facts(ia)
        assert len(facts) == len(ia)

    def test_piece_counts_positive(self):
        ia = generate_synthetic_ia_index(n_sets=200)
        facts = generate_synthetic_set_facts(ia)
        assert (facts["total_pieces"] >= 10).all()
        assert (facts["unique_parts"] >= 1).all()

    def test_unique_parts_less_than_total(self):
        ia = generate_synthetic_ia_index(n_sets=200)
        facts = generate_synthetic_set_facts(ia)
        assert (facts["unique_parts"] <= facts["total_pieces"]).all()

    def test_pieces_increase_over_time(self):
        ia = generate_synthetic_ia_index(n_sets=1000, seed=42)
        facts = generate_synthetic_set_facts(ia, seed=42)
        early = facts[facts["year"] < 1985]["total_pieces"].median()
        recent = facts[facts["year"] >= 2015]["total_pieces"].median()
        assert recent > early  # sets get bigger over time


class TestGenerateSyntheticManualMetrics:
    def test_correct_size(self):
        ia = generate_synthetic_ia_index(n_sets=100)
        facts = generate_synthetic_set_facts(ia)
        metrics = generate_synthetic_manual_metrics(ia, facts)
        assert len(metrics) == len(ia)

    def test_pages_positive(self):
        ia = generate_synthetic_ia_index(n_sets=200)
        facts = generate_synthetic_set_facts(ia)
        metrics = generate_synthetic_manual_metrics(ia, facts)
        assert (metrics["pages_total"] >= 4).all()
        assert (metrics["booklets"] >= 1).all()

    def test_pages_per_piece_increases(self):
        ia = generate_synthetic_ia_index(n_sets=1000, seed=42)
        facts = generate_synthetic_set_facts(ia, seed=42)
        metrics = generate_synthetic_manual_metrics(ia, facts, seed=42)

        merged = metrics.merge(facts[["set_number", "year", "total_pieces"]], on="set_number")
        merged["ppp"] = merged["pages_total"] / merged["total_pieces"]

        early = merged[merged["year"] < 1985]["ppp"].median()
        recent = merged[merged["year"] >= 2015]["ppp"].median()
        assert recent > early  # instructions get more detailed


class TestGenerateSyntheticRarityMetrics:
    def test_correct_size(self):
        ia = generate_synthetic_ia_index(n_sets=100)
        facts = generate_synthetic_set_facts(ia)
        rarity = generate_synthetic_rarity_metrics(facts)
        assert len(rarity) == len(facts)

    def test_rarity_increases_over_time(self):
        ia = generate_synthetic_ia_index(n_sets=1000, seed=42)
        facts = generate_synthetic_set_facts(ia, seed=42)
        rarity = generate_synthetic_rarity_metrics(facts, seed=42)

        merged = facts[["set_number", "year"]].merge(rarity, on="set_number")
        early = merged[merged["year"] < 1985]["rarity_wmean"].median()
        recent = merged[merged["year"] >= 2015]["rarity_wmean"].median()
        assert recent > early  # parts become more specialized


class TestGenerateAllSyntheticData:
    def test_returns_all_keys(self):
        data = generate_all_synthetic_data(n_sets=50)
        assert "ia_index" in data
        assert "set_facts" in data
        assert "manual_metrics" in data
        assert "rarity_metrics" in data

    def test_consistent_set_numbers(self):
        data = generate_all_synthetic_data(n_sets=100)
        ia_sns = set(data["ia_index"]["set_number"])
        facts_sns = set(data["set_facts"]["set_number"])
        manual_sns = set(data["manual_metrics"]["set_number"])
        rarity_sns = set(data["rarity_metrics"]["set_number"])

        assert ia_sns == facts_sns
        assert ia_sns == manual_sns
        assert ia_sns == rarity_sns
