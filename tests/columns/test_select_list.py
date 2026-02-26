"""Tests for the SelectList column type."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from clearskies_snyk.columns.select_list import SelectList


class TestSelectListFromBackend:
    """Test from_backend conversion."""

    def test_from_backend_with_list(self) -> None:
        """Test conversion from list of strings."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        result = column.from_backend(["critical", "high"])

        assert result == ["critical", "high"]

    def test_from_backend_with_empty_list(self) -> None:
        """Test conversion from empty list."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        result = column.from_backend([])

        assert result == []

    def test_from_backend_with_none(self) -> None:
        """Test conversion from None."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        result = column.from_backend(None)

        assert result == []

    def test_from_backend_with_single_string(self) -> None:
        """Test conversion from single string (wraps in list)."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        result = column.from_backend("critical")

        assert result == ["critical"]


class TestSelectListToBackend:
    """Test to_backend conversion."""

    def test_to_backend_with_list(self) -> None:
        """Test conversion to backend with list."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        data = {"business_criticality": ["critical", "high"]}
        result = column.to_backend(data)

        assert result["business_criticality"] == ["critical", "high"]

    def test_to_backend_with_single_string(self) -> None:
        """Test conversion to backend with single string (wraps in list)."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        data = {"business_criticality": "critical"}
        result = column.to_backend(data)

        assert result["business_criticality"] == ["critical"]

    def test_to_backend_with_none(self) -> None:
        """Test conversion to backend with None (returns empty list)."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        data = {"business_criticality": None}
        result = column.to_backend(data)

        assert result["business_criticality"] == []

    def test_to_backend_without_column(self) -> None:
        """Test conversion to backend when column not in data."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        data = {"other_field": "value"}
        result = column.to_backend(data)

        assert "business_criticality" not in result
        assert result["other_field"] == "value"


class TestSelectListInputErrors:
    """Test input validation."""

    def test_input_errors_with_valid_values(self) -> None:
        """Test validation with valid values."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": ["critical", "high"]}

        errors = column.input_errors(model, data)

        assert errors == {}

    def test_input_errors_with_invalid_value(self) -> None:
        """Test validation with invalid value."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": ["critical", "invalid"]}

        errors = column.input_errors(model, data)

        assert "business_criticality" in errors
        assert "invalid" in errors["business_criticality"]

    def test_input_errors_with_none(self) -> None:
        """Test validation with None value."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": None}

        errors = column.input_errors(model, data)

        assert errors == {}

    def test_input_errors_with_missing_column(self) -> None:
        """Test validation when column not in data."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"other_field": "value"}

        errors = column.input_errors(model, data)

        assert errors == {}

    def test_input_errors_with_single_string(self) -> None:
        """Test validation with single string (valid)."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": "critical"}

        errors = column.input_errors(model, data)

        assert errors == {}

    def test_input_errors_with_invalid_single_string(self) -> None:
        """Test validation with invalid single string."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": "invalid"}

        errors = column.input_errors(model, data)

        assert "business_criticality" in errors
        assert "invalid" in errors["business_criticality"]

    def test_input_errors_with_non_list_non_string(self) -> None:
        """Test validation with non-list, non-string value."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": 123}

        errors = column.input_errors(model, data)

        assert "business_criticality" in errors
        assert "must be a list" in errors["business_criticality"]

    def test_input_errors_without_allowed_values(self) -> None:
        """Test validation without allowed_values (no validation)."""
        column = SelectList()
        column.name = "business_criticality"

        model = Mock()
        data = {"business_criticality": ["anything", "goes"]}

        errors = column.input_errors(model, data)

        assert errors == {}


class TestSelectListProperties:
    """Test column properties."""

    def test_allowed_values_property(self) -> None:
        """Test allowed_values property returns the list."""
        column = SelectList(allowed_values=["critical", "high", "medium", "low"])

        assert column.allowed_values == ["critical", "high", "medium", "low"]

    def test_allowed_values_property_empty(self) -> None:
        """Test allowed_values property with no values."""
        column = SelectList()

        assert column.allowed_values == []


class TestSelectListIntegration:
    """Integration tests for SelectList with Snyk API format."""

    def test_snyk_business_criticality_format(self) -> None:
        """Test that business_criticality is serialized correctly for Snyk API."""
        column = SelectList(
            allowed_values=["critical", "high", "medium", "low"],
        )
        column.name = "business_criticality"

        # Simulate what the API expects
        data = {"business_criticality": ["critical"]}
        result = column.to_backend(data)

        # Snyk API expects: {"business_criticality": ["critical"]}
        assert result["business_criticality"] == ["critical"]
        assert isinstance(result["business_criticality"], list)

    def test_snyk_environment_format(self) -> None:
        """Test that environment is serialized correctly for Snyk API."""
        column = SelectList(
            allowed_values=[
                "frontend",
                "backend",
                "internal",
                "external",
                "mobile",
                "saas",
                "onprem",
                "hosted",
                "distributed",
            ],
        )
        column.name = "environment"

        # Simulate what the API expects
        data = {"environment": ["external", "hosted"]}
        result = column.to_backend(data)

        # Snyk API expects: {"environment": ["external", "hosted"]}
        assert result["environment"] == ["external", "hosted"]
        assert isinstance(result["environment"], list)

    def test_snyk_lifecycle_format(self) -> None:
        """Test that lifecycle is serialized correctly for Snyk API."""
        column = SelectList(
            allowed_values=["production", "development", "sandbox"],
        )
        column.name = "lifecycle"

        # Simulate what the API expects
        data = {"lifecycle": ["production"]}
        result = column.to_backend(data)

        # Snyk API expects: {"lifecycle": ["production"]}
        assert result["lifecycle"] == ["production"]
        assert isinstance(result["lifecycle"], list)
