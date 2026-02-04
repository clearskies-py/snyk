"""Snyk REST API backend for clearskies v2."""

from typing import Any

import clearskies
import requests
from clearskies import configs
from clearskies.authentication import Authentication
from clearskies.decorators import parameters_to_properties
from clearskies.di import inject
from clearskies.query import Query


class SnykBackend(clearskies.backends.ApiBackend):
    """
    Backend for interacting with the Snyk REST API.

    This backend extends the ApiBackend to provide seamless integration with the Snyk platform.
    It handles the specific pagination and response format used by Snyk REST APIs, where pagination
    uses cursor-based navigation with `starting_after` parameter.

    The Snyk REST API uses JSON:API format, so responses have a `data` key containing records
    with `id`, `type`, and `attributes` fields. This backend automatically flattens these
    into a simple dictionary format expected by clearskies models.

    ## Usage

    The SnykBackend is typically used with models that represent Snyk entities:

    ```python
    import clearskies
    from clearskies_snyk.backends import SnykBackend


    class SnykOrg(clearskies.Model):
        backend = SnykBackend()

        @classmethod
        def destination_name(cls) -> str:
            return "orgs"

        id = clearskies.columns.String()
        name = clearskies.columns.String()
        slug = clearskies.columns.String()
    ```

    ## Authentication

    By default, the backend uses the `snyk_auth` binding for authentication, which should be
    configured in your application's dependency injection container. You can also provide a custom
    authentication instance:

    ```python
    backend = SnykBackend(
        authentication=clearskies.authentication.SecretBearer(
            environment_key="SNYK_API_KEY",
            header_prefix="token ",
        )
    )
    ```

    ## Pagination

    The Snyk REST API uses cursor-based pagination with the following response format:

    ```json
    {
        "data": [...],
        "links": {
            "next": "/rest/orgs?starting_after=abc123&version=2024-10-15"
        }
    }
    ```

    The backend automatically handles extracting pagination data and provides the next page
    information to clearskies for seamless iteration through results.

    ## API Version

    The Snyk REST API requires a version parameter. By default, this is set to "2024-10-15".
    You can override this by setting the `api_version` parameter.

    ## Relationship Mapping

    The backend automatically extracts relationship IDs from JSON:API relationships.
    For example, if a record has:

    ```json
    {
        "relationships": {
            "organization": {
                "data": {"id": "org-123", "type": "org"}
            }
        }
    }
    ```

    The backend will add `organization_id: "org-123"` to the flattened record.
    """

    base_url = configs.String(default="https://api.snyk.io/rest/")
    api_version = configs.String(default="2025-11-05")
    authentication = inject.ByName("snyk_auth")  # type: ignore[assignment]
    requests = inject.Requests()
    api_casing = configs.Select(["snake_case", "camelCase", "TitleCase"], default="snake_case")
    api_to_model_map = configs.AnyDict(default={})
    pagination_parameter_name = configs.String(default="starting_after")
    limit_parameter_name = configs.String(default="limit")
    headers = configs.StringDict(default={"Accept": "application/vnd.api+json"})

    can_count = False

    @parameters_to_properties
    def __init__(
        self,
        base_url: str | None = "https://api.snyk.io/rest/",
        api_version: str = "2025-11-05",
        authentication: Authentication | None = None,
        model_casing: str = "snake_case",
        api_casing: str = "snake_case",
        api_to_model_map: dict[str, str | list[str]] | None = None,
        pagination_parameter_name: str = "starting_after",
        pagination_parameter_type: str = "str",
        limit_parameter_name: str = "limit",
        can_create: bool | None = True,
        can_update: bool | None = True,
        can_delete: bool | None = True,
        can_query: bool | None = True,
    ):
        self.finalize_and_validate_configuration()

    def pagination_to_request_parameters(self, query: Query) -> tuple[dict[str, str], dict[str, Any]]:
        """
        Add pagination parameters and the required version parameter.

        The Snyk REST API requires a `version` parameter on all requests.
        """
        url_parameters, body_parameters = super().pagination_to_request_parameters(query)
        url_parameters["version"] = self.api_version
        return (url_parameters, body_parameters)

    def map_records_response(
        self, response_data: Any, query: Query, query_data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Map the Snyk REST API response to model fields.

        The Snyk REST API returns responses in JSON:API format where the actual records
        are nested within a `data` key. Each record has `id`, `type`, and `attributes`.

        This method extracts the `data` list and flattens each record by merging
        the `id` with the `attributes`, and also extracts relationship IDs.
        """
        if isinstance(response_data, dict):
            data = response_data.get("data", [])
            if isinstance(data, list):
                flattened_records = []
                for record in data:
                    flattened_records.append(self._flatten_json_api_record(record))
                return super().map_records_response(flattened_records, query, query_data)
            elif isinstance(data, dict):
                # Single record response
                return super().map_records_response([self._flatten_json_api_record(data)], query, query_data)
        return super().map_records_response(response_data, query, query_data)

    def _flatten_json_api_record(self, record: dict[str, Any]) -> dict[str, Any]:
        """Flatten a JSON:API record into a simple dictionary."""
        if not isinstance(record, dict):
            return record

        flattened: dict[str, Any] = {"id": record.get("id")}

        # Extract attributes
        attributes = record.get("attributes", {})
        if isinstance(attributes, dict):
            flattened.update(attributes)

        # Extract relationship IDs
        relationships = record.get("relationships", {})
        if isinstance(relationships, dict):
            for rel_name, rel_data in relationships.items():
                if isinstance(rel_data, dict):
                    rel_data_inner = rel_data.get("data", {})
                    if isinstance(rel_data_inner, dict):
                        # Map common relationship names
                        mapped_name = self._map_relationship_name(rel_name)
                        flattened[f"{mapped_name}_id"] = rel_data_inner.get("id")

        return flattened

    def _map_relationship_name(self, rel_name: str) -> str:
        """Map JSON:API relationship names to model column names."""
        # Common mappings for Snyk API
        relationship_map = {
            "organization": "org",
        }
        return relationship_map.get(rel_name, rel_name)

    def get_next_page_data_from_response(
        self,
        query: Query,
        response: "requests.Response",  # type: ignore
    ) -> dict[str, Any]:
        """
        Extract pagination data from the Snyk REST API response.

        The Snyk REST API includes pagination information in the response body under `links`:

        - `links.next`: URL for the next page of results (contains `starting_after` parameter)

        This method parses the next URL to extract the `starting_after` cursor value.
        """
        next_page_data: dict[str, Any] = {}

        response_data = response.json() if response.content else {}

        if isinstance(response_data, dict):
            links = response_data.get("links", {})
            if isinstance(links, dict):
                next_url = links.get("next", "")
                if next_url:
                    from urllib.parse import parse_qs, urlparse

                    parsed = urlparse(next_url)
                    params = parse_qs(parsed.query)
                    starting_after = params.get("starting_after", [None])[0]
                    if starting_after:
                        next_page_data[self.pagination_parameter_name] = starting_after

        return next_page_data
