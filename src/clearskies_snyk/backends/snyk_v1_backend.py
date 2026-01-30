"""Snyk v1 API backend for clearskies v2."""

from typing import Any

import clearskies
import requests
from clearskies import configs
from clearskies.authentication import Authentication
from clearskies.decorators import parameters_to_properties
from clearskies.di import inject
from clearskies.query import Query


class SnykV1Backend(clearskies.backends.ApiBackend):
    """
    Backend for interacting with the Snyk v1 API.

    This backend extends the ApiBackend to provide seamless integration with the Snyk platform's
    legacy v1 API. It handles the specific response format and pagination used by Snyk v1 APIs.

    The v1 API uses camelCase field names (automatically converted to snake_case) and returns
    responses with various wrapper keys like `orgs`, `projects`, etc.

    ## Usage

    The SnykV1Backend is typically used with models that represent Snyk entities available
    through the v1 API:

    ```python
    import clearskies
    from clearskies_snyk.backends import SnykV1Backend


    class SnykOrgV1(clearskies.Model):
        backend = SnykV1Backend()

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
    backend = SnykV1Backend(
        authentication=clearskies.authentication.SecretBearer(
            environment_key="SNYK_API_KEY",
            header_prefix="token ",
        )
    )
    ```

    ## Response Format

    The Snyk v1 API returns responses in various formats depending on the endpoint:

    - `{"orgs": [...]}` for organization lists
    - `{"projects": [...]}` for project lists
    - `{"snapshots": [...]}` for project history
    - Direct list `[...]` for some endpoints
    - Single object `{...}` for single record endpoints

    This backend automatically handles these variations.

    ## Pagination

    The Snyk v1 API uses offset-based pagination with `page` and `perPage` parameters.
    """

    base_url = configs.String(default="https://api.snyk.io/v1/")
    authentication = inject.ByName("snyk_auth")  # type: ignore[assignment]
    requests = inject.Requests()

    # v1 API uses camelCase, models use snake_case
    model_casing = configs.Select(["snake_case", "camelCase", "TitleCase"], default="snake_case")
    api_casing = configs.Select(["snake_case", "camelCase", "TitleCase"], default="camelCase")

    api_to_model_map = configs.AnyDict(default={})
    pagination_parameter_name = configs.String(default="page")
    limit_parameter_name = configs.String(default="perPage")
    headers = configs.StringDict(default={"Content-Type": "application/json"})

    can_count = False

    @parameters_to_properties
    def __init__(
        self,
        base_url: str | None = "https://api.snyk.io/v1/",
        authentication: Authentication | None = None,
        model_casing: str = "snake_case",
        api_casing: str = "camelCase",
        api_to_model_map: dict[str, str | list[str]] | None = None,
        pagination_parameter_name: str = "page",
        pagination_parameter_type: str = "int",
        limit_parameter_name: str = "perPage",
    ):
        self.finalize_and_validate_configuration()

    def map_records_response(
        self, response_data: Any, query: Query, query_data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Map the Snyk v1 API response to model fields.

        The Snyk v1 API returns responses in various formats:

        - `{"orgs": [...]}` for organization lists
        - `{"projects": [...]}` for project lists
        - `{"snapshots": [...]}` for project history
        - Direct list `[...]` for some endpoints
        - Single object `{...}` for single record endpoints

        This method extracts the records from these various formats and passes them
        to the parent class for casing conversion and mapping.
        """
        if isinstance(response_data, dict):
            # Check for known wrapper keys
            for wrapper_key in ["orgs", "projects", "snapshots", "members", "integrations", "results"]:
                if wrapper_key in response_data and isinstance(response_data[wrapper_key], list):
                    return super().map_records_response(response_data[wrapper_key], query, query_data)

            # Check if the first key contains a list (generic wrapper detection)
            if len(response_data) == 1:
                first_key = next(iter(response_data))
                if isinstance(response_data[first_key], list):
                    return super().map_records_response(response_data[first_key], query, query_data)

            # Single record response - let parent handle it
            # Parent will check if it looks like a record based on columns

        return super().map_records_response(response_data, query, query_data)

    def get_next_page_data_from_response(
        self,
        query: Query,
        response: "requests.Response",  # type: ignore
    ) -> dict[str, Any]:
        """
        Extract pagination data from the Snyk v1 API response.

        The Snyk v1 API uses offset-based pagination. This method checks if there are
        more records available based on the response size and returns the next page number.
        """
        next_page_data: dict[str, Any] = {}

        response_data = response.json() if response.content else {}

        # Get current page from query or default to 1
        current_page = 1
        if query.pagination.get(self.pagination_parameter_name):
            current_page = int(query.pagination.get(self.pagination_parameter_name))

        # Get the limit (perPage) from query or default
        limit = query.limit or 100

        # Extract records to check count
        records = self._extract_records_from_response(response_data)

        # If we got a full page, there might be more
        if len(records) >= limit:
            next_page_data[self.pagination_parameter_name] = current_page + 1

        return next_page_data

    def _extract_records_from_response(self, response_data: Any) -> list[Any]:
        """Extract the list of records from the response for pagination checking."""
        if isinstance(response_data, list):
            return response_data

        if isinstance(response_data, dict):
            for wrapper_key in ["orgs", "projects", "snapshots", "members", "integrations", "results"]:
                if wrapper_key in response_data and isinstance(response_data[wrapper_key], list):
                    return response_data[wrapper_key]

            if len(response_data) == 1:
                first_key = next(iter(response_data))
                if isinstance(response_data[first_key], list):
                    return response_data[first_key]

        return []
