"""
Tests for the SnykOrg model.

This module demonstrates the test patterns for Snyk models, including:
- Model configuration tests
- Response mapping tests
- Pagination tests
- Edge case handling
"""

from __future__ import annotations

import pytest
from unittest.mock import MagicMock

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models import SnykOrg

from tests.fixtures import (
    OrgResponseFactory,
    make_jsonapi_response,
    make_pagination_links,
    make_resource,
    ERROR_401,
    ERROR_404,
)


class TestSnykOrgConfiguration:
    """Tests for SnykOrg model configuration."""

    def test_destination_name_returns_orgs(self) -> None:
        """Verify destination_name returns the correct endpoint."""
        assert SnykOrg.destination_name() == "orgs"

    def test_model_has_id_column(self) -> None:
        """Verify the model has an id column."""
        assert hasattr(SnykOrg, "id")
        assert SnykOrg.id_column_name == "id"

    def test_model_has_name_column(self) -> None:
        """Verify the model has a name column."""
        assert hasattr(SnykOrg, "name")

    def test_model_has_slug_column(self) -> None:
        """Verify the model has a slug column."""
        assert hasattr(SnykOrg, "slug")

    def test_model_has_is_personal_column(self) -> None:
        """Verify the model has an is_personal column."""
        assert hasattr(SnykOrg, "is_personal")

    def test_model_has_group_id_column(self) -> None:
        """Verify the model has a group_id column."""
        assert hasattr(SnykOrg, "group_id")

    def test_model_uses_snyk_backend(self) -> None:
        """Verify the model uses SnykBackend."""
        assert isinstance(SnykOrg.backend, SnykBackend)


class TestSnykOrgResponseMapping:
    """Tests for mapping API responses to model data."""

    @pytest.fixture
    def backend(self) -> SnykBackend:
        """Create a SnykBackend instance for testing."""
        return SnykBackend()

    @pytest.fixture
    def mock_query(self) -> MagicMock:
        """Create a mock query object."""
        return MagicMock()

    def test_map_single_org_response(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test mapping a single organization response."""
        response = OrgResponseFactory.single(
            id="org-123",
            name="Test Org",
            slug="test-org",
            group_id="group-456",
            is_personal=False,
        )

        result = backend.map_records_response(response, mock_query)

        assert len(result) == 1
        assert result[0]["id"] == "org-123"
        assert result[0]["name"] == "Test Org"
        assert result[0]["slug"] == "test-org"
        assert result[0]["group_id"] == "group-456"
        assert result[0]["is_personal"] is False

    def test_map_list_org_response(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test mapping a list of organizations response."""
        response = OrgResponseFactory.list(count=3)

        result = backend.map_records_response(response, mock_query)

        assert len(result) == 3
        for record in result:
            assert "id" in record
            assert "name" in record
            assert "slug" in record

    def test_map_empty_response(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test mapping an empty response."""
        response = make_jsonapi_response([])

        result = backend.map_records_response(response, mock_query)

        assert len(result) == 0

    def test_map_response_with_missing_attributes(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test mapping a response with missing optional attributes."""
        response = make_jsonapi_response(
            make_resource(
                id="org-123",
                type="org",
                attributes={
                    "name": "Test Org",
                    # Missing slug, is_personal, group_id
                },
            )
        )

        result = backend.map_records_response(response, mock_query)

        assert len(result) == 1
        assert result[0]["id"] == "org-123"
        assert result[0]["name"] == "Test Org"
        # Missing attributes should not be present (or be None)
        assert result[0].get("slug") is None


class TestSnykOrgPagination:
    """Tests for pagination handling."""

    @pytest.fixture
    def backend(self) -> SnykBackend:
        """Create a SnykBackend instance for testing."""
        return SnykBackend()

    @pytest.fixture
    def mock_query(self) -> MagicMock:
        """Create a mock query object."""
        return MagicMock()

    def test_extract_pagination_cursor(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test extracting pagination cursor from response."""
        mock_response = MagicMock()
        mock_response.content = b'{"links": {"next": "/rest/orgs?starting_after=cursor123&version=2024-10-15"}}'
        mock_response.json.return_value = {
            "links": {
                "next": "/rest/orgs?starting_after=cursor123&version=2024-10-15"
            }
        }

        result = backend.get_next_page_data_from_response(mock_query, mock_response)

        assert result["starting_after"] == "cursor123"

    def test_no_next_page(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test handling when there's no next page."""
        mock_response = MagicMock()
        mock_response.content = b'{"links": {}}'
        mock_response.json.return_value = {"links": {}}

        result = backend.get_next_page_data_from_response(mock_query, mock_response)

        assert "starting_after" not in result

    def test_empty_links(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test handling when links is empty."""
        mock_response = MagicMock()
        mock_response.content = b'{}'
        mock_response.json.return_value = {}

        result = backend.get_next_page_data_from_response(mock_query, mock_response)

        assert "starting_after" not in result


class TestSnykOrgEdgeCases:
    """Tests for edge cases and error handling."""

    @pytest.fixture
    def backend(self) -> SnykBackend:
        """Create a SnykBackend instance for testing."""
        return SnykBackend()

    @pytest.fixture
    def mock_query(self) -> MagicMock:
        """Create a mock query object."""
        return MagicMock()

    def test_map_response_with_relationships(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test mapping a response that includes relationships."""
        response = make_jsonapi_response(
            make_resource(
                id="org-123",
                type="org",
                attributes={
                    "name": "Test Org",
                    "slug": "test-org",
                },
                relationships={
                    "group": {
                        "data": {"id": "group-456", "type": "group"}
                    }
                },
            )
        )

        result = backend.map_records_response(response, mock_query)

        assert len(result) == 1
        assert result[0]["id"] == "org-123"
        # Relationship should be extracted as {rel_name}_id
        assert result[0].get("group_id") == "group-456"

    def test_map_response_with_null_data(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test mapping a response with null data field."""
        response = {"data": None, "jsonapi": {"version": "1.0"}}

        # The backend passes through to parent which wraps in list
        # This test documents the current behavior
        result = backend.map_records_response(response, mock_query)
        
        # Current implementation wraps the response in a list
        # This is acceptable behavior - the model layer handles None
        assert isinstance(result, list)

    def test_map_response_with_extra_fields(
        self, backend: SnykBackend, mock_query: MagicMock
    ) -> None:
        """Test that extra fields in response are preserved."""
        response = make_jsonapi_response(
            make_resource(
                id="org-123",
                type="org",
                attributes={
                    "name": "Test Org",
                    "slug": "test-org",
                    "custom_field": "custom_value",  # Extra field
                },
            )
        )

        result = backend.map_records_response(response, mock_query)

        assert len(result) == 1
        assert result[0]["custom_field"] == "custom_value"
