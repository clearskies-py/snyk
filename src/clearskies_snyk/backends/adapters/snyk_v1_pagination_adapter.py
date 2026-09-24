"""Snyk v1 page-based pagination adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from clearskies import configs, decorators
from clearskies.backends.adapters import ParameterPaginationAdapter

if TYPE_CHECKING:
    from clearskies.query import Query
    from requests import Response as RequestsResponse


V1_WRAPPER_KEYS = ("orgs", "projects", "snapshots", "members", "integrations", "results")


def extract_v1_records(body: Any) -> list[Any] | None:
    """
    Extract the record list from a Snyk v1 response body.

    Handles direct lists, known wrapper keys (``{"orgs": [...]}`` etc.) and generic
    single-key wrappers.  Returns ``None`` when no list is found (e.g. a single-record dict).
    """
    if isinstance(body, list):
        return body
    if not isinstance(body, dict):
        return None
    for key in V1_WRAPPER_KEYS:
        if isinstance(body.get(key), list):
            return body[key]
    if len(body) == 1:
        (first_value,) = body.values()
        if isinstance(first_value, list):
            return first_value
    return None


class SnykV1PaginationAdapter(ParameterPaginationAdapter):
    """
    Page-based pagination adapter for the Snyk v1 API.

    Extends :class:`~clearskies.backends.adapters.ParameterPaginationAdapter` with v1-aware record
    extraction.  The stock adapter checks for more pages via ``body.get("data", body)``, which doesn't
    work for the v1 envelope format (``{"orgs": [...]}`` etc.), so this subclass uses
    :func:`extract_v1_records` for the "are there more pages?" guard.
    """

    pagination_parameter_name = configs.String(default="page")
    start_value = configs.Integer(default=1)
    step = configs.Integer(default=1)

    @decorators.parameters_to_properties
    def __init__(
        self,
        pagination_parameter_name: str = "page",
        start_value: int = 1,
        step: int = 1,
    ):
        self.finalize_and_validate_configuration()

    def extract_next_page_data(
        self,
        response: RequestsResponse,
        query: Query,
    ) -> dict[str, Any]:
        """Increment the page number unless the response had no records or fewer than the limit."""
        if not response.content:
            return {}
        try:
            body = response.json()
        except Exception:
            return {}

        records = extract_v1_records(body)
        if not records:
            # No list (single record / unknown shape) or an empty page: nothing more to fetch.
            return {}
        if query.limit and len(records) < int(query.limit):
            return {}

        current = query.pagination.get(self.pagination_parameter_name, self.start_value)
        try:
            return {self.pagination_parameter_name: int(current) + self.step}
        except (ValueError, TypeError):
            return {}
