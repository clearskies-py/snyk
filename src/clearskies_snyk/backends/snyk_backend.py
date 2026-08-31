"""Snyk REST API backend for clearskies v2."""

from typing import Any

import clearskies
import requests
from clearskies import configs, di
from clearskies.authentication import Authentication
from clearskies.decorators import parameters_to_properties
from clearskies.di import inject
from clearskies.query import Query
from clearskies.query.result import CountQueryResult
from requests import Response


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

    ## JSON:API Resource Type

    When creating or updating records, the backend needs to know the JSON:API resource type
    (e.g., "project", "org", etc.). By default, it will try to infer this from the model's
    destination_name by taking the last path segment and singularizing it. However, you can
    explicitly set this using the `resource_type` parameter:

    ```python
    backend = SnykBackend(resource_type="project")
    ```
    """

    base_url = configs.String(default="https://api.snyk.io/rest/")
    api_version = configs.String(default="2026-03-25")
    authentication = inject.ByName("snyk_auth")  # type: ignore[assignment]
    requests = inject.Requests()
    api_casing = configs.Select(["snake_case", "camelCase", "TitleCase"], default="snake_case")
    api_to_model_map = configs.AnyDict(default={})
    pagination_parameter_name = configs.String(default="starting_after")
    limit_parameter_name = configs.String(default="limit")
    headers = configs.StringDict(
        default={"Accept": "application/vnd.api+json", "Content-Type": "application/vnd.api+json"}
    )
    resource_type = configs.String(default="")

    can_count = True

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
        headers: dict[str, str] | None = None,
        update_headers: dict[str, str] | None = None,
        create_headers: dict[str, str] | None = None,
        delete_headers: dict[str, str] | None = None,
        records_headers: dict[str, str] | None = None,
        resource_type: str = "",
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

    def records(self, query: Query) -> Any:
        """
        Fetch records and populate total_count from ``meta.count`` if present.

        Some Snyk endpoints (e.g. ``/orgs/{org_id}/projects``) always include
        ``meta.count`` in the response.  Others (e.g. ``/orgs/{org_id}/targets``)
        include it only when ``count=true`` is sent.  Either way, if the field is
        present we pass it as ``total_count`` to ``RecordsQueryResult`` so that
        ``len()`` works without a second round-trip.
        """
        from clearskies.query.result import RecordsQueryResult

        self.check_query(query)
        url, method, body, headers = self.build_records_request(query)
        response = self.execute_request(url, method, json=body, headers=headers)
        response_data = response.json() if response.content else {}
        records = self.map_records_response(response_data, query)
        next_page_data = self.get_next_page_data_from_response(query, response)

        total_count = None
        if isinstance(response_data, dict):
            meta = response_data.get("meta", {})
            if isinstance(meta, dict) and "count" in meta:
                try:
                    total_count = int(meta["count"])
                except (TypeError, ValueError):
                    pass

        return RecordsQueryResult(
            records=records,
            next_page_data=next_page_data or None,
            total_count=total_count,
        )

    def map_records_response(
        self, response_data: Any, query: Query, query_data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Map the Snyk REST API response to model fields.

        The Snyk REST API returns responses in JSON:API format where the actual records
        are nested within a `data` key. Each record has `id`, `type`, and `attributes`.

        This method extracts the `data` list and flattens each record by merging
        the `id` with the `attributes`, and also extracts relationship IDs.

        The parent ApiBackend.map_records_response() will call check_dict_and_map_to_model()
        on each record, which merges query_data into the record using {**query_data, **mapped}.
        """
        if isinstance(response_data, dict):
            data = response_data.get("data", [])
            if isinstance(data, list):
                flattened_records = []
                for record in data:
                    flattened_records.append(self._flatten_json_api_record(record))
                # Parent will merge query_data into each record via check_dict_and_map_to_model()
                return super().map_records_response(flattened_records, query, query_data)
            elif isinstance(data, dict):
                # Single record response - parent will merge query_data
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

    def conditions_to_request_parameters(
        self, query: Any, used_routing_parameters: list[str]
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        """Serialise boolean URL params as true/false instead of 1/0.

        The Snyk REST API rejects boolean query params that are not the strings
        ``"true"`` or ``"false"``.
        """
        route_id, url_parameters, body_parameters = super().conditions_to_request_parameters(
            query, used_routing_parameters
        )
        boolean_columns = {
            name for name, col in query.model_class.get_columns().items() if col.__class__.__name__ == "Boolean"
        }
        for key in list(url_parameters.keys()):
            col_name = key.replace("-", "_")
            if col_name in boolean_columns:
                url_parameters[key] = "true" if url_parameters[key] in (1, "1", True) else "false"
        return route_id, url_parameters, body_parameters

    def get_next_page_data_from_response(
        self,
        query: Query,
        response: Response,
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

    def count(self, query: Query) -> CountQueryResult:
        """
        Return the total count of records matching the query.

        Calls ``records()`` which extracts ``meta.count`` from the response body.
        Raises ``ValueError`` if the endpoint does not return ``meta.count``
        (most Snyk endpoints don't; override ``build_records_request`` to inject
        ``count=true`` for endpoints that support it).
        """
        result = self.records(query)
        if result.total_count is None:
            raise ValueError(
                f"The Snyk API endpoint did not return a 'meta.count' field. "
                f"Only endpoints that explicitly support counting (e.g. "
                f"/orgs/{{org_id}}/targets) can be used with count operations."
            )
        return CountQueryResult(count=result.total_count)

    def map_update_request(self, id: int | str, data: dict[str, Any], model: clearskies.Model) -> dict[str, Any]:
        """
        Map update data to JSON:API format required by Snyk REST API.

        The Snyk REST API expects:
        {"data": {"attributes": {...}, "id": "...", "relationships": {}, "type": "..."}}

        This hook is called by the ApiBackend.update() method to transform the data before
        sending it to the API.

        Note: Based on working implementation, the Snyk API requires 'type' and an empty
        'relationships' object for PATCH requests on projects.
        """
        import json
        import logging

        resource_type = self._get_resource_type(model)

        # Remove relationship fields (*_id) from attributes - these can't be updated via PATCH
        # Also remove empty string values that should be null or omitted
        attributes = {}
        for k, v in data.items():
            # Skip relationship fields
            if k.endswith("_id") and k != "id":
                continue
            # Skip empty strings for array fields (business_criticality, lifecycle, environment)
            if k in ("business_criticality", "lifecycle", "environment") and v == "":
                continue
            attributes[k] = v

        return {
            "data": {
                "attributes": attributes,
                "id": str(id),
                "relationships": {},
                "type": resource_type,
            }
        }

    def map_create_request(self, data: dict[str, Any], model: clearskies.Model) -> dict[str, Any]:
        """
        Map create data to JSON:API format required by Snyk REST API.

        The Snyk REST API expects: {"data": {"type": "...", "attributes": {...}}}

        This hook is called by the ApiBackend.create() method to transform the data before
        sending it to the API.
        """
        resource_type = self._get_resource_type(model)

        return {
            "data": {
                "type": resource_type,
                "attributes": data,
            }
        }

    def _get_resource_type(self, model: clearskies.Model) -> str:
        """
        Get the JSON:API resource type for a model.

        If resource_type is explicitly set in the backend configuration, use that.
        Otherwise, infer it from the model's destination_name by taking the last
        path segment and singularizing it (e.g., "orgs/{org_id}/projects" -> "project").
        """
        # Use explicitly configured resource type if available
        if self.resource_type:
            return self.resource_type

        # Otherwise, infer from destination_name
        if model and hasattr(model, "destination_name"):
            destination = model.destination_name()
            # Extract the last segment and singularize
            # e.g., "orgs/{org_id}/projects" -> "project"
            parts = destination.split("/")
            resource_name = parts[-1]
            # Simple singularization: remove trailing 's'
            if resource_name.endswith("s") and len(resource_name) > 1:
                return resource_name[:-1]
            return resource_name

        return "resource"

    def _add_version_to_url(self, url: str) -> str:
        """
        Add the API version parameter to a URL if not already present.

        Args:
            url: The URL to add the version parameter to

        Returns:
            The URL with the version parameter added
        """
        if "version=" not in url:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}version={self.api_version}"
        return url

    def update_url(self, id: int | str, data: dict[str, Any], model: clearskies.Model) -> tuple[str, list[str]]:
        """
        Override to add version parameter to update URLs.

        This hook is called by the parent ApiBackend.update() method to build the URL.
        """
        url, used_routing_params = super().update_url(id, data, model)
        return (self._add_version_to_url(url), used_routing_params)

    def create_url(self, data: dict[str, Any], model: clearskies.Model) -> tuple[str, list[str]]:
        """
        Override to add version parameter to create URLs.

        This hook is called by the parent ApiBackend.create() method to build the URL.
        """
        url, used_routing_params = super().create_url(data, model)
        return (self._add_version_to_url(url), used_routing_params)

    def delete_url(self, id: int | str, model: clearskies.Model) -> tuple[str, list[str]]:
        """
        Override to add version parameter to delete URLs.

        This hook is called by the parent ApiBackend.delete() method to build the URL.
        The parent method uses model.data to extract routing parameters.
        """
        url, used_routing_params = super().delete_url(id, model)
        return (self._add_version_to_url(url), used_routing_params)

    def records_url(self, query: Query) -> tuple[str, list[str]]:
        """
        Override to add version parameter to records URLs.

        This hook is called by the parent ApiBackend.records() method to build the URL.
        Note: For records/query operations, the version is already added via
        pagination_to_request_parameters(), so we don't add it again here.
        """
        return super().records_url(query)

    def get_update_headers(self) -> dict[str, str]:
        """Return headers to use for update requests."""
        return self.headers

    def get_create_headers(self) -> dict[str, str]:
        """Return headers to use for create requests."""
        return self.headers

    def get_delete_headers(self) -> dict[str, str]:
        """Return headers to use for delete requests."""
        return self.headers
