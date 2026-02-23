"""Generate test fixtures from OpenAPI spec."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import Mock

from tests.validation.spec_parser import EndpointInfo, SpecParser


@dataclass
class TestCase:
    """A test case for an endpoint."""

    endpoint: EndpointInfo
    test_name: str
    test_data: dict[str, Any]
    expected_result: Any | None = None


class SpecTestFixtures:
    """Generate test data from OpenAPI spec."""

    def __init__(self, spec_parser: SpecParser | None = None):
        """
        Initialize the fixtures generator.

        Args:
            spec_parser: Optional SpecParser instance. If not provided, will create one
                        using the default spec path.
        """
        if spec_parser is None:
            # Default to v2 REST API spec
            spec_path = Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"
            spec_parser = SpecParser(spec_path)

        self.spec_parser = spec_parser

    def generate_request_data(self, endpoint: EndpointInfo) -> dict[str, Any]:
        """
        Generate valid request data from schema.

        Args:
            endpoint: Endpoint information

        Returns:
            Dictionary containing valid request data
        """
        # For JSON:API format, create a data structure
        data: dict[str, Any] = {
            "data": {
                "type": self._infer_resource_type(endpoint.path),
                "attributes": {},
            }
        }

        # Add sample attributes based on common Snyk fields
        if endpoint.method in ["POST", "PATCH"]:
            data["data"]["attributes"] = self._generate_sample_attributes(endpoint)

        # For PATCH, include the ID
        if endpoint.method == "PATCH":
            data["data"]["id"] = "test-id-123"
            data["data"]["relationships"] = {}

        return data

    def generate_response_data(self, endpoint: EndpointInfo) -> dict[str, Any]:
        """
        Generate valid response data from schema.

        Args:
            endpoint: Endpoint information

        Returns:
            Dictionary containing valid response data
        """
        resource_type = self._infer_resource_type(endpoint.path)

        # For list endpoints
        if endpoint.method == "GET" and not endpoint.path.endswith("}"):
            return {
                "data": [
                    {
                        "id": "test-id-1",
                        "type": resource_type,
                        "attributes": self._generate_sample_attributes(endpoint),
                    },
                    {
                        "id": "test-id-2",
                        "type": resource_type,
                        "attributes": self._generate_sample_attributes(endpoint),
                    },
                ],
                "links": {
                    "next": f"/rest/{endpoint.path}?starting_after=abc123&version=2025-11-05",
                },
            }

        # For single resource endpoints
        return {
            "data": {
                "id": "test-id-123",
                "type": resource_type,
                "attributes": self._generate_sample_attributes(endpoint),
            }
        }

    def _infer_resource_type(self, path: str) -> str:
        """
        Infer the JSON:API resource type from the path.

        Args:
            path: API path (e.g., "orgs/{org_id}/projects")

        Returns:
            Singular resource type (e.g., "project")
        """
        # Take the last segment
        parts = path.split("/")
        resource_name = parts[-1].replace("{", "").replace("}", "")

        # Skip parameter names like {id}, {project_id}, etc.
        if resource_name.endswith("_id") or resource_name == "id":
            if len(parts) > 1:
                resource_name = parts[-2]

        # Simple singularization: remove trailing 's'
        if resource_name.endswith("s") and len(resource_name) > 1:
            return resource_name[:-1]

        return resource_name

    def _generate_sample_attributes(self, endpoint: EndpointInfo) -> dict[str, Any]:
        """
        Generate sample attributes based on endpoint type.

        Args:
            endpoint: Endpoint information

        Returns:
            Dictionary of sample attributes
        """
        # Common attributes for various Snyk resources
        attributes: dict[str, Any] = {}

        resource_type = self._infer_resource_type(endpoint.path)

        # Add common attributes based on resource type
        if resource_type in ["org", "organization"]:
            attributes = {
                "name": "Test Organization",
                "slug": "test-org",
                "is_personal": False,
            }
        elif resource_type == "group":
            attributes = {
                "name": "Test Group",
            }
        elif resource_type == "project":
            attributes = {
                "name": "Test Project",
                "origin": "github",
                "status": "active",
            }
        elif resource_type == "target":
            attributes = {
                "display_name": "Test Target",
                "is_private": False,
            }
        elif resource_type == "collection":
            attributes = {
                "name": "Test Collection",
            }
        else:
            # Generic attributes
            attributes = {
                "name": f"Test {resource_type.title()}",
            }

        return attributes

    def get_all_create_endpoints(self) -> list[EndpointInfo]:
        """
        Get all endpoints that support CREATE (POST).

        Returns:
            List of endpoint information for POST endpoints
        """
        return self.spec_parser.get_endpoints_for_operation("POST")

    def get_all_update_endpoints(self) -> list[EndpointInfo]:
        """
        Get all endpoints that support UPDATE (PATCH).

        Returns:
            List of endpoint information for PATCH endpoints
        """
        return self.spec_parser.get_endpoints_for_operation("PATCH")

    def get_all_delete_endpoints(self) -> list[EndpointInfo]:
        """
        Get all endpoints that support DELETE.

        Returns:
            List of endpoint information for DELETE endpoints
        """
        return self.spec_parser.get_endpoints_for_operation("DELETE")

    def get_all_read_endpoints(self) -> list[EndpointInfo]:
        """
        Get all endpoints that support READ (GET).

        Returns:
            List of endpoint information for GET endpoints
        """
        return self.spec_parser.get_endpoints_for_operation("GET")

    def get_all_endpoints(self) -> list[EndpointInfo]:
        """
        Get all endpoints from the spec.

        Returns:
            List of all endpoint information
        """
        return self.spec_parser.get_all_endpoints()

    def get_test_cases_for_endpoint(self, endpoint: EndpointInfo) -> list[TestCase]:
        """
        Generate all test cases for an endpoint.

        Args:
            endpoint: Endpoint information

        Returns:
            List of test cases
        """
        test_cases = []

        # Header validation test
        test_cases.append(
            TestCase(
                endpoint=endpoint,
                test_name=f"test_{endpoint.method.lower()}_headers_{endpoint.operation_id}",
                test_data=self.generate_request_data(endpoint),
            )
        )

        # URL validation test
        test_cases.append(
            TestCase(
                endpoint=endpoint,
                test_name=f"test_{endpoint.method.lower()}_url_{endpoint.operation_id}",
                test_data=self.generate_request_data(endpoint),
            )
        )

        # Body validation test (for POST/PATCH)
        if endpoint.method in ["POST", "PATCH"]:
            test_cases.append(
                TestCase(
                    endpoint=endpoint,
                    test_name=f"test_{endpoint.method.lower()}_body_{endpoint.operation_id}",
                    test_data=self.generate_request_data(endpoint),
                )
            )

        return test_cases

    def create_mock_model(self, endpoint: EndpointInfo, **kwargs: Any) -> Mock:
        """
        Create a mock model for testing.

        Args:
            endpoint: Endpoint information
            **kwargs: Additional attributes to set on the mock

        Returns:
            Mock model instance
        """
        model = Mock()
        model.destination_name.return_value = endpoint.path
        model.get_raw_data.return_value = {}
        model.id_column_name = "id"

        # Set any additional attributes
        for key, value in kwargs.items():
            setattr(model, key, value)

        return model

    def get_endpoints_for_models(self, model_names: list[str]) -> list[EndpointInfo]:
        """
        Get endpoints relevant to specific models.

        Args:
            model_names: List of model names (e.g., ["orgs", "projects"])

        Returns:
            List of endpoint information
        """
        all_endpoints = self.get_all_endpoints()
        relevant_endpoints = []

        for endpoint in all_endpoints:
            for model_name in model_names:
                if model_name in endpoint.path:
                    relevant_endpoints.append(endpoint)
                    break

        return relevant_endpoints
