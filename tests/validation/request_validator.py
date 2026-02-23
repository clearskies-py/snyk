"""Validate HTTP requests against OpenAPI spec."""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlparse

from tests.validation.spec_parser import SpecParser, ValidationResult


class RequestValidator:
    """Validate HTTP requests against OpenAPI spec."""

    def __init__(self, spec_parser: SpecParser):
        """
        Initialize the validator with a spec parser.

        Args:
            spec_parser: SpecParser instance to use for validation
        """
        self.spec_parser = spec_parser

    def validate_headers(self, path: str, method: str, headers: dict[str, str]) -> ValidationResult:
        """
        Validate request headers match spec requirements.

        Args:
            path: The API path
            method: HTTP method
            headers: Headers sent with the request

        Returns:
            ValidationResult indicating success or failure
        """
        result = ValidationResult(valid=True)

        # Ensure headers is a dict
        if not isinstance(headers, dict):
            result.add_error(f"Headers must be a dictionary, got {type(headers).__name__}")
            return result

        # Get required headers from spec
        required_headers = self.spec_parser.get_required_headers(path, method)

        # Check if all required headers are present
        for header_name, expected_value in required_headers.items():
            if header_name not in headers:
                result.add_error(f"Missing required header: {header_name}")

        # For Snyk REST API, check for JSON:API headers
        if "Accept" not in headers:
            result.add_error("Missing required header: Accept")
        elif headers["Accept"] != "application/vnd.api+json":
            result.add_error(f"Invalid Accept header: expected 'application/vnd.api+json', got '{headers['Accept']}'")

        # For POST/PATCH requests, validate Content-Type
        if method.upper() in ["POST", "PATCH", "PUT"]:
            if "Content-Type" not in headers:
                result.add_error("Missing required header: Content-Type for POST/PATCH request")
            elif headers["Content-Type"] != "application/vnd.api+json":
                result.add_error(
                    f"Invalid Content-Type header: expected 'application/vnd.api+json', got '{headers['Content-Type']}'"
                )

        result.details["required_headers"] = required_headers
        result.details["provided_headers"] = headers

        return result

    def validate_method(self, path: str, method: str) -> ValidationResult:
        """
        Validate HTTP method is allowed for endpoint.

        Args:
            path: The API path
            method: HTTP method to validate

        Returns:
            ValidationResult indicating success or failure
        """
        result = ValidationResult(valid=True)

        # Get endpoint info
        endpoint = self.spec_parser.get_endpoint_by_path_and_method(path, method)

        if endpoint is None:
            result.add_error(f"Endpoint {method.upper()} {path} not found in spec")
            result.details["path"] = path
            result.details["method"] = method
        else:
            result.details["endpoint"] = endpoint

        return result

    def validate_url(
        self, url: str, expected_path: str | None = None, required_params: list[str] | None = None
    ) -> ValidationResult:
        """
        Validate URL construction and parameters.

        Args:
            url: The full URL to validate
            expected_path: Expected path component (optional)
            required_params: List of required query parameters (optional)

        Returns:
            ValidationResult indicating success or failure
        """
        result = ValidationResult(valid=True)
        required_params = required_params or []

        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)

        # Check for version parameter (required for Snyk REST API)
        if "version" not in query_params:
            result.add_error("Missing required query parameter: version")

        # Check for other required parameters
        for param in required_params:
            if param not in query_params:
                result.add_error(f"Missing required query parameter: {param}")

        # Validate path if expected_path provided
        if expected_path:
            if not parsed.path.endswith(expected_path) and expected_path not in parsed.path:
                result.add_error(f"URL path does not contain expected path: {expected_path}")

        result.details["url"] = url
        result.details["path"] = parsed.path
        result.details["query_params"] = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}

        return result

    def validate_body(self, path: str, method: str, body: dict[str, Any]) -> ValidationResult:
        """
        Validate request body against schema.

        Args:
            path: The API path
            method: HTTP method
            body: Request body to validate

        Returns:
            ValidationResult indicating success or failure
        """
        result = ValidationResult(valid=True)

        # Skip validation for methods that don't have request bodies
        if method.upper() not in ["POST", "PATCH", "PUT"]:
            return result

        # Get request schema from spec
        schema = self.spec_parser.get_request_schema(path, method)

        if not schema:
            # No schema defined, but we should still validate JSON:API format
            if not isinstance(body, dict):
                result.add_error("Request body must be a dictionary")
            elif "data" not in body:
                result.add_error("Request body must contain 'data' key (JSON:API format)")
        else:
            # Validate JSON:API format
            if not isinstance(body, dict):
                result.add_error("Request body must be a dictionary")
            elif "data" not in body:
                result.add_error("Request body must contain 'data' key (JSON:API format)")
            else:
                data = body["data"]
                if not isinstance(data, dict):
                    result.add_error("Request body 'data' must be a dictionary")
                else:
                    # Check for required JSON:API fields
                    if "type" not in data:
                        result.add_error("Request body 'data' must contain 'type' field")

                    # For POST requests, attributes should be present
                    if method.upper() == "POST":
                        if "attributes" not in data:
                            result.add_error("Request body 'data' must contain 'attributes' for POST requests")

                    # For PATCH requests, id should be present
                    if method.upper() == "PATCH":
                        if "id" not in data:
                            result.add_error("Request body 'data' must contain 'id' for PATCH requests")

        result.details["schema"] = schema
        result.details["body"] = body

        return result

    def validate_request(
        self,
        url: str,
        method: str,
        headers: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
        expected_path: str | None = None,
    ) -> ValidationResult:
        """
        Validate a complete HTTP request.

        Args:
            url: The full URL
            method: HTTP method
            headers: Request headers
            body: Request body
            expected_path: Expected path component

        Returns:
            ValidationResult indicating success or failure
        """
        result = ValidationResult(valid=True)
        headers = headers or {}
        body = body or {}

        # Parse URL to get path
        parsed = urlparse(url)
        path_to_check = expected_path or parsed.path

        # Remove base URL if present
        if path_to_check.startswith("https://") or path_to_check.startswith("http://"):
            path_to_check = parsed.path

        # Remove /rest/ prefix if present
        if path_to_check.startswith("/rest/"):
            path_to_check = path_to_check[6:]  # Remove "/rest/"

        # Validate method
        method_result = self.validate_method(path_to_check, method)
        if not method_result.valid:
            result.valid = False
            result.errors.extend(method_result.errors)

        # Validate headers
        headers_result = self.validate_headers(path_to_check, method, headers)
        if not headers_result.valid:
            result.valid = False
            result.errors.extend(headers_result.errors)

        # Validate URL
        url_result = self.validate_url(url, expected_path)
        if not url_result.valid:
            result.valid = False
            result.errors.extend(url_result.errors)

        # Validate body
        if body:
            body_result = self.validate_body(path_to_check, method, body)
            if not body_result.valid:
                result.valid = False
                result.errors.extend(body_result.errors)

        result.details["url"] = url
        result.details["method"] = method
        result.details["headers"] = headers
        result.details["body"] = body

        return result
