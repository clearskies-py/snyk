#!/usr/bin/env python3
"""
Comprehensive model-to-spec compliance checker.

This script validates that all clearskies-snyk models correctly implement
the Snyk REST API as defined in the OpenAPI specification.

Usage:
    python tools/check_spec_compliance.py [--spec PATH] [--models-dir DIR] [--verbose]

Examples:
    # Check v2 models against v2 spec (default)
    python tools/check_spec_compliance.py --verbose

    # Check v1 models against v1 spec
    python tools/check_spec_compliance.py --spec api_spec/v1-api-spec.yaml --models-dir src/clearskies_snyk/models/v1 --verbose
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]


@dataclass
class ColumnInfo:
    """Information about a model column."""

    name: str
    column_type: str
    is_searchable: bool = False
    is_temporary: bool = False


@dataclass
class ModelInfo:
    """Information about a model."""

    name: str
    destination_name: str
    columns: list[ColumnInfo] = field(default_factory=list)
    id_column_name: str = "id"


@dataclass
class EndpointInfo:
    """Information about an API endpoint."""

    path: str
    method: str
    operation_id: str
    tags: list[str]
    parameters: list[dict[str, Any]]
    request_body_schema: str | None
    response_schema: str | None


@dataclass
class SchemaInfo:
    """Information about an API schema."""

    name: str
    properties: dict[str, dict[str, Any]]
    required: list[str]


@dataclass
class ComplianceIssue:
    """A compliance issue found during validation."""

    model: str
    severity: str  # "error", "warning", "info"
    category: str
    message: str
    details: str | None = None


def load_spec(spec_path: str | Path) -> dict[str, Any]:
    """Load the OpenAPI specification (JSON or YAML)."""
    spec_path = Path(spec_path)
    with open(spec_path) as f:
        if spec_path.suffix in (".yaml", ".yml"):
            return yaml.safe_load(f)
        return json.load(f)


def extract_models(models_dir: str | Path = "src/clearskies_snyk/models") -> dict[str, ModelInfo]:
    """Extract model information from the codebase."""
    models: dict[str, ModelInfo] = {}
    models_dir = Path(models_dir)

    for model_file in models_dir.glob("*.py"):
        if model_file.name.startswith("_"):
            continue

        content = model_file.read_text()

        # Extract class name
        class_match = re.search(r"class\s+(\w+)\s*\(", content)
        if not class_match:
            continue

        class_name = class_match.group(1)

        # Skip reference classes
        if "Reference" in class_name:
            continue

        # Extract destination_name - handle multiple patterns including docstrings
        dest_patterns = [
            # Pattern with docstring: def destination_name(...): """...""" return "..."
            r'def\s+destination_name\s*\([^)]*\)[^:]*:.*?return\s*["\']([^"\']+)["\']',
        ]
        destination = ""
        for pattern in dest_patterns:
            dest_match = re.search(pattern, content, re.DOTALL)
            if dest_match:
                destination = dest_match.group(1)
                break

        # Extract columns
        columns = []
        column_pattern = (
            r"^\s+(\w+)\s*=\s*(String|Boolean|Integer|Datetime|Json|Select|HasMany|BelongsTo|ProjectTagList)\s*\("
        )
        for match in re.finditer(column_pattern, content, re.MULTILINE):
            col_name = match.group(1)
            col_type = match.group(2)

            # Check for is_searchable
            line_start = match.start()
            line_end = content.find("\n", match.end())
            if line_end == -1:
                line_end = len(content)
            line = content[line_start:line_end]

            is_searchable = "is_searchable=True" in line
            is_temporary = "is_temporary=True" in line

            columns.append(
                ColumnInfo(
                    name=col_name,
                    column_type=col_type,
                    is_searchable=is_searchable,
                    is_temporary=is_temporary,
                )
            )

        # Extract id_column_name
        id_match = re.search(r'id_column_name\s*[=:]\s*["\'](\w+)["\']', content)
        id_column = id_match.group(1) if id_match else "id"

        models[class_name] = ModelInfo(
            name=class_name,
            destination_name=destination,
            columns=columns,
            id_column_name=id_column,
        )

    return models


def extract_endpoints(spec: dict[str, Any]) -> dict[str, list[EndpointInfo]]:
    """Extract endpoint information from the spec, grouped by normalized path."""
    endpoints: dict[str, list[EndpointInfo]] = {}

    for path, methods in spec.get("paths", {}).items():
        # Normalize path for matching
        normalized = re.sub(r"\{[^}]+\}", "{param}", path)

        if normalized not in endpoints:
            endpoints[normalized] = []

        for method, details in methods.items():
            if not isinstance(details, dict):
                continue

            # Extract response schema
            response_schema = None
            responses = details.get("responses", {})
            for status, response in responses.items():
                if status.startswith("2"):
                    content = response.get("content", {})
                    json_content = content.get("application/vnd.api+json", content.get("application/json", {}))
                    schema = json_content.get("schema", {})
                    if "$ref" in schema:
                        response_schema = schema["$ref"].split("/")[-1]
                    break

            # Extract request body schema
            request_schema = None
            request_body = details.get("requestBody", {})
            if request_body:
                content = request_body.get("content", {})
                json_content = content.get("application/vnd.api+json", content.get("application/json", {}))
                schema = json_content.get("schema", {})
                if "$ref" in schema:
                    request_schema = schema["$ref"].split("/")[-1]

            endpoints[normalized].append(
                EndpointInfo(
                    path=path,
                    method=method.upper(),
                    operation_id=details.get("operationId", ""),
                    tags=details.get("tags", []),
                    parameters=details.get("parameters", []),
                    request_body_schema=request_schema,
                    response_schema=response_schema,
                )
            )

    return endpoints


def extract_schemas(spec: dict[str, Any]) -> dict[str, SchemaInfo]:
    """Extract schema information from the spec."""
    schemas: dict[str, SchemaInfo] = {}

    for name, schema in spec.get("components", {}).get("schemas", {}).items():
        properties = schema.get("properties", {})
        required = schema.get("required", [])

        schemas[name] = SchemaInfo(
            name=name,
            properties=properties,
            required=required,
        )

    return schemas


def normalize_destination(destination: str) -> str:
    """Normalize a destination name for comparison."""
    # Convert {param} style to {param}
    normalized = re.sub(r"\{[^}]+\}", "{param}", destination)
    # Ensure leading slash
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    return normalized


def find_matching_endpoints(model: ModelInfo, endpoints: dict[str, list[EndpointInfo]]) -> list[EndpointInfo]:
    """Find endpoints that match a model's destination."""
    if not model.destination_name:
        return []

    normalized_dest = normalize_destination(model.destination_name)

    matching = []
    for path, eps in endpoints.items():
        if normalized_dest == path or path.endswith(normalized_dest):
            matching.extend(eps)

    return matching


def check_endpoint_exists(model: ModelInfo, endpoints: dict[str, list[EndpointInfo]]) -> list[ComplianceIssue]:
    """Check if the model's endpoint exists in the spec."""
    issues = []

    if not model.destination_name:
        issues.append(
            ComplianceIssue(
                model=model.name,
                severity="warning",
                category="endpoint",
                message="No destination_name defined",
                details="Model should define destination_name() to specify the API endpoint",
            )
        )
        return issues

    matching = find_matching_endpoints(model, endpoints)

    if not matching:
        issues.append(
            ComplianceIssue(
                model=model.name,
                severity="error",
                category="endpoint",
                message=f"Endpoint not found in spec: {model.destination_name}",
                details=f"Normalized path: {normalize_destination(model.destination_name)}",
            )
        )

    return issues


def check_column_coverage(
    model: ModelInfo, endpoints: dict[str, list[EndpointInfo]], schemas: dict[str, SchemaInfo]
) -> list[ComplianceIssue]:
    """Check if model columns match the API schema."""
    issues: list[ComplianceIssue] = []

    matching = find_matching_endpoints(model, endpoints)
    if not matching:
        return issues

    # Get response schemas for GET endpoints
    response_schemas = set()
    for ep in matching:
        if ep.method == "GET" and ep.response_schema:
            response_schemas.add(ep.response_schema)

    # Find attribute schemas
    model_columns = {col.name for col in model.columns}

    for schema_name in response_schemas:
        schema = schemas.get(schema_name)
        if not schema:
            continue

        # Look for nested attribute schemas
        for prop_name, prop_def in schema.properties.items():
            if prop_name == "attributes" and "$ref" in prop_def:
                attr_schema_name = prop_def["$ref"].split("/")[-1]
                attr_schema = schemas.get(attr_schema_name)
                if attr_schema:
                    # Check for missing required properties
                    for required_prop in attr_schema.required:
                        if required_prop not in model_columns:
                            issues.append(
                                ComplianceIssue(
                                    model=model.name,
                                    severity="warning",
                                    category="column",
                                    message=f"Missing required column: {required_prop}",
                                    details=f"Schema {attr_schema_name} requires this property",
                                )
                            )

    return issues


def check_query_parameters(model: ModelInfo, endpoints: dict[str, list[EndpointInfo]]) -> list[ComplianceIssue]:
    """Check if searchable columns match query parameters."""
    issues: list[ComplianceIssue] = []

    matching = find_matching_endpoints(model, endpoints)
    if not matching:
        return issues

    # Get query parameters from GET endpoints
    query_params = set()
    for ep in matching:
        if ep.method == "GET":
            for param in ep.parameters:
                if param.get("in") == "query":
                    query_params.add(param.get("name"))

    # Check searchable columns
    searchable_columns = {col.name for col in model.columns if col.is_searchable}

    # Note: This is informational - not all query params need model columns
    for col in searchable_columns:
        if col not in query_params:
            # Convert query_params to list and filter None values
            sorted_params = sorted(str(p) for p in query_params if p is not None)
            issues.append(
                ComplianceIssue(
                    model=model.name,
                    severity="info",
                    category="query_param",
                    message=f"Searchable column '{col}' not in spec query params",
                    details=f"Available query params: {', '.join(sorted_params[:10])}...",
                )
            )

    return issues


def run_compliance_check(
    spec_path: str, models_dir: str = "src/clearskies_snyk/models", verbose: bool = False
) -> list[ComplianceIssue]:
    """Run the full compliance check."""
    print(f"Loading spec from: {spec_path}")
    spec = load_spec(spec_path)

    print(f"Extracting models from: {models_dir}")
    models = extract_models(models_dir)
    print(f"  Found {len(models)} models")

    print("Extracting endpoints from spec...")
    endpoints = extract_endpoints(spec)
    print(f"  Found {len(endpoints)} unique endpoint paths")

    print("Extracting schemas from spec...")
    schemas = extract_schemas(spec)
    print(f"  Found {len(schemas)} schemas")

    all_issues: list[ComplianceIssue] = []

    print("\nChecking model compliance...")
    for model_name, model in sorted(models.items()):
        if verbose:
            print(f"\n  Checking {model_name}...")
            print(f"    destination: {model.destination_name}")
            print(f"    columns: {len(model.columns)}")

        # Check endpoint exists
        issues = check_endpoint_exists(model, endpoints)
        all_issues.extend(issues)

        # Check column coverage
        issues = check_column_coverage(model, endpoints, schemas)
        all_issues.extend(issues)

        # Check query parameters
        issues = check_query_parameters(model, endpoints)
        all_issues.extend(issues)

    return all_issues


def print_report(issues: list[ComplianceIssue]) -> bool:
    """Print a compliance report and return success status."""
    print("\n" + "=" * 70)
    print("COMPLIANCE REPORT")
    print("=" * 70)

    # Group by severity
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    infos = [i for i in issues if i.severity == "info"]

    print(f"\nSummary:")
    print(f"  ❌ Errors:   {len(errors)}")
    print(f"  ⚠️  Warnings: {len(warnings)}")
    print(f"  ℹ️  Info:     {len(infos)}")

    if errors:
        print("\n" + "-" * 70)
        print("ERRORS")
        print("-" * 70)
        for issue in errors:
            print(f"\n❌ [{issue.model}] {issue.message}")
            if issue.details:
                print(f"   {issue.details}")

    if warnings:
        print("\n" + "-" * 70)
        print("WARNINGS")
        print("-" * 70)
        for issue in warnings:
            print(f"\n⚠️  [{issue.model}] {issue.message}")
            if issue.details:
                print(f"   {issue.details}")

    if infos:
        print("\n" + "-" * 70)
        print("INFO")
        print("-" * 70)
        for issue in infos:
            print(f"\nℹ️  [{issue.model}] {issue.message}")

    print("\n" + "=" * 70)

    if errors:
        print("❌ COMPLIANCE CHECK FAILED")
        return False
    elif warnings:
        print("⚠️  COMPLIANCE CHECK PASSED WITH WARNINGS")
        return True
    else:
        print("✅ COMPLIANCE CHECK PASSED")
        return True


def main() -> int:
    """Run the compliance check script."""
    parser = argparse.ArgumentParser(description="Check model compliance with OpenAPI spec")
    parser.add_argument(
        "--spec",
        default="api_spec/v2-rest-api-spec.json",
        help="Path to the OpenAPI spec (JSON or YAML)",
    )
    parser.add_argument(
        "--models-dir",
        default="src/clearskies_snyk/models",
        help="Path to the models directory",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose output",
    )

    args = parser.parse_args()

    issues = run_compliance_check(args.spec, args.models_dir, args.verbose)
    success = print_report(issues)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
