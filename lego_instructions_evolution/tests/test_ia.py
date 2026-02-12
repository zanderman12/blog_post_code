"""Tests for the Internet Archive module."""

import pytest
from unittest.mock import patch, MagicMock

from src.ia import (
    parse_set_number,
    list_original_pdfs,
    build_ia_index,
    ia_scrape_collection,
    ia_fetch_item_metadata,
)


class TestParseSetNumber:
    def test_basic_identifier(self):
        assert parse_set_number("lego-building-instructions-20200") == "20200"

    def test_identifier_with_prefix(self):
        assert parse_set_number("lego-set-42115-instructions") == "42115"

    def test_from_title_fallback(self):
        assert parse_set_number("no-digits-here", "Set 75192 Millennium Falcon") == "75192"

    def test_short_number(self):
        assert parse_set_number("lego-set-375") == "375"

    def test_no_number_found(self):
        assert parse_set_number("no-digits", "") is None

    def test_empty_strings(self):
        assert parse_set_number("", "") is None

    def test_multiple_numbers_takes_first(self):
        result = parse_set_number("lego-12345-extra-678")
        assert result == "12345"


class TestListOriginalPdfs:
    def test_finds_original_pdfs(self):
        meta = {
            "files": [
                {"name": "instructions.pdf", "source": "original"},
                {"name": "instructions_djvu.xml", "source": "derivative"},
                {"name": "book2.PDF", "source": "original"},
                {"name": "cover.jpg", "source": "original"},
            ]
        }
        result = list_original_pdfs(meta)
        assert result == ["instructions.pdf", "book2.PDF"]

    def test_empty_files(self):
        assert list_original_pdfs({"files": []}) == []

    def test_no_files_key(self):
        assert list_original_pdfs({}) == []

    def test_no_original_pdfs(self):
        meta = {
            "files": [
                {"name": "instructions.pdf", "source": "derivative"},
            ]
        }
        assert list_original_pdfs(meta) == []


class TestBuildIaIndex:
    def test_basic_index(self):
        items = [
            {"identifier": "lego-building-instructions-42100", "title": "LEGO 42100"},
            {"identifier": "lego-building-instructions-75192", "title": "LEGO 75192"},
        ]
        index = build_ia_index(items)
        assert len(index) == 2
        assert index[0]["set_number"] == "42100"
        assert index[1]["set_number"] == "75192"
        assert index[0]["identifier"] == "lego-building-instructions-42100"

    def test_item_without_number(self):
        items = [{"identifier": "some-random-item", "title": ""}]
        index = build_ia_index(items)
        assert len(index) == 1
        assert index[0]["set_number"] is None

    def test_preserves_metadata(self):
        items = [
            {
                "identifier": "lego-10000",
                "title": "My Set",
                "date": "2020-01-01",
                "publicdate": "2020-06-01",
            }
        ]
        index = build_ia_index(items)
        assert index[0]["date"] == "2020-01-01"
        assert index[0]["publicdate"] == "2020-06-01"
        assert index[0]["title"] == "My Set"


class TestIaScrapeCollection:
    @patch("src.ia.requests.Session")
    def test_single_page(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "items": [{"identifier": "item1"}, {"identifier": "item2"}],
            # No cursor means end of results
        }
        mock_session.get.return_value = mock_resp

        result = ia_scrape_collection(query="test", fields=["identifier"])
        assert len(result) == 2
        assert result[0]["identifier"] == "item1"

    @patch("src.ia.requests.Session")
    def test_pagination(self, mock_session_cls):
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session

        resp1 = MagicMock()
        resp1.json.return_value = {
            "items": [{"identifier": "item1"}],
            "cursor": "abc123",
        }
        resp2 = MagicMock()
        resp2.json.return_value = {
            "items": [{"identifier": "item2"}],
        }
        mock_session.get.side_effect = [resp1, resp2]

        result = ia_scrape_collection(query="test", fields=["identifier"])
        assert len(result) == 2
        assert mock_session.get.call_count == 2


class TestIaFetchItemMetadata:
    @patch("src.ia.requests.get")
    def test_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"files": [], "metadata": {}}
        mock_get.return_value = mock_resp

        result = ia_fetch_item_metadata("test-id")
        assert result == {"files": [], "metadata": {}}
        mock_get.assert_called_once()
