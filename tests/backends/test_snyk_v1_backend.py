"""Tests for SnykV1Backend."""

import json
from unittest.mock import MagicMock, patch

import clearskies
import pytest

from clearskies_snyk.backends import SnykV1Backend


class TestSnykV1Backend:
    """Tests for the SnykV1Backend class."""

    def test_default_base_url(self):
        """Test that the default base URL is set correctly."""
        backend = SnykV1Backend()
        assert backend.base_url == "https://api.snyk.io/v1/"

    def test_default_api_casing(self):
        """Test that the default API casing is camelCase."""
        backend = SnykV1Backend()
        assert backend.api_casing == "camelCase"

    def test_default_pagination_parameters(self):
        """Test that the default pagination parameters are set correctly."""
        backend = SnykV1Backend()
        assert backend.pagination_parameter_name == "page"
        assert backend.limit_parameter_name == "perPage"

    def test_headers_config(self):
        """Test that headers include Content-Type."""
        backend = SnykV1Backend()
        assert backend.headers["Content-Type"] == "application/json"

    def test_map_records_response_with_orgs_wrapper(self):
        """Test mapping response with orgs wrapper."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "orgs"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {
            "orgs": [
                {"id": "org-1", "name": "Org One"},
                {"id": "org-2", "name": "Org Two"},
            ]
        }

        records = backend.map_records_response(response_data, query)
        assert len(records) == 2
        assert records[0]["id"] == "org-1"
        assert records[1]["name"] == "Org Two"

    def test_map_records_response_with_projects_wrapper(self):
        """Test mapping response with projects wrapper."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "projects"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {
            "projects": [
                {"id": "proj-1", "name": "Project One"},
            ]
        }

        records = backend.map_records_response(response_data, query)
        assert len(records) == 1
        assert records[0]["id"] == "proj-1"

    def test_map_records_response_with_single_record(self):
        """Test mapping response with a single record."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "org"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {"id": "org-1", "name": "Org One"}

        records = backend.map_records_response(response_data, query)
        assert len(records) == 1
        assert records[0]["id"] == "org-1"

    def test_map_records_response_with_list(self):
        """Test mapping response that is already a list."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "items"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = [
            {"id": "item-1", "name": "Item One"},
            {"id": "item-2", "name": "Item Two"},
        ]

        records = backend.map_records_response(response_data, query)
        assert len(records) == 2

    def test_custom_base_url(self):
        """Test that a custom base URL can be set."""
        backend = SnykV1Backend(base_url="https://custom.snyk.io/v1/")
        assert backend.base_url == "https://custom.snyk.io/v1/"

    def test_map_records_response_with_generic_wrapper(self):
        """Test mapping response with a generic single-key wrapper."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()
            name = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "custom"

        query = clearskies.query.Query(model_class=MockModel)
        response_data = {
            "custom_items": [
                {"id": "item-1", "name": "Item One"},
                {"id": "item-2", "name": "Item Two"},
            ]
        }

        records = backend.map_records_response(response_data, query)
        assert len(records) == 2
        assert records[0]["id"] == "item-1"

    def test_get_next_page_data_with_full_page(self):
        """Test pagination when response has a full page of results."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "items"

        query = clearskies.query.Query(model_class=MockModel).set_limit(2)

        mock_response = MagicMock()
        mock_response.content = b'{"items": [{"id": "1"}, {"id": "2"}]}'
        mock_response.json.return_value = {
            "items": [{"id": "1"}, {"id": "2"}]
        }

        result = backend.get_next_page_data_from_response(query, mock_response)
        assert result.get("page") == 2  # Should request page 2

    def test_get_next_page_data_with_partial_page(self):
        """Test pagination when response has fewer results than limit."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "items"

        query = clearskies.query.Query(model_class=MockModel).set_limit(10)

        mock_response = MagicMock()
        mock_response.content = b'{"items": [{"id": "1"}]}'
        mock_response.json.return_value = {
            "items": [{"id": "1"}]  # Only 1 result, less than limit
        }

        result = backend.get_next_page_data_from_response(query, mock_response)
        assert "page" not in result  # Should not have next page

    def test_get_next_page_data_with_empty_response(self):
        """Test pagination with empty response."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "items"

        query = clearskies.query.Query(model_class=MockModel)

        mock_response = MagicMock()
        mock_response.content = b'{}'
        mock_response.json.return_value = {}

        result = backend.get_next_page_data_from_response(query, mock_response)
        assert "page" not in result

    def test_get_next_page_data_with_existing_page(self):
        """Test pagination when already on a specific page."""
        backend = SnykV1Backend()

        class MockModel(clearskies.Model):
            id_column_name = "id"
            id = clearskies.columns.String()

            @classmethod
            def destination_name(cls):
                return "items"

        query = clearskies.query.Query(model_class=MockModel).set_limit(2).set_pagination({"page": 3})

        mock_response = MagicMock()
        mock_response.content = b'{"items": [{"id": "1"}, {"id": "2"}]}'
        mock_response.json.return_value = {
            "items": [{"id": "1"}, {"id": "2"}]
        }

        result = backend.get_next_page_data_from_response(query, mock_response)
        assert result.get("page") == 4  # Should request page 4

    def test_extract_records_from_response_with_list(self):
        """Test _extract_records_from_response with direct list."""
        backend = SnykV1Backend()
        records = backend._extract_records_from_response([{"id": "1"}, {"id": "2"}])
        assert len(records) == 2

    def test_extract_records_from_response_with_wrapper(self):
        """Test _extract_records_from_response with wrapper key."""
        backend = SnykV1Backend()
        records = backend._extract_records_from_response({
            "projects": [{"id": "1"}, {"id": "2"}]
        })
        assert len(records) == 2

    def test_extract_records_from_response_with_generic_wrapper(self):
        """Test _extract_records_from_response with generic single-key wrapper."""
        backend = SnykV1Backend()
        records = backend._extract_records_from_response({
            "custom_data": [{"id": "1"}]
        })
        assert len(records) == 1

    def test_extract_records_from_response_with_empty_dict(self):
        """Test _extract_records_from_response with empty dict."""
        backend = SnykV1Backend()
        records = backend._extract_records_from_response({})
        assert len(records) == 0

    def test_extract_records_from_response_with_non_list_value(self):
        """Test _extract_records_from_response with non-list value."""
        backend = SnykV1Backend()
        records = backend._extract_records_from_response({
            "single_item": {"id": "1"}
        })
        assert len(records) == 0  # Non-list values return empty
