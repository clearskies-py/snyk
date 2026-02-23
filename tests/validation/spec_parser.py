"""Parse OpenAPI specification for testing purposes."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class EndpointInfo:
    """Information about an API endpoint extracted from the OpenAPI spec."""

    path: str
    method: str
    operation_id: str
    tags: list[str] = field(default_factory=list)
    parameters: list[dict[str, Any]] = field(default_factory=list)
    request_body: dict[str, Any] | None = None
    responses: dict[str, Any] = field(default_factory=dict)
    required_headers: dict[str, str] = field(default_factory=dict)
    summary: str = ""
    description: str = ""


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    valid: bool
    errors: list[str] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.valid = False
        self.errors.append(error)


class SpecParser:
    """Parse OpenAPI spec and extract testing data."""

    def __init__(self, spec_path: Path):
        """
        Initialize the parser with an OpenAPI spec file.

        Args:
            spec_path: Path to the OpenAPI spec JSON file
        """
        self.spec_path = spec_path
        self.spec = self._load_spec(spec_path)

    def _load_spec(self, spec_path: Path) -> dict[str, Any]:
        """Load the OpenAPI spec from a file."""
        if not spec_path.exists():
            raise FileNotFoundError(f"OpenAPI spec not found at {spec_path}")

        with open(spec_path) as f:
            return json.load(f)

    def get_all_endpoints(self) -> list[EndpointInfo]:
        """Get all endpoints from the spec."""
        endpoints = []
        paths = self.spec.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() in ["GET", "POST", "PATCH", "DELETE", "PUT"]:
                    if isinstance(details, dict):
                        endpoints.append(self._parse_endpoint(path, method.upper(), details))

        return endpoints

    def get_endpoints_for_operation(self, operation: str) -> list[EndpointInfo]:
        """
        Get all endpoints that support an operation (GET, POST, PATCH, DELETE).

        Args:
            operation: HTTP method (GET, POST, PATCH, DELETE)

        Returns:
            List of endpoint information for endpoints supporting the operation
        """
        all_endpoints = self.get_all_endpoints()
        return [ep for ep in all_endpoints if ep.method == operation.upper()]

    def get_endpoints_by_tag(self, tag: str) -> list[EndpointInfo]:
        """
        Get all endpoints with a specific tag.

        Args:
            tag: The tag to filter by

        Returns:
            List of endpoint information for endpoints with the tag
        """
        all_endpoints = self.get_all_endpoints()
        return [ep for ep in all_endpoints if tag in ep.tags]

    def _parse_endpoint(self, path: str, method: str, details: dict[str, Any]) -> EndpointInfo:
        """Parse an endpoint from the spec."""
        # Extract basic information
        operation_id = details.get("operationId", "")
        tags = details.get("tags", [])
        summary = details.get("summary", "")
        description = details.get("description", "")
        parameters = details.get("parameters", [])

        # Extract request body schema if present
        request_body = None
        request_body_spec = details.get("requestBody", {})
        if request_body_spec:
            content = request_body_spec.get("content", {})
            json_api_content = content.get("application/vnd.api+json", {})
            if json_api_content:
                request_body = json_api_content.get("schema", {})

        # Extract response schemas
        responses = details.get("responses", {})

        # Extract required headers from parameters
        required_headers = self._extract_required_headers(parameters)

        return EndpointInfo(
            path=path,
            method=method,
            operation_id=operation_id,
            tags=tags,
            parameters=parameters,
            request_body=request_body,
            responses=responses,
            required_headers=required_headers,
            summary=summary,
            description=description,
        )

    def _extract_required_headers(self, parameters: list[dict[str, Any]]) -> dict[str, str]:
        """Extract required headers from parameter list."""
        headers = {}
        for param in parameters:
            if param.get("in") == "header" and param.get("required", False):
                name = param.get("name", "")
                # Try to get example or default value
                schema = param.get("schema", {})
                example = param.get("example") or schema.get("example") or schema.get("default", "")
                if name:
                    headers[name] = str(example) if example else ""
        return headers

    def get_required_headers(self, path: str, method: str) -> dict[str, str]:
        """
        Extract required headers from spec for a specific endpoint.

        Args:
            path: The API path (e.g., "/orgs/{org_id}/projects")
            method: HTTP method (GET, POST, etc.)

        Returns:
            Dictionary of required headers
        """
        paths = self.spec.get("paths", {})
        if path in paths:
            methods = paths[path]
            if method.lower() in methods:
                details = methods[method.lower()]
                parameters = details.get("parameters", [])
                return self._extract_required_headers(parameters)
        return {}

    def get_request_schema(self, path: str, method: str) -> dict[str, Any] | None:
        """
        Get JSON schema for request body.

        Args:
            path: The API path
            method: HTTP method

        Returns:
            Request body schema or None if not applicable
        """
        paths = self.spec.get("paths", {})
        if path in paths:
            methods = paths[path]
            if method.lower() in methods:
                details = methods[method.lower()]
                request_body = details.get("requestBody", {})
                if request_body:
                    content = request_body.get("content", {})
                    json_api_content = content.get("application/vnd.api+json", {})
                    if json_api_content:
                        return json_api_content.get("schema", {})
        return None

    def get_response_schema(self, path: str, method: str, status: int = 200) -> dict[str, Any] | None:
        """
        Get JSON schema for response body.

        Args:
            path: The API path
            method: HTTP method
            status: HTTP status code (default: 200)

        Returns:
            Response body schema or None if not found
        """
        paths = self.spec.get("paths", {})
        if path in paths:
            methods = paths[path]
            if method.lower() in methods:
                details = methods[method.lower()]
                responses = details.get("responses", {})
                status_response = responses.get(str(status), {})
                if status_response:
                    content = status_response.get("content", {})
                    json_api_content = content.get("application/vnd.api+json", {})
                    if json_api_content:
                        return json_api_content.get("schema", {})
        return None

    def validate_request_body(self, path: str, method: str, body: dict[str, Any]) -> bool:
        """
        Validate request body against schema.

        Args:
            path: The API path
            method: HTTP method
            body: The request body to validate

        Returns:
            True if valid, False otherwise
        """
        schema = self.get_request_schema(path, method)
        if not schema:
            # No schema means no validation required
            return True

        # Basic validation - check if it's a dict with 'data' key for JSON:API
        if not isinstance(body, dict):
            return False

        # For JSON:API format, expect 'data' key
        if "data" not in body:
            return False

        return True

    def get_endpoint_by_path_and_method(self, path: str, method: str) -> EndpointInfo | None:
        """
        Get endpoint info for a specific path and method.

        Args:
            path: The API path
            method: HTTP method

        Returns:
            EndpointInfo or None if not found
        """
        all_endpoints = self.get_all_endpoints()
        for endpoint in all_endpoints:
            if endpoint.path == path and endpoint.method == method.upper():
                return endpoint
        return None
