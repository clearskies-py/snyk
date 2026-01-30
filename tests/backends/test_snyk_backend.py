"""Tests for the Snyk backend."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from clearskies_snyk.backends import SnykBackend


class TestSnykBackend(unittest.TestCase):
    """Tests for SnykBackend."""

    def test_backend_initialization(self) -> None:
        """Test that the backend initializes with correct defaults."""
        backend = SnykBackend()
        assert backend.base_url == "https://api.snyk.io/rest/"
        assert backend.api_version == "2025-11-05"
        assert backend.api_casing == "snake_case"
        assert backend.pagination_parameter_name == "starting_after"
        assert backend.limit_parameter_name == "limit"

    def test_backend_custom_initialization(self) -> None:
        """Test that the backend can be initialized with custom values."""
        backend = SnykBackend(
            base_url="https://custom.snyk.io/rest/",
            api_version="2025-01-01",
        )
        assert backend.base_url == "https://custom.snyk.io/rest/"
        assert backend.api_version == "2025-01-01"

    def test_headers_config(self) -> None:
        """Test that headers include the correct Accept header."""
        backend = SnykBackend()
        assert backend.headers["Accept"] == "application/vnd.api+json"

    def test_map_records_response_list(self) -> None:
        """Test mapping of list response data."""
        backend = SnykBackend()
        mock_query = MagicMock()

        response_data = {
            "data": [
                {
                    "id": "org-123",
                    "type": "org",
                    "attributes": {
                        "name": "Test Org",
                        "slug": "test-org",
                    },
                },
                {
                    "id": "org-456",
                    "type": "org",
                    "attributes": {
                        "name": "Another Org",
                        "slug": "another-org",
                    },
                },
            ],
        }

        result = backend.map_records_response(response_data, mock_query)

        assert len(result) == 2
        assert result[0]["id"] == "org-123"
        assert result[0]["name"] == "Test Org"
        assert result[0]["slug"] == "test-org"
        assert result[1]["id"] == "org-456"
        assert result[1]["name"] == "Another Org"

    def test_map_records_response_with_relationships(self) -> None:
        """Test mapping of response data with relationships."""
        backend = SnykBackend()
        mock_query = MagicMock()

        response_data = {
            "data": [
                {
                    "id": "project-123",
                    "type": "project",
                    "attributes": {
                        "name": "Test Project",
                    },
                    "relationships": {
                        "organization": {
                            "data": {
                                "id": "org-456",
                                "type": "org",
                            }
                        }
                    },
                },
            ],
        }

        result = backend.map_records_response(response_data, mock_query)

        assert len(result) == 1
        assert result[0]["id"] == "project-123"
        assert result[0]["name"] == "Test Project"
        # organization is mapped to org_id
        assert result[0]["org_id"] == "org-456"

    def test_get_next_page_data_from_response(self) -> None:
        """Test extraction of pagination data from response."""
        backend = SnykBackend()
        mock_query = MagicMock()
        mock_response = MagicMock()
        mock_response.content = b'{"links": {"next": "/rest/orgs?starting_after=abc123&version=2024-10-15"}}'
        mock_response.json.return_value = {
            "links": {
                "next": "/rest/orgs?starting_after=abc123&version=2024-10-15"
            }
        }

        result = backend.get_next_page_data_from_response(mock_query, mock_response)

        assert result["starting_after"] == "abc123"

    def test_get_next_page_data_no_next_page(self) -> None:
        """Test extraction of pagination data when there's no next page."""
        backend = SnykBackend()
        mock_query = MagicMock()
        mock_response = MagicMock()
        mock_response.content = b'{"links": {}}'
        mock_response.json.return_value = {"links": {}}

        result = backend.get_next_page_data_from_response(mock_query, mock_response)

        assert "starting_after" not in result

    def test_pagination_to_request_parameters_adds_version(self) -> None:
        """Test that pagination_to_request_parameters adds the version parameter."""
        backend = SnykBackend()
        mock_query = MagicMock()
        mock_query.pagination_data = {}
        mock_query.limit = None
        mock_query.offset = None

        url_params, body_params = backend.pagination_to_request_parameters(mock_query)

        assert "version" in url_params
        assert url_params["version"] == "2025-11-05"

    def test_flatten_json_api_record_with_non_dict(self) -> None:
        """Test _flatten_json_api_record returns non-dict values unchanged."""
        backend = SnykBackend()

        # When record is not a dict, it should be returned as-is
        result = backend._flatten_json_api_record("not a dict")
        assert result == "not a dict"

        result = backend._flatten_json_api_record(123)
        assert result == 123

        result = backend._flatten_json_api_record(None)
        assert result is None


if __name__ == "__main__":
    unittest.main()
