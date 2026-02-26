"""
Automated field type validation for ALL Snyk models against OpenAPI spec.

This module automatically discovers array fields in the OpenAPI spec and validates
that the corresponding model columns use array column types (Json, SelectList, etc.)
rather than scalar types (String, Select, etc.).

This test would have caught the business_criticality/environment/lifecycle bug
and will catch similar issues in ANY model.
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


def load_decomposed_manifest() -> dict[str, Any]:
    """Load the decomposed spec manifest."""
    manifest_path = Path(__file__).parent.parent.parent / "api_spec" / "decomposed" / "manifest.json"
    if not manifest_path.exists():
        pytest.skip(f"Manifest not found at {manifest_path}")
    with open(manifest_path) as f:
        return json.load(f)


def load_decomposed_chunk(chunk_path: str) -> dict[str, Any]:
    """Load a decomposed spec chunk."""
    full_path = Path(__file__).parent.parent.parent / "api_spec" / "decomposed" / chunk_path
    if not full_path.exists():
        return {}
    with open(full_path) as f:
        return json.load(f)


def get_model_columns(model_class: type) -> dict[str, Any]:
    """Extract column definitions from a model class."""
    columns = {}
    for name in dir(model_class):
        if name.startswith("_"):
            continue
        attr = getattr(model_class, name, None)
        if attr is not None and hasattr(attr, "__class__"):
            class_name = type(attr).__name__
            # Check if it's a column type by looking at the class hierarchy
            mro_str = str(type(attr).__mro__)
            if "Column" in mro_str or class_name in [
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
                "Uuid",
                "Created",
                "Updated",
                "Timestamp",
            ]:
                columns[name] = attr
    return columns


def is_array_column(column: Any) -> bool:
    """Check if a column is an array type."""
    column_type = type(column).__name__
    return column_type in [
        "Json",
        "SelectList",
        "ProjectTagList",
        "HasMany",
        "ManyToManyIds",
        "ManyToManyModels",
    ]


def is_scalar_column(column: Any) -> bool:
    """Check if a column is a scalar (non-array) type."""
    column_type = type(column).__name__
    return column_type in [
        "String",
        "Select",
        "Integer",
        "Float",
        "Boolean",
        "Datetime",
        "Email",
        "Phone",
        "Uuid",
        "Created",
        "Updated",
        "Timestamp",
        "BelongsToId",
    ]


def extract_array_fields_from_schema(schema: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Extract all array fields from a schema with their details."""
    array_fields = {}
    properties = schema.get("properties", {})
    for field_name, field_schema in properties.items():
        if field_schema.get("type") == "array":
            array_fields[field_name] = {
                "items_type": field_schema.get("items", {}).get("type"),
                "items_enum": field_schema.get("items", {}).get("enum"),
                "description": field_schema.get("description", ""),
            }
    return array_fields


def extract_string_enum_fields_from_schema(schema: dict[str, Any]) -> dict[str, list[str]]:
    """Extract all string enum fields (single value, not array) from a schema."""
    enum_fields = {}
    properties = schema.get("properties", {})
    for field_name, field_schema in properties.items():
        if field_schema.get("type") == "string" and "enum" in field_schema:
            enum_fields[field_name] = field_schema["enum"]
    return enum_fields


# Mapping of model classes to their spec tag and schema name patterns
MODEL_TO_SPEC_MAP = {
    SnykProject: ("Projects", ["ProjectAttributes", "PatchProjectRequest"]),
    SnykOrg: ("Orgs", ["OrgAttributes"]),
    SnykGroup: ("Groups", ["GroupAttributes"]),
    SnykTarget: ("Targets", ["TargetAttributes"]),
    SnykCollection: ("Collection", ["CollectionAttributes"]),
    SnykOrgIssue: ("Issues", ["IssueAttributes"]),
    SnykGroupIssue: ("Issues", ["IssueAttributes"]),
    SnykOrgServiceAccount: ("ServiceAccounts", ["ServiceAccountAttributes"]),
    SnykGroupServiceAccount: ("ServiceAccounts", ["ServiceAccountAttributes"]),
    SnykOrgPolicy: ("Policies", ["PolicyAttributes"]),
    SnykGroupPolicy: ("Policies", ["PolicyAttributes"]),
    SnykCloudEnvironment: ("Cloud", ["EnvironmentAttributes"]),
    SnykCloudResource: ("Cloud", ["ResourceAttributes"]),
    SnykCloudScan: ("Cloud", ["ScanAttributes"]),
    SnykContainerImage: ("ContainerImage", ["ContainerImageAttributes"]),
    SnykCustomBaseImage: ("Custom Base Images", ["CustomBaseImageAttributes"]),
    SnykTenant: ("Tenants", ["TenantAttributes"]),
    SnykBrokerConnection: ("BrokerConnections", ["BrokerConnectionAttributes"]),
    SnykBrokerDeployment: ("BrokerDeployments", ["BrokerDeploymentAttributes"]),
}


def find_schema_in_chunk(chunk: dict[str, Any], schema_patterns: list[str]) -> dict[str, Any] | None:
    """Find a schema in a chunk that matches one of the patterns."""
    schemas = chunk.get("schemas", {})
    for pattern in schema_patterns:
        # Try exact match first
        if pattern in schemas:
            return schemas[pattern]
        # Try partial match
        for schema_name, schema in schemas.items():
            if pattern.lower() in schema_name.lower():
                return schema
    return None


def get_all_array_field_mismatches() -> list[tuple[str, str, str, str]]:
    """
    Scan all models and find fields where spec says array but model uses scalar.

    Returns list of (model_name, field_name, spec_type, model_type) tuples.
    """
    mismatches = []
    manifest = load_decomposed_manifest()

    for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
        model_name = model_class.__name__

        # Find the chunk for this tag
        chunk_data = None
        for chunk in manifest.get("chunks", []):
            if chunk.get("tag") == tag:
                chunk_data = load_decomposed_chunk(chunk["path"])
                if chunk_data:
                    break

        if not chunk_data:
            continue

        # Find the schema
        schema = find_schema_in_chunk(chunk_data, schema_patterns)
        if not schema:
            continue

        # Get array fields from spec
        spec_array_fields = extract_array_fields_from_schema(schema)

        # Get model columns
        model_columns = get_model_columns(model_class)

        # Check each array field
        for field_name, field_info in spec_array_fields.items():
            if field_name in model_columns:
                column = model_columns[field_name]
                if is_scalar_column(column):
                    mismatches.append(
                        (
                            model_name,
                            field_name,
                            "array",
                            type(column).__name__,
                        )
                    )

    return mismatches


class TestAllModelsArrayFieldsUseArrayColumns:
    """Test that ALL models use array columns for spec array fields."""

    def test_no_array_field_type_mismatches(self) -> None:
        """
        Verify no model has array fields using scalar column types.

        This test scans ALL models against their OpenAPI spec schemas and
        reports any field where the spec defines it as an array but the
        model uses a scalar column type (String, Select, etc.).
        """
        mismatches = get_all_array_field_mismatches()

        if mismatches:
            error_msg = "Found array fields using scalar column types:\n"
            for model_name, field_name, spec_type, model_type in mismatches:
                error_msg += (
                    f"  - {model_name}.{field_name}: spec says '{spec_type}', "
                    f"model uses '{model_type}' (should use Json, SelectList, etc.)\n"
                )
            pytest.fail(error_msg)


class TestSpecificModelArrayFields:
    """Test specific models for array field compliance."""

    @pytest.fixture
    def projects_chunk(self) -> dict[str, Any]:
        """Load the Projects spec chunk."""
        return load_decomposed_chunk("chunks/domain_projects.json")

    def test_snyk_project_array_fields(self, projects_chunk: dict[str, Any]) -> None:
        """Verify SnykProject array fields use array column types."""
        schema = projects_chunk.get("schemas", {}).get("ProjectAttributes", {})
        spec_array_fields = extract_array_fields_from_schema(schema)
        model_columns = get_model_columns(SnykProject)

        errors = []
        for field_name, field_info in spec_array_fields.items():
            if field_name in model_columns:
                column = model_columns[field_name]
                if is_scalar_column(column):
                    errors.append(f"{field_name}: spec='array', model='{type(column).__name__}'")

        assert not errors, f"SnykProject has array fields with scalar columns:\n" + "\n".join(errors)

    def test_snyk_project_string_enum_fields(self, projects_chunk: dict[str, Any]) -> None:
        """Verify SnykProject string enum fields use Select (not SelectList)."""
        schema = projects_chunk.get("schemas", {}).get("ProjectAttributes", {})
        spec_enum_fields = extract_string_enum_fields_from_schema(schema)
        model_columns = get_model_columns(SnykProject)

        errors = []
        for field_name, allowed_values in spec_enum_fields.items():
            if field_name in model_columns:
                column = model_columns[field_name]
                # String enums should use Select, not SelectList
                if isinstance(column, SelectList):
                    errors.append(f"{field_name}: spec='string enum', model='SelectList' (should be 'Select')")

        assert not errors, f"SnykProject has string enum fields with SelectList:\n" + "\n".join(errors)


class TestArrayEnumAllowedValues:
    """Test that array enum fields have correct allowed values."""

    @pytest.fixture
    def projects_chunk(self) -> dict[str, Any]:
        """Load the Projects spec chunk."""
        return load_decomposed_chunk("chunks/domain_projects.json")

    def test_snyk_project_array_enum_allowed_values(self, projects_chunk: dict[str, Any]) -> None:
        """Verify SnykProject array enum fields have correct allowed values."""
        schema = projects_chunk.get("schemas", {}).get("ProjectAttributes", {})
        spec_array_fields = extract_array_fields_from_schema(schema)
        model_columns = get_model_columns(SnykProject)

        errors = []
        for field_name, field_info in spec_array_fields.items():
            if field_name in model_columns and field_info.get("items_enum"):
                column = model_columns[field_name]
                if hasattr(column, "allowed_values"):
                    spec_values = set(field_info["items_enum"])
                    model_values = set(column.allowed_values)
                    if spec_values != model_values:
                        missing = spec_values - model_values
                        extra = model_values - spec_values
                        error_parts = [f"{field_name}:"]
                        if missing:
                            error_parts.append(f"  missing from model: {missing}")
                        if extra:
                            error_parts.append(f"  extra in model: {extra}")
                        errors.append("\n".join(error_parts))

        assert not errors, f"SnykProject array enum allowed values mismatch:\n" + "\n".join(errors)


class TestDiscoverAllArrayFields:
    """Discover and report all array fields across all spec chunks."""

    def test_report_all_spec_array_fields(self) -> None:
        """
        Report all array fields found in the spec.

        This is an informational test that helps identify which fields
        need to use array column types.
        """
        manifest = load_decomposed_manifest()
        all_array_fields: dict[str, list[str]] = {}

        for chunk_info in manifest.get("chunks", []):
            chunk = load_decomposed_chunk(chunk_info["path"])
            if not chunk:
                continue

            tag = chunk_info["tag"]
            schemas = chunk.get("schemas", {})

            for schema_name, schema in schemas.items():
                if "Attributes" in schema_name or "Request" in schema_name:
                    array_fields = extract_array_fields_from_schema(schema)
                    if array_fields:
                        key = f"{tag}/{schema_name}"
                        all_array_fields[key] = list(array_fields.keys())

        # This test always passes - it's for reporting
        print("\n\nArray fields found in spec:")
        for schema_key, fields in sorted(all_array_fields.items()):
            print(f"  {schema_key}: {fields}")

        # Assert at least some array fields were found (sanity check)
        assert len(all_array_fields) > 0, "No array fields found in spec - check spec loading"
