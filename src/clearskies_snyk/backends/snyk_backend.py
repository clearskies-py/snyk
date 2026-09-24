"""Snyk REST API backend for clearskies v2."""

from typing import Any

import clearskies
from clearskies import configs, di
from clearskies.authentication import Authentication
from clearskies.backends.adapters import (
    BodyCountAdapter,
    CountAdapter,
    PaginationAdapter,
    ResponseAdapter,
    UrlAdapter,
)
from clearskies.decorators import parameters_to_properties
from clearskies.di import inject
from clearskies.query import Query

from clearskies_snyk.backends.adapters import (
    SnykCursorPaginationAdapter,
    SnykJsonApiResponseAdapter,
    SnykVersionUrlAdapter,
)


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
            "next": "/rest/orgs?starting_after=abc123&version=2026-03-25"
        }
    }
    ```

    The backend automatically handles extracting pagination data and provides the next page
    information to clearskies for seamless iteration through results.

    ## API Version

    The Snyk REST API requires a version parameter. By default, this is set to "2026-03-25".
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

    The backend will add `org_id: "org-123"` to the flattened record (the `organization`
    relationship is mapped to the `org` prefix; other relationships become `{name}_id`).

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
        api_version: str = "2026-03-25",
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
        response_adapter: ResponseAdapter | None = None,
        pagination_adapter: PaginationAdapter | None = None,
        count_adapter: CountAdapter | None = None,
        url_adapter: UrlAdapter | None = None,
    ):
        if response_adapter is None:
            self.response_adapter = SnykJsonApiResponseAdapter()
        if pagination_adapter is None:
            self.pagination_adapter = SnykCursorPaginationAdapter(
                pagination_parameter_name=pagination_parameter_name,
            )
        if count_adapter is None:
            self.count_adapter = BodyCountAdapter(count_path="meta.count")
        self.finalize_and_validate_configuration()
        # Create url_adapter after finalize so self.api_version / self.base_url are resolved.
        if url_adapter is None:
            self.url_adapter = SnykVersionUrlAdapter(
                base_url=self.base_url,
                api_version=self.api_version,
            )

    def count(self, query: Query) -> "clearskies.query.result.CountQueryResult":
        """
        Return the total count of records matching the query.

        Delegates to ``records()`` which extracts ``meta.count`` from the response body
        via :class:`~clearskies_snyk.backends.adapters.SnykJsonApiResponseAdapter`.
        Raises ``ValueError`` if the endpoint does not return ``meta.count``
        (most Snyk endpoints don't; override ``build_records_request`` to inject
        ``count=true`` for endpoints that support it).
        """
        from clearskies.query.result import CountQueryResult

        result = self.records(query)
        if result.total_count is None:
            raise ValueError(
                "The Snyk API endpoint did not return a 'meta.count' field. "
                "Only endpoints that explicitly support counting (e.g. "
                "/orgs/{org_id}/targets) can be used with count operations."
            )
        return CountQueryResult(count=result.total_count)

    def pagination_to_request_parameters(self, query: Query) -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Add pagination parameters and the required version parameter.

        The Snyk REST API requires a `version` parameter on all requests.
        """
        url_parameters, body_parameters = super().pagination_to_request_parameters(query)
        url_parameters["version"] = self.api_version
        return (url_parameters, body_parameters)

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

    def map_update_request(self, id: int | str, data: dict[str, Any], model: clearskies.Model) -> dict[str, Any]:
        """
        Map update data to JSON:API format required by Snyk REST API.

        The Snyk REST API expects:
        {"data": {"attributes": {...}, "id": "...", "relationships": {}, "type": "..."}}
        """
        resource_type = self._get_resource_type(model)

        attributes = {}
        for k, v in data.items():
            if k.endswith("_id") and k != "id":
                continue
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
        """
        resource_type = self._get_resource_type(model)
        return {"data": {"type": resource_type, "attributes": data}}

    def _get_resource_type(self, model: clearskies.Model) -> str:
        """Infer the JSON:API resource type from the model's destination_name."""
        if self.resource_type:
            return self.resource_type
        if model and hasattr(model, "destination_name"):
            destination = model.destination_name()
            parts = destination.split("/")
            resource_name = parts[-1]
            if resource_name.endswith("s") and len(resource_name) > 1:
                return resource_name[:-1]
            return resource_name
        return "resource"

    def get_update_headers(self) -> dict[str, str]:
        return self.headers

    def get_create_headers(self) -> dict[str, str]:
        return self.headers

    def get_delete_headers(self) -> dict[str, str]:
        return self.headers
