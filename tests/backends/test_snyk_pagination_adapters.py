"""Tests for SnykCursorPaginationAdapter and SnykV1PaginationAdapter."""

from __future__ import annotations

from unittest.mock import MagicMock

from clearskies_snyk.backends.adapters import (
    SnykCursorPaginationAdapter,
    SnykV1PaginationAdapter,
    SnykVersionUrlAdapter,
    extract_v1_records,
)


class TestSnykCursorPaginationAdapter:
    """Unit tests for the Snyk REST API cursor pagination adapter."""

    def setup_method(self):
        self.adapter = SnykCursorPaginationAdapter()

    def _mock_response(self, body: dict) -> MagicMock:
        mock = MagicMock()
        mock.content = b"x"
        mock.json.return_value = body
        return mock

    def test_extracts_cursor_from_links_next(self):
        """starting_after cursor is extracted from links.next URL."""
        response = self._mock_response({"links": {"next": "/rest/orgs?starting_after=abc123&version=2024-10-15"}})
        result = self.adapter.extract_next_page_data(response, MagicMock())
        assert result == {"starting_after": "abc123"}

    def test_returns_empty_when_no_next_link(self):
        """Empty links dict signals no more pages."""
        response = self._mock_response({"links": {}})
        assert self.adapter.extract_next_page_data(response, MagicMock()) == {}

    def test_returns_empty_when_links_key_absent(self):
        """Response without a links key signals no more pages."""
        response = self._mock_response({"data": []})
        assert self.adapter.extract_next_page_data(response, MagicMock()) == {}

    def test_returns_empty_for_empty_content(self):
        """Empty response body returns no next page."""
        mock = MagicMock()
        mock.content = b""
        assert self.adapter.extract_next_page_data(mock, MagicMock()) == {}

    def test_returns_empty_for_non_dict_body(self):
        """Non-dict response body is handled gracefully."""
        response = MagicMock()
        response.content = b"x"
        response.json.return_value = []
        assert self.adapter.extract_next_page_data(response, MagicMock()) == {}

    def test_custom_pagination_parameter_name(self):
        """Custom pagination parameter name is respected."""
        adapter = SnykCursorPaginationAdapter(pagination_parameter_name="cursor")
        response = self._mock_response({"links": {"next": "/api/items?cursor=xyz789&limit=10"}})
        result = adapter.extract_next_page_data(response, MagicMock())
        assert result == {"cursor": "xyz789"}

    def test_returns_empty_when_cursor_param_not_in_next_url(self):
        """Returns empty dict when the configured param isn't in the next URL."""
        response = self._mock_response({"links": {"next": "/rest/orgs?version=2024-10-15"}})
        assert self.adapter.extract_next_page_data(response, MagicMock()) == {}


class TestSnykV1PaginationAdapter:
    """Unit tests for the Snyk v1 page-based pagination adapter."""

    def setup_method(self):
        self.adapter = SnykV1PaginationAdapter()

    def _make_query(self, limit=None, page=None):
        mock = MagicMock()
        mock.limit = limit
        pagination = {}
        if page is not None:
            pagination["page"] = page
        mock.pagination = pagination
        return mock

    def _mock_response(self, body: dict | list) -> MagicMock:
        mock = MagicMock()
        mock.content = b"x"
        mock.json.return_value = body
        return mock

    def test_increments_page_when_full_page_returned(self):
        """Full page (count == limit) increments the page number."""
        query = self._make_query(limit=2)
        response = self._mock_response({"items": [{"id": "1"}, {"id": "2"}]})
        result = self.adapter.extract_next_page_data(response, query)
        assert result == {"page": 2}  # page 1 → page 2

    def test_no_next_page_when_partial_page_returned(self):
        """Partial page (count < limit) signals end of results."""
        query = self._make_query(limit=10)
        response = self._mock_response({"items": [{"id": "1"}]})
        assert self.adapter.extract_next_page_data(response, query) == {}

    def test_increments_from_existing_page(self):
        """Starts increment from the current page in query.pagination."""
        query = self._make_query(limit=2, page=3)
        response = self._mock_response({"items": [{"id": "1"}, {"id": "2"}]})
        result = self.adapter.extract_next_page_data(response, query)
        assert result == {"page": 4}

    def test_empty_response_returns_no_next_page(self):
        """Empty response body returns no next page."""
        mock = MagicMock()
        mock.content = b""
        assert self.adapter.extract_next_page_data(mock, self._make_query()) == {}

    def test_orgs_wrapper_detected_for_pagination(self):
        """Records inside 'orgs' wrapper are counted for pagination guard."""
        query = self._make_query(limit=1)
        response = self._mock_response({"orgs": [{"id": "o1"}]})
        # 1 record == limit=1 → still try next page
        result = self.adapter.extract_next_page_data(response, query)
        assert result == {"page": 2}

    def test_projects_wrapper_partial_page(self):
        """Partial page via 'projects' wrapper stops pagination."""
        query = self._make_query(limit=10)
        response = self._mock_response({"projects": [{"id": "p1"}]})
        assert self.adapter.extract_next_page_data(response, query) == {}

    def test_direct_list_response(self):
        """Direct list responses (not wrapped) are handled correctly."""
        query = self._make_query(limit=2)
        response = self._mock_response([{"id": "1"}, {"id": "2"}])
        result = self.adapter.extract_next_page_data(response, query)
        assert result == {"page": 2}

    def test_generic_single_key_wrapper(self):
        """Generic single-key wrapper is handled."""
        query = self._make_query(limit=2, page=1)
        response = self._mock_response({"custom_data": [{"id": "1"}, {"id": "2"}]})
        result = self.adapter.extract_next_page_data(response, query)
        assert result == {"page": 2}

    def test_extract_v1_records_returns_none_for_non_list_dict(self):
        """Dict without a list value (single record) returns None."""
        assert extract_v1_records({"single_item": {"id": "1"}}) is None


class TestSnykVersionUrlAdapter:
    """Unit tests for SnykVersionUrlAdapter."""

    def setup_method(self):
        self.adapter = SnykVersionUrlAdapter(
            base_url="https://api.snyk.io/rest/",
            api_version="2026-03-25",
        )

    def test_create_url_has_version(self):
        """Create operations get ?version= appended."""
        url, _ = self.adapter.finalize_url("orgs", {}, "create")
        assert "version=2026-03-25" in url

    def test_update_url_has_version(self):
        """Update operations get ?version= appended."""
        url, _ = self.adapter.finalize_url("orgs/org-1", {}, "update")
        assert "version=2026-03-25" in url

    def test_delete_url_has_version(self):
        """Delete operations get ?version= appended."""
        url, _ = self.adapter.finalize_url("orgs/org-1", {}, "delete")
        assert "version=2026-03-25" in url

    def test_records_url_has_no_version(self):
        """Records operations do NOT get version appended (comes from pagination_to_request_parameters)."""
        url, _ = self.adapter.finalize_url("orgs", {}, "records")
        assert "version" not in url

    def test_version_separator_ampersand_when_query_string_present(self):
        """Uses & when URL already has a query string."""
        url, _ = self.adapter.finalize_url("orgs?foo=bar", {}, "create")
        assert "?foo=bar&version=2026-03-25" in url

    def test_custom_api_version(self):
        """Custom api_version is used."""
        adapter = SnykVersionUrlAdapter(api_version="2025-01-01")
        url, _ = adapter.finalize_url("orgs", {}, "create")
        assert "version=2025-01-01" in url
