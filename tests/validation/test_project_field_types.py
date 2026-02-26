"""
Comprehensive field type validation tests for Snyk models.

This module validates that model field types match the OpenAPI specification,
ensuring that array fields are properly typed as arrays, strings as strings, etc.

This test would have caught the bug where business_criticality, environment,
and lifecycle were defined as Select (string) columns instead of SelectList (array).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from clearskies.columns import Boolean, Datetime, Integer, Json, Select, String

from clearskies_snyk.columns import ProjectTagList, SelectList
from clearskies_snyk.models import SnykProject


def load_spec() -> dict[str, Any]:
    """Load the API specification."""
    spec_path = Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"
    if not spec_path.exists():
        pytest.skip(f"API spec not found at {spec_path}")
    with open(spec_path) as f:
        return json.load(f)


def load_projects_spec() -> dict[str, Any]:
    """Load the decomposed projects spec for detailed schema info."""
    spec_path = Path(__file__).parent.parent.parent / "api_spec" / "decomposed" / "chunks" / "domain_projects.json"
    if not spec_path.exists():
        pytest.skip(f"Projects spec not found at {spec_path}")
    with open(spec_path) as f:
        return json.load(f)


def get_schema_type(schema: dict[str, Any]) -> str:
    """Extract the type from a JSON schema."""
    if "type" in schema:
        return schema["type"]
    if "oneOf" in schema or "anyOf" in schema:
        return "union"
    if "$ref" in schema:
        return "ref"
    return "unknown"


def get_schema_items_type(schema: dict[str, Any]) -> str | None:
    """Extract the items type from an array schema."""
    if schema.get("type") == "array" and "items" in schema:
        items = schema["items"]
        if "type" in items:
            return items["type"]
        if "enum" in items:
            return "enum"
    return None


class TestProjectFieldTypesMatchSpec:
    """Test that SnykProject field types match the OpenAPI specification."""

    @pytest.fixture
    def projects_spec(self) -> dict[str, Any]:
        return load_projects_spec()

    @pytest.fixture
    def project_attributes_schema(self, projects_spec: dict[str, Any]) -> dict[str, Any]:
        """Extract the ProjectAttributes schema from the spec."""
        return projects_spec.get("schemas", {}).get("ProjectAttributes", {})

    @pytest.fixture
    def patch_request_schema(self, projects_spec: dict[str, Any]) -> dict[str, Any]:
        """Extract the PatchProjectRequest schema from the spec."""
        return projects_spec.get("schemas", {}).get("PatchProjectRequest", {})

    def test_business_criticality_is_array_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify business_criticality is defined as array in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        bc_schema = properties.get("business_criticality", {})

        assert bc_schema.get("type") == "array", (
            f"Spec defines business_criticality as '{bc_schema.get('type')}', expected 'array'"
        )

        # Check model column type
        column = getattr(SnykProject, "business_criticality", None)
        assert column is not None, "SnykProject missing business_criticality column"
        assert isinstance(column, SelectList), (
            f"SnykProject.business_criticality should be SelectList, got {type(column).__name__}"
        )

    def test_environment_is_array_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify environment is defined as array in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        env_schema = properties.get("environment", {})

        assert env_schema.get("type") == "array", (
            f"Spec defines environment as '{env_schema.get('type')}', expected 'array'"
        )

        # Check model column type
        column = getattr(SnykProject, "environment", None)
        assert column is not None, "SnykProject missing environment column"
        assert isinstance(column, SelectList), (
            f"SnykProject.environment should be SelectList, got {type(column).__name__}"
        )

    def test_lifecycle_is_array_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify lifecycle is defined as array in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        lifecycle_schema = properties.get("lifecycle", {})

        assert lifecycle_schema.get("type") == "array", (
            f"Spec defines lifecycle as '{lifecycle_schema.get('type')}', expected 'array'"
        )

        # Check model column type
        column = getattr(SnykProject, "lifecycle", None)
        assert column is not None, "SnykProject missing lifecycle column"
        assert isinstance(column, SelectList), (
            f"SnykProject.lifecycle should be SelectList, got {type(column).__name__}"
        )

    def test_status_is_string_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify status is defined as string (enum) in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        status_schema = properties.get("status", {})

        assert status_schema.get("type") == "string", (
            f"Spec defines status as '{status_schema.get('type')}', expected 'string'"
        )

        # Check model column type - should be Select (single value enum)
        column = getattr(SnykProject, "status", None)
        assert column is not None, "SnykProject missing status column"
        assert isinstance(column, Select), f"SnykProject.status should be Select, got {type(column).__name__}"

    def test_tags_is_array_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify tags is defined as array in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        tags_schema = properties.get("tags", {})

        assert tags_schema.get("type") == "array", f"Spec defines tags as '{tags_schema.get('type')}', expected 'array'"

        # Check model column type
        column = getattr(SnykProject, "tags", None)
        assert column is not None, "SnykProject missing tags column"
        assert isinstance(column, ProjectTagList), (
            f"SnykProject.tags should be ProjectTagList, got {type(column).__name__}"
        )

    def test_name_is_string_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify name is defined as string in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        name_schema = properties.get("name", {})

        assert name_schema.get("type") == "string", (
            f"Spec defines name as '{name_schema.get('type')}', expected 'string'"
        )

        # Check model column type
        column = getattr(SnykProject, "name", None)
        assert column is not None, "SnykProject missing name column"
        assert isinstance(column, String), f"SnykProject.name should be String, got {type(column).__name__}"

    def test_read_only_is_boolean_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify read_only is defined as boolean in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        read_only_schema = properties.get("read_only", {})

        assert read_only_schema.get("type") == "boolean", (
            f"Spec defines read_only as '{read_only_schema.get('type')}', expected 'boolean'"
        )

        # Check model column type
        column = getattr(SnykProject, "read_only", None)
        assert column is not None, "SnykProject missing read_only column"
        assert isinstance(column, Boolean), f"SnykProject.read_only should be Boolean, got {type(column).__name__}"

    def test_created_is_datetime_type(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify created is defined as date-time in spec and model."""
        # Check spec
        properties = project_attributes_schema.get("properties", {})
        created_schema = properties.get("created", {})

        assert created_schema.get("type") == "string", (
            f"Spec defines created as '{created_schema.get('type')}', expected 'string'"
        )
        assert created_schema.get("format") == "date-time", (
            f"Spec defines created format as '{created_schema.get('format')}', expected 'date-time'"
        )

        # Check model column type
        column = getattr(SnykProject, "created", None)
        assert column is not None, "SnykProject missing created column"
        assert isinstance(column, Datetime), f"SnykProject.created should be Datetime, got {type(column).__name__}"


class TestProjectAllowedValuesMatchSpec:
    """Test that SnykProject enum allowed values match the OpenAPI specification."""

    @pytest.fixture
    def projects_spec(self) -> dict[str, Any]:
        return load_projects_spec()

    @pytest.fixture
    def project_attributes_schema(self, projects_spec: dict[str, Any]) -> dict[str, Any]:
        """Extract the ProjectAttributes schema from the spec."""
        return projects_spec.get("schemas", {}).get("ProjectAttributes", {})

    def test_business_criticality_allowed_values(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify business_criticality allowed values match spec."""
        properties = project_attributes_schema.get("properties", {})
        bc_schema = properties.get("business_criticality", {})
        items = bc_schema.get("items", {})
        spec_values = set(items.get("enum", []))

        column = getattr(SnykProject, "business_criticality", None)
        model_values = set(column.allowed_values) if column else set()

        assert spec_values == model_values, (
            f"business_criticality allowed values mismatch.\nSpec: {sorted(spec_values)}\nModel: {sorted(model_values)}"
        )

    def test_environment_allowed_values(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify environment allowed values match spec."""
        properties = project_attributes_schema.get("properties", {})
        env_schema = properties.get("environment", {})
        items = env_schema.get("items", {})
        spec_values = set(items.get("enum", []))

        column = getattr(SnykProject, "environment", None)
        model_values = set(column.allowed_values) if column else set()

        assert spec_values == model_values, (
            f"environment allowed values mismatch.\nSpec: {sorted(spec_values)}\nModel: {sorted(model_values)}"
        )

    def test_lifecycle_allowed_values(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify lifecycle allowed values match spec."""
        properties = project_attributes_schema.get("properties", {})
        lifecycle_schema = properties.get("lifecycle", {})
        items = lifecycle_schema.get("items", {})
        spec_values = set(items.get("enum", []))

        column = getattr(SnykProject, "lifecycle", None)
        model_values = set(column.allowed_values) if column else set()

        assert spec_values == model_values, (
            f"lifecycle allowed values mismatch.\nSpec: {sorted(spec_values)}\nModel: {sorted(model_values)}"
        )

    def test_status_allowed_values(self, project_attributes_schema: dict[str, Any]) -> None:
        """Verify status allowed values match spec."""
        properties = project_attributes_schema.get("properties", {})
        status_schema = properties.get("status", {})
        spec_values = set(status_schema.get("enum", []))

        column = getattr(SnykProject, "status", None)
        model_values = set(column.allowed_values) if column else set()

        assert spec_values == model_values, (
            f"status allowed values mismatch.\nSpec: {sorted(spec_values)}\nModel: {sorted(model_values)}"
        )


class TestSelectListSerializationFormat:
    """Test that SelectList columns serialize correctly for the Snyk API."""

    def test_business_criticality_serializes_as_array(self) -> None:
        """Verify business_criticality serializes as array for API."""
        column = getattr(SnykProject, "business_criticality", None)
        assert column is not None, "business_criticality column not found"
        column.name = "business_criticality"

        # Test single value input
        data: dict[str, Any] = {"business_criticality": "critical"}
        result = column.to_backend(data)
        assert isinstance(result["business_criticality"], list), "Should serialize as list"
        assert result["business_criticality"] == ["critical"]

        # Test list input
        data = {"business_criticality": ["critical", "high"]}
        result = column.to_backend(data)
        assert isinstance(result["business_criticality"], list), "Should serialize as list"
        assert result["business_criticality"] == ["critical", "high"]

    def test_environment_serializes_as_array(self) -> None:
        """Verify environment serializes as array for API."""
        column = getattr(SnykProject, "environment", None)
        assert column is not None, "environment column not found"
        column.name = "environment"

        # Test single value input
        data: dict[str, Any] = {"environment": "production"}
        result = column.to_backend(data)
        assert isinstance(result["environment"], list), "Should serialize as list"
        assert result["environment"] == ["production"]

        # Test list input
        data = {"environment": ["frontend", "backend"]}
        result = column.to_backend(data)
        assert isinstance(result["environment"], list), "Should serialize as list"
        assert result["environment"] == ["frontend", "backend"]

    def test_lifecycle_serializes_as_array(self) -> None:
        """Verify lifecycle serializes as array for API."""
        column = getattr(SnykProject, "lifecycle", None)
        assert column is not None, "lifecycle column not found"
        column.name = "lifecycle"

        # Test single value input
        data: dict[str, Any] = {"lifecycle": "production"}
        result = column.to_backend(data)
        assert isinstance(result["lifecycle"], list), "Should serialize as list"
        assert result["lifecycle"] == ["production"]

        # Test list input
        data = {"lifecycle": ["production", "development"]}
        result = column.to_backend(data)
        assert isinstance(result["lifecycle"], list), "Should serialize as list"
        assert result["lifecycle"] == ["production", "development"]


class TestSelectListDeserializationFormat:
    """Test that SelectList columns deserialize correctly from the Snyk API."""

    def test_business_criticality_deserializes_from_array(self) -> None:
        """Verify business_criticality deserializes from array."""
        column = getattr(SnykProject, "business_criticality", None)
        assert column is not None, "business_criticality column not found"
        column.name = "business_criticality"

        # Test array input from API
        result = column.from_backend(["critical", "high"])
        assert isinstance(result, list), "Should deserialize as list"
        assert result == ["critical", "high"]

        # Test empty array
        result = column.from_backend([])
        assert result == []

        # Test None
        result = column.from_backend(None)
        assert result == []

    def test_environment_deserializes_from_array(self) -> None:
        """Verify environment deserializes from array."""
        column = getattr(SnykProject, "environment", None)
        assert column is not None, "environment column not found"
        column.name = "environment"

        # Test array input from API
        result = column.from_backend(["external", "hosted"])
        assert isinstance(result, list), "Should deserialize as list"
        assert result == ["external", "hosted"]

    def test_lifecycle_deserializes_from_array(self) -> None:
        """Verify lifecycle deserializes from array."""
        column = getattr(SnykProject, "lifecycle", None)
        assert column is not None, "lifecycle column not found"
        column.name = "lifecycle"

        # Test array input from API
        result = column.from_backend(["production"])
        assert isinstance(result, list), "Should deserialize as list"
        assert result == ["production"]
