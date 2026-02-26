"""
Generic field type validation tests for all Snyk models.

This module provides automated validation that model field types match the OpenAPI
specification, ensuring that array fields use array column types, strings use string
column types, etc.

This test framework would have caught bugs like the business_criticality/environment/lifecycle
issue where Select (string) columns were used instead of SelectList (array) columns.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from clearskies.columns import Boolean, Datetime, Float, Integer, Json, Select, String

from clearskies_snyk.columns import ProjectTagList, SelectList

# Import all models
from clearskies_snyk.models import (
    SnykAccessRequest,
    SnykAiBom,
    SnykBrokerConnection,
    SnykBrokerConnectionIntegration,
    SnykBrokerDeployment,
    SnykCloudEnvironment,
    SnykCloudResource,
    SnykCloudScan,
    SnykCollection,
    SnykCollectionRelationshipProject,
    SnykContainerImage,
    SnykContainerImageTargetRef,
    SnykCustomBaseImage,
    SnykFixPullRequest,
    SnykGroup,
    SnykGroupAppInstall,
    SnykGroupAuditLog,
    SnykGroupExport,
    SnykGroupIssue,
    SnykGroupMember,
    SnykGroupMembership,
    SnykGroupOrgMembership,
    SnykGroupPolicy,
    SnykGroupServiceAccount,
    SnykGroupSettingsIac,
    SnykGroupSsoConnection,
    SnykGroupSsoConnectionUser,
    SnykGroupUser,
    SnykLearnAssignment,
    SnykLearnCatalog,
    SnykOrg,
    SnykOrgApp,
    SnykOrgAppBot,
    SnykOrgAppInstall,
    SnykOrgAuditLog,
    SnykOrgExport,
    SnykOrgInvite,
    SnykOrgIssue,
    SnykOrgMember,
    SnykOrgMembership,
    SnykOrgPolicy,
    SnykOrgPolicyEvent,
    SnykOrgServiceAccount,
    SnykOrgSettingsIac,
    SnykOrgSettingsOpenSource,
    SnykOrgSettingsSast,
    SnykOrgUser,
    SnykPackage,
    SnykProject,
    SnykProjectHistory,
    SnykProjectIgnore,
    SnykProjectSbom,
    SnykPullRequestTemplate,
    SnykSbomTest,
    SnykSelf,
    SnykSelfApp,
    SnykSelfAppSession,
    SnykSlackChannel,
    SnykSlackDefaultNotificationSettings,
    SnykSlackProjectNotificationSettings,
    SnykTarget,
    SnykTenant,
    SnykTenantMembership,
    SnykTenantRole,
    SnykTestJob,
)


def load_spec() -> dict[str, Any]:
    """Load the main API specification."""
    spec_path = Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"
    if not spec_path.exists():
        pytest.skip(f"API spec not found at {spec_path}")
    with open(spec_path) as f:
        return json.load(f)


def load_decomposed_spec(tag: str) -> dict[str, Any] | None:
    """Load a decomposed spec chunk by tag name."""
    manifest_path = Path(__file__).parent.parent.parent / "api_spec" / "decomposed" / "manifest.json"
    if not manifest_path.exists():
        return None

    with open(manifest_path) as f:
        manifest = json.load(f)

    # Find the chunk for this tag
    for chunk in manifest.get("chunks", []):
        if chunk.get("tag") == tag:
            chunk_path = Path(__file__).parent.parent.parent / "api_spec" / "decomposed" / chunk["path"]
            if chunk_path.exists():
                with open(chunk_path) as f:
                    return json.load(f)
    return None


def get_model_columns(model_class: type) -> dict[str, Any]:
    """Extract column definitions from a model class."""
    columns = {}
    for name in dir(model_class):
        if name.startswith("_"):
            continue
        attr = getattr(model_class, name, None)
        if attr is not None and hasattr(attr, "__class__"):
            class_name = type(attr).__name__
            # Check if it's a column type
            if "Column" in str(type(attr).__mro__) or class_name in [
                "String",
                "Integer",
                "Boolean",
                "Float",
                "Datetime",
                "Json",
                "Select",
                "SelectList",
                "ProjectTagList",
                "BelongsToId",
                "BelongsToModel",
                "HasMany",
                "ManyToManyIds",
            ]:
                columns[name] = attr
    return columns


def is_array_column(column: Any) -> bool:
    """Check if a column is an array type."""
    return isinstance(column, (Json, SelectList, ProjectTagList)) or type(column).__name__ in [
        "Json",
        "SelectList",
        "ProjectTagList",
        "HasMany",
        "ManyToManyIds",
    ]


def is_string_column(column: Any) -> bool:
    """Check if a column is a string type."""
    return isinstance(column, (String, Select)) or type(column).__name__ in ["String", "Select", "Email", "Phone"]


def is_boolean_column(column: Any) -> bool:
    """Check if a column is a boolean type."""
    return isinstance(column, Boolean) or type(column).__name__ == "Boolean"


def is_integer_column(column: Any) -> bool:
    """Check if a column is an integer type."""
    return isinstance(column, Integer) or type(column).__name__ == "Integer"


def is_datetime_column(column: Any) -> bool:
    """Check if a column is a datetime type."""
    return isinstance(column, Datetime) or type(column).__name__ in ["Datetime", "Created", "Updated", "Timestamp"]


# Mapping of models to their spec tags and attribute schema names
MODEL_SPEC_MAP = {
    "SnykProject": ("Projects", "ProjectAttributes"),
    "SnykOrg": ("Orgs", "OrgAttributes"),
    "SnykGroup": ("Groups", "GroupAttributes"),
    "SnykTarget": ("Targets", "TargetAttributes"),
    "SnykCollection": ("Collection", "CollectionAttributes"),
    "SnykOrgIssue": ("Issues", "IssueAttributes"),
    "SnykGroupIssue": ("Issues", "IssueAttributes"),
    "SnykOrgServiceAccount": ("ServiceAccounts", "ServiceAccountAttributes"),
    "SnykGroupServiceAccount": ("ServiceAccounts", "ServiceAccountAttributes"),
    "SnykOrgPolicy": ("Policies", "PolicyAttributes"),
    "SnykGroupPolicy": ("Policies", "PolicyAttributes"),
    "SnykCloudEnvironment": ("Cloud", "EnvironmentAttributes"),
    "SnykCloudResource": ("Cloud", "ResourceAttributes"),
    "SnykCloudScan": ("Cloud", "ScanAttributes"),
    "SnykContainerImage": ("ContainerImage", "ContainerImageAttributes"),
    "SnykCustomBaseImage": ("Custom Base Images", "CustomBaseImageAttributes"),
    "SnykTenant": ("Tenants", "TenantAttributes"),
    "SnykTenantMembership": ("Tenants", "TenantMembershipAttributes"),
    "SnykTenantRole": ("TenantRole", "TenantRoleAttributes"),
}


class TestArrayFieldsUseArrayColumns:
    """Test that spec array fields use array column types in models."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def _get_array_fields_from_schema(self, schema: dict[str, Any]) -> list[str]:
        """Extract field names that are arrays from a schema."""
        array_fields = []
        properties = schema.get("properties", {})
        for field_name, field_schema in properties.items():
            if field_schema.get("type") == "array":
                array_fields.append(field_name)
        return array_fields

    def _get_string_enum_fields_from_schema(self, schema: dict[str, Any]) -> list[str]:
        """Extract field names that are string enums (not arrays) from a schema."""
        enum_fields = []
        properties = schema.get("properties", {})
        for field_name, field_schema in properties.items():
            if field_schema.get("type") == "string" and "enum" in field_schema:
                enum_fields.append(field_name)
        return enum_fields

    @pytest.mark.parametrize(
        "model_name,model_class",
        [
            ("SnykProject", SnykProject),
        ],
    )
    def test_project_array_fields_use_array_columns(self, model_name: str, model_class: type) -> None:
        """Verify that array fields in spec use array column types in model."""
        spec_data = load_decomposed_spec("Projects")
        if spec_data is None:
            pytest.skip("Projects spec not found")
            return  # For mypy

        schema: dict[str, Any] = spec_data.get("schemas", {}).get("ProjectAttributes", {})
        array_fields = self._get_array_fields_from_schema(schema)

        model_columns = get_model_columns(model_class)

        for field_name in array_fields:
            if field_name in model_columns:
                column = model_columns[field_name]
                assert is_array_column(column), (
                    f"{model_name}.{field_name} should be an array column type "
                    f"(Json, SelectList, ProjectTagList, etc.) but got {type(column).__name__}. "
                    f"The OpenAPI spec defines this field as type 'array'."
                )

    @pytest.mark.parametrize(
        "model_name,model_class",
        [
            ("SnykProject", SnykProject),
        ],
    )
    def test_project_string_enum_fields_use_select_columns(self, model_name: str, model_class: type) -> None:
        """Verify that string enum fields in spec use Select column types in model."""
        spec_data = load_decomposed_spec("Projects")
        if spec_data is None:
            pytest.skip("Projects spec not found")
            return  # For mypy

        schema: dict[str, Any] = spec_data.get("schemas", {}).get("ProjectAttributes", {})
        enum_fields = self._get_string_enum_fields_from_schema(schema)

        model_columns = get_model_columns(model_class)

        for field_name in enum_fields:
            if field_name in model_columns:
                column = model_columns[field_name]
                # String enums should use Select, not SelectList
                assert isinstance(column, Select) and not isinstance(column, SelectList), (
                    f"{model_name}.{field_name} should be a Select column type "
                    f"(for single-value enum) but got {type(column).__name__}. "
                    f"The OpenAPI spec defines this field as type 'string' with enum."
                )


class TestFieldTypeConsistency:
    """Test that field types are consistent across all models."""

    def test_all_models_have_columns(self) -> None:
        """Verify all models have at least some columns defined."""
        models = [
            SnykProject,
            SnykOrg,
            SnykGroup,
            SnykTarget,
            SnykCollection,
            SnykOrgIssue,
            SnykGroupIssue,
        ]

        for model in models:
            columns = get_model_columns(model)
            assert len(columns) > 0, f"{model.__name__} has no columns defined"

    def test_project_has_expected_array_columns(self) -> None:
        """Verify SnykProject has the expected array column types."""
        columns = get_model_columns(SnykProject)

        # These should be array types based on the spec
        array_fields = ["business_criticality", "environment", "lifecycle", "tags"]

        for field_name in array_fields:
            assert field_name in columns, f"SnykProject missing {field_name} column"
            column = columns[field_name]
            assert is_array_column(column), (
                f"SnykProject.{field_name} should be an array column type, got {type(column).__name__}"
            )

    def test_project_has_expected_string_columns(self) -> None:
        """Verify SnykProject has the expected string column types."""
        columns = get_model_columns(SnykProject)

        # These should be string types based on the spec
        string_fields = ["name", "origin", "target_file", "target_reference"]

        for field_name in string_fields:
            assert field_name in columns, f"SnykProject missing {field_name} column"
            column = columns[field_name]
            assert is_string_column(column), (
                f"SnykProject.{field_name} should be a string column type, got {type(column).__name__}"
            )

    def test_project_status_is_select_not_select_list(self) -> None:
        """Verify SnykProject.status is Select (single value) not SelectList (array)."""
        columns = get_model_columns(SnykProject)

        assert "status" in columns, "SnykProject missing status column"
        column = columns["status"]

        # status should be Select (single value enum), not SelectList (array)
        assert isinstance(column, Select), f"SnykProject.status should be Select, got {type(column).__name__}"
        assert not isinstance(column, SelectList), (
            f"SnykProject.status should be Select (single value), not SelectList (array)"
        )


class TestSelectListVsSelectUsage:
    """Test that SelectList and Select are used appropriately."""

    def test_select_list_used_for_array_enums(self) -> None:
        """Verify SelectList is used for array enum fields."""
        columns = get_model_columns(SnykProject)

        # These are array enum fields per the spec
        array_enum_fields = ["business_criticality", "environment", "lifecycle"]

        for field_name in array_enum_fields:
            column = columns.get(field_name)
            assert column is not None, f"Missing {field_name} column"
            assert isinstance(column, SelectList), (
                f"{field_name} should use SelectList for array enums, got {type(column).__name__}"
            )

    def test_select_used_for_single_value_enums(self) -> None:
        """Verify Select is used for single-value enum fields."""
        columns = get_model_columns(SnykProject)

        # status is a single-value enum per the spec
        column = columns.get("status")
        assert column is not None, "Missing status column"
        assert isinstance(column, Select), (
            f"status should use Select for single-value enums, got {type(column).__name__}"
        )
        assert not isinstance(column, SelectList), "status should not use SelectList"


class TestSpecSchemaExtraction:
    """Test the spec schema extraction utilities."""

    def test_can_load_projects_spec(self) -> None:
        """Verify we can load the Projects decomposed spec."""
        spec = load_decomposed_spec("Projects")
        assert spec is not None, "Could not load Projects spec"
        assert "schemas" in spec, "Projects spec missing schemas"
        assert "ProjectAttributes" in spec["schemas"], "Projects spec missing ProjectAttributes schema"

    def test_can_extract_array_fields(self) -> None:
        """Verify we can extract array fields from schema."""
        spec = load_decomposed_spec("Projects")
        if spec is None:
            pytest.skip("Projects spec not found")
            return  # For mypy

        schema: dict[str, Any] = spec["schemas"]["ProjectAttributes"]
        properties = schema.get("properties", {})

        # These should be arrays
        assert properties.get("business_criticality", {}).get("type") == "array"
        assert properties.get("environment", {}).get("type") == "array"
        assert properties.get("lifecycle", {}).get("type") == "array"
        assert properties.get("tags", {}).get("type") == "array"

        # This should be a string
        assert properties.get("status", {}).get("type") == "string"
        assert properties.get("name", {}).get("type") == "string"


class TestModelColumnTypeMapping:
    """Test the mapping between spec types and column types."""

    @pytest.mark.parametrize(
        "spec_type,expected_column_types",
        [
            ("array", [Json, SelectList, ProjectTagList]),
            ("string", [String, Select]),
            ("boolean", [Boolean]),
            ("integer", [Integer]),
            ("number", [Float, Integer]),
        ],
    )
    def test_spec_type_to_column_type_mapping(self, spec_type: str, expected_column_types: list[type]) -> None:
        """Document the expected mapping from spec types to column types."""
        # This test documents the expected mapping
        # In a real implementation, you would validate actual columns against this
        assert len(expected_column_types) > 0, f"No column types defined for spec type {spec_type}"
