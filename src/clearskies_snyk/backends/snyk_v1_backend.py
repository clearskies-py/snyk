"""Snyk v1 API backend for clearskies v2."""

from typing import Any

import clearskies
from clearskies import configs
from clearskies.authentication import Authentication
from clearskies.backends.adapters import PaginationAdapter
from clearskies.decorators import parameters_to_properties
from clearskies.di import inject
from clearskies.query import Query

from clearskies_snyk.backends.adapters import SnykV1PaginationAdapter, extract_v1_records


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

    This backend automatically handles these variations via ``map_records_response``.

    ## Pagination

    The Snyk v1 API uses offset-based pagination with `page` and `perPage` parameters,
    handled automatically by
    :class:`~clearskies_snyk.backends.adapters.SnykV1PaginationAdapter`.
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
        can_create: bool | None = True,
        can_update: bool | None = True,
        can_delete: bool | None = True,
        can_query: bool | None = True,
        pagination_adapter: PaginationAdapter | None = None,
    ):
        # Wire v1 page-based pagination adapter as default when not overridden by caller.
        if pagination_adapter is None:
            self.pagination_adapter = SnykV1PaginationAdapter(
                pagination_parameter_name=pagination_parameter_name,
            )
        self.finalize_and_validate_configuration()

    def map_records_response(
        self, response_data: Any, query: Query, query_data: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Map the Snyk v1 API response to model fields.

        The Snyk v1 API returns responses in various formats:

        - ``{"orgs": [...]}`` for organization lists
        - ``{"projects": [...]}`` for project lists
        - ``{"snapshots": [...]}`` for project history
        - Direct list ``[...]`` for some endpoints
        - Single object ``{...}`` for single record endpoints

        Known wrapper keys are unwrapped before delegating to the parent.
        Single-record dicts fall through to the parent's column-aware detection.
        """
        records = extract_v1_records(response_data)
        return super().map_records_response(response_data if records is None else records, query, query_data)
