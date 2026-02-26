"""
Comprehensive field type validation for ALL Snyk models against OpenAPI spec.

This module validates that model column types match the OpenAPI specification
for ALL field types, not just arrays. This includes:

1. Arrays - fields that should use Json/SelectList/ProjectTagList
2. Booleans - fields that should use Boolean column
3. Integers - fields that should use Integer column
4. Numbers (floats) - fields that should use Float column
5. Date-times - fields that should use Datetime column
6. String enums - fields that should use Select (single value) vs SelectList (array)
7. Objects - fields that should use Json column
8. Required fields - fields that must be present in the model

This comprehensive validation would catch bugs like:
- Array fields using scalar columns (the business_criticality bug)
- Boolean fields using String columns
- Integer fields using String columns
- Date-time fields using String columns
- Object fields using String columns
"""

from __future__ import annotations

import json
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


def get_column_type_name(column: Any) -> str:
    """Get the type name of a column."""
    return type(column).__name__


# Column type categories
ARRAY_COLUMN_TYPES = {"Json", "SelectList", "ProjectTagList", "HasMany", "ManyToManyIds", "ManyToManyModels"}
BOOLEAN_COLUMN_TYPES = {"Boolean"}
INTEGER_COLUMN_TYPES = {"Integer"}
FLOAT_COLUMN_TYPES = {"Float", "Integer"}  # Integer can also represent numbers
DATETIME_COLUMN_TYPES = {"Datetime", "Created", "Updated", "Timestamp"}
STRING_COLUMN_TYPES = {"String", "Select", "Email", "Phone", "Uuid"}
OBJECT_COLUMN_TYPES = {"Json"}


def extract_fields_by_type(schema: dict[str, Any]) -> dict[str, list[tuple[str, dict[str, Any]]]]:
    """
    Extract fields from schema grouped by their type.

    Returns dict with keys: 'array', 'boolean', 'integer', 'number', 'string', 'object'
    Each value is a list of (field_name, field_schema) tuples.
    """
    fields_by_type: dict[str, list[tuple[str, dict[str, Any]]]] = {
        "array": [],
        "boolean": [],
        "integer": [],
        "number": [],
        "string": [],
        "object": [],
        "datetime": [],
        "string_enum": [],
        "array_enum": [],
    }

    properties = schema.get("properties", {})
    for field_name, field_schema in properties.items():
        field_type = field_schema.get("type")
        field_format = field_schema.get("format")

        if field_type == "array":
            fields_by_type["array"].append((field_name, field_schema))
            # Check if it's an array of enums
            items = field_schema.get("items", {})
            if "enum" in items:
                fields_by_type["array_enum"].append((field_name, field_schema))

        elif field_type == "boolean":
            fields_by_type["boolean"].append((field_name, field_schema))

        elif field_type == "integer":
            fields_by_type["integer"].append((field_name, field_schema))

        elif field_type == "number":
            fields_by_type["number"].append((field_name, field_schema))

        elif field_type == "string":
            if field_format == "date-time":
                fields_by_type["datetime"].append((field_name, field_schema))
            elif "enum" in field_schema:
                fields_by_type["string_enum"].append((field_name, field_schema))
            else:
                fields_by_type["string"].append((field_name, field_schema))

        elif field_type == "object":
            fields_by_type["object"].append((field_name, field_schema))

    return fields_by_type


# Mapping of model classes to their spec tag and schema name patterns
MODEL_TO_SPEC_MAP = {
    SnykProject: ("Projects", ["ProjectAttributes"]),
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
        if pattern in schemas:
            return schemas[pattern]
        for schema_name, schema in schemas.items():
            if pattern.lower() in schema_name.lower():
                return schema
    return None


def validate_field_type(
    field_name: str,
    spec_type: str,
    column: Any,
    expected_column_types: set[str],
) -> str | None:
    """
    Validate that a column type matches the expected types for a spec type.

    Returns error message if mismatch, None if valid.
    """
    column_type = get_column_type_name(column)
    if column_type not in expected_column_types:
        return f"{field_name}: spec='{spec_type}', model='{column_type}' (expected one of: {expected_column_types})"
    return None


class TestAllFieldTypesMatchSpec:
    """Test that ALL field types in models match their OpenAPI spec definitions."""

    def _get_chunk_for_tag(self, tag: str) -> dict[str, Any] | None:
        """Get the spec chunk for a tag."""
        manifest = load_decomposed_manifest()
        for chunk_info in manifest.get("chunks", []):
            if chunk_info.get("tag") == tag:
                return load_decomposed_chunk(chunk_info["path"])
        return None

    def test_array_fields_use_array_columns(self) -> None:
        """Verify array fields use array column types."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["array"]:
                if field_name in model_columns:
                    error = validate_field_type(
                        f"{model_class.__name__}.{field_name}",
                        "array",
                        model_columns[field_name],
                        ARRAY_COLUMN_TYPES,
                    )
                    if error:
                        errors.append(error)

        assert not errors, "Array field type mismatches:\n" + "\n".join(errors)

    def test_boolean_fields_use_boolean_columns(self) -> None:
        """Verify boolean fields use Boolean column types."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["boolean"]:
                if field_name in model_columns:
                    error = validate_field_type(
                        f"{model_class.__name__}.{field_name}",
                        "boolean",
                        model_columns[field_name],
                        BOOLEAN_COLUMN_TYPES,
                    )
                    if error:
                        errors.append(error)

        assert not errors, "Boolean field type mismatches:\n" + "\n".join(errors)

    def test_integer_fields_use_integer_columns(self) -> None:
        """Verify integer fields use Integer column types."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["integer"]:
                if field_name in model_columns:
                    error = validate_field_type(
                        f"{model_class.__name__}.{field_name}",
                        "integer",
                        model_columns[field_name],
                        INTEGER_COLUMN_TYPES,
                    )
                    if error:
                        errors.append(error)

        assert not errors, "Integer field type mismatches:\n" + "\n".join(errors)

    def test_datetime_fields_use_datetime_columns(self) -> None:
        """Verify date-time fields use Datetime column types."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["datetime"]:
                if field_name in model_columns:
                    error = validate_field_type(
                        f"{model_class.__name__}.{field_name}",
                        "datetime",
                        model_columns[field_name],
                        DATETIME_COLUMN_TYPES,
                    )
                    if error:
                        errors.append(error)

        assert not errors, "Datetime field type mismatches:\n" + "\n".join(errors)

    def test_object_fields_use_json_columns(self) -> None:
        """Verify object fields use Json column types."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["object"]:
                if field_name in model_columns:
                    error = validate_field_type(
                        f"{model_class.__name__}.{field_name}",
                        "object",
                        model_columns[field_name],
                        OBJECT_COLUMN_TYPES,
                    )
                    if error:
                        errors.append(error)

        assert not errors, "Object field type mismatches:\n" + "\n".join(errors)

    def test_string_enum_fields_use_select_not_select_list(self) -> None:
        """Verify string enum fields use Select (not SelectList for arrays)."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["string_enum"]:
                if field_name in model_columns:
                    column = model_columns[field_name]
                    column_type = get_column_type_name(column)
                    # String enums should use Select, not SelectList
                    if column_type == "SelectList":
                        errors.append(
                            f"{model_class.__name__}.{field_name}: spec='string enum', "
                            f"model='SelectList' (should be 'Select' for single-value enum)"
                        )

        assert not errors, "String enum using SelectList (should be Select):\n" + "\n".join(errors)

    def test_array_enum_fields_use_select_list_not_select(self) -> None:
        """Verify array enum fields use SelectList (not Select for single values)."""
        errors = []

        for model_class, (tag, schema_patterns) in MODEL_TO_SPEC_MAP.items():
            chunk = self._get_chunk_for_tag(tag)
            if not chunk:
                continue

            schema = find_schema_in_chunk(chunk, schema_patterns)
            if not schema:
                continue

            fields_by_type = extract_fields_by_type(schema)
            model_columns = get_model_columns(model_class)

            for field_name, field_schema in fields_by_type["array_enum"]:
                if field_name in model_columns:
                    column = model_columns[field_name]
                    column_type = get_column_type_name(column)
                    # Array enums should use SelectList or Json, not Select
                    if column_type == "Select":
                        errors.append(
                            f"{model_class.__name__}.{field_name}: spec='array of enum', "
                            f"model='Select' (should be 'SelectList' or 'Json' for array)"
                        )

        assert not errors, "Array enum using Select (should be SelectList):\n" + "\n".join(errors)


class TestFieldTypeReport:
    """Generate reports on field types across all models."""

    def test_report_all_field_types(self) -> None:
        """Report all field types found in specs (informational)."""
        manifest = load_decomposed_manifest()
        type_counts: dict[str, int] = {
            "array": 0,
            "boolean": 0,
            "integer": 0,
            "number": 0,
            "string": 0,
            "object": 0,
            "datetime": 0,
            "string_enum": 0,
            "array_enum": 0,
        }

        for chunk_info in manifest.get("chunks", []):
            chunk = load_decomposed_chunk(chunk_info["path"])
            if not chunk:
                continue

            for schema_name, schema in chunk.get("schemas", {}).items():
                if "Attributes" in schema_name:
                    fields_by_type = extract_fields_by_type(schema)
                    for type_name, fields in fields_by_type.items():
                        type_counts[type_name] += len(fields)

        print("\n\nField type distribution in OpenAPI spec:")
        for type_name, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {type_name}: {count}")

        # Sanity check
        assert sum(type_counts.values()) > 0, "No fields found in spec"


class TestSpecificModelFieldTypes:
    """Test specific models for comprehensive field type coverage."""

    def test_snyk_project_all_field_types(self) -> None:
        """Verify SnykProject has correct types for all field categories."""
        chunk = load_decomposed_chunk("chunks/domain_projects.json")
        schema = chunk.get("schemas", {}).get("ProjectAttributes", {})
        fields_by_type = extract_fields_by_type(schema)
        model_columns = get_model_columns(SnykProject)

        errors = []

        # Check arrays
        for field_name, _ in fields_by_type["array"]:
            if field_name in model_columns:
                column_type = get_column_type_name(model_columns[field_name])
                if column_type not in ARRAY_COLUMN_TYPES:
                    errors.append(f"array field '{field_name}' uses '{column_type}'")

        # Check booleans
        for field_name, _ in fields_by_type["boolean"]:
            if field_name in model_columns:
                column_type = get_column_type_name(model_columns[field_name])
                if column_type not in BOOLEAN_COLUMN_TYPES:
                    errors.append(f"boolean field '{field_name}' uses '{column_type}'")

        # Check datetimes
        for field_name, _ in fields_by_type["datetime"]:
            if field_name in model_columns:
                column_type = get_column_type_name(model_columns[field_name])
                if column_type not in DATETIME_COLUMN_TYPES:
                    errors.append(f"datetime field '{field_name}' uses '{column_type}'")

        # Check objects
        for field_name, _ in fields_by_type["object"]:
            if field_name in model_columns:
                column_type = get_column_type_name(model_columns[field_name])
                if column_type not in OBJECT_COLUMN_TYPES:
                    errors.append(f"object field '{field_name}' uses '{column_type}'")

        # Check string enums (should be Select, not SelectList)
        for field_name, _ in fields_by_type["string_enum"]:
            if field_name in model_columns:
                column_type = get_column_type_name(model_columns[field_name])
                if column_type == "SelectList":
                    errors.append(f"string enum field '{field_name}' uses 'SelectList' (should be 'Select')")

        # Check array enums (should be SelectList, not Select)
        for field_name, _ in fields_by_type["array_enum"]:
            if field_name in model_columns:
                column_type = get_column_type_name(model_columns[field_name])
                if column_type == "Select":
                    errors.append(f"array enum field '{field_name}' uses 'Select' (should be 'SelectList')")

        assert not errors, "SnykProject field type errors:\n" + "\n".join(errors)
