"""
Tests for the SnykGroupMembership model.

This module tests the SnykGroupMembership model including:
- Model configuration
- Helper methods (get_membership_count, email, name, username properties)
- Edge cases for missing/malformed data
"""

from __future__ import annotations

from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models import SnykGroupMembership


class TestSnykGroupMembershipConfiguration:
    """Tests for SnykGroupMembership model configuration."""

    def test_destination_name_returns_correct_endpoint(self) -> None:
        """Verify destination_name returns the correct endpoint."""
        assert SnykGroupMembership.destination_name() == "groups/{group_id}/memberships"

    def test_model_has_id_column(self) -> None:
        """Verify the model has an id column."""
        assert hasattr(SnykGroupMembership, "id")
        assert SnykGroupMembership.id_column_name == "id"

    def test_model_has_group_id_column(self) -> None:
        """Verify the model has a group_id column."""
        assert hasattr(SnykGroupMembership, "group_id")

    def test_model_has_user_column(self) -> None:
        """Verify the model has a user column."""
        assert hasattr(SnykGroupMembership, "user")

    def test_model_has_role_column(self) -> None:
        """Verify the model has a role column."""
        assert hasattr(SnykGroupMembership, "role")

    def test_model_uses_snyk_backend(self) -> None:
        """Verify the model uses SnykBackend."""
        assert isinstance(SnykGroupMembership.backend, SnykBackend)

    def test_backend_has_type_mapping(self) -> None:
        """Verify the backend maps 'type' to 'membership_type'."""
        assert SnykGroupMembership.backend.api_to_model_map.get("type") == "membership_type"


class TestSnykGroupMembershipHelperMethods:
    """Tests for SnykGroupMembership helper methods using mocks."""

    def test_get_membership_count_with_valid_data(self) -> None:
        """Test get_membership_count returns correct count."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.meta = {"group_membership_count": 5}
        # Call the actual method
        result = SnykGroupMembership.get_membership_count(membership)
        assert result == 5

    def test_get_membership_count_with_empty_meta(self) -> None:
        """Test get_membership_count returns 0 when meta is empty."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.meta = {}
        result = SnykGroupMembership.get_membership_count(membership)
        assert result == 0

    def test_get_membership_count_with_none_meta(self) -> None:
        """Test get_membership_count returns 0 when meta is None."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.meta = None
        result = SnykGroupMembership.get_membership_count(membership)
        assert result == 0

    def test_email_property_with_valid_data(self) -> None:
        """Test email property returns correct email."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {"email": "test@example.com", "name": "Test User"}
        # Access the property through the class
        result = SnykGroupMembership.email.fget(membership)  # type: ignore[attr-defined]
        assert result == "test@example.com"

    def test_email_property_with_empty_user(self) -> None:
        """Test email property returns empty string when user is empty."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {}
        result = SnykGroupMembership.email.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_email_property_with_none_user(self) -> None:
        """Test email property returns empty string when user is None."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = None
        result = SnykGroupMembership.email.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_name_property_with_valid_data(self) -> None:
        """Test name property returns correct name."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {"name": "Test User", "email": "test@example.com"}
        result = SnykGroupMembership.name.fget(membership)  # type: ignore[attr-defined]
        assert result == "Test User"

    def test_name_property_with_empty_user(self) -> None:
        """Test name property returns empty string when user is empty."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {}
        result = SnykGroupMembership.name.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_name_property_with_none_user(self) -> None:
        """Test name property returns empty string when user is None."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = None
        result = SnykGroupMembership.name.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_username_property_with_valid_data(self) -> None:
        """Test username property returns correct username."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {"username": "testuser", "email": "test@example.com"}
        result = SnykGroupMembership.username.fget(membership)  # type: ignore[attr-defined]
        assert result == "testuser"

    def test_username_property_with_empty_user(self) -> None:
        """Test username property returns empty string when user is empty."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {}
        result = SnykGroupMembership.username.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_username_property_with_none_user(self) -> None:
        """Test username property returns empty string when user is None."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = None
        result = SnykGroupMembership.username.fget(membership)  # type: ignore[attr-defined]
        assert result == ""


class TestSnykGroupMembershipEdgeCases:
    """Tests for edge cases in SnykGroupMembership."""

    def test_get_membership_count_with_string_value(self) -> None:
        """Test get_membership_count handles string values."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.meta = {"group_membership_count": "10"}
        result = SnykGroupMembership.get_membership_count(membership)
        assert result == 10

    def test_get_membership_count_with_invalid_value(self) -> None:
        """Test get_membership_count handles invalid values."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.meta = {"group_membership_count": "invalid"}
        # Should return 0 due to ValueError in int conversion
        result = SnykGroupMembership.get_membership_count(membership)
        assert result == 0

    def test_email_property_with_missing_key(self) -> None:
        """Test email property handles missing email key."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {"name": "Test User"}  # No email key
        result = SnykGroupMembership.email.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_name_property_with_missing_key(self) -> None:
        """Test name property handles missing name key."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {"email": "test@example.com"}  # No name key
        result = SnykGroupMembership.name.fget(membership)  # type: ignore[attr-defined]
        assert result == ""

    def test_username_property_with_missing_key(self) -> None:
        """Test username property handles missing username key."""
        membership = MagicMock(spec=SnykGroupMembership)
        membership.user = {"email": "test@example.com"}  # No username key
        result = SnykGroupMembership.username.fget(membership)  # type: ignore[attr-defined]
        assert result == ""
