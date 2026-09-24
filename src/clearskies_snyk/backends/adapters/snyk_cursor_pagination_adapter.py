"""Snyk REST API cursor-based pagination adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qs, urlparse

from clearskies import configs, decorators
from clearskies.backends.adapters import PaginationAdapter

if TYPE_CHECKING:
    from clearskies.query import Query
    from requests import Response as RequestsResponse


class SnykCursorPaginationAdapter(PaginationAdapter):
    """
    Cursor-based pagination adapter for the Snyk REST API.

    Snyk embeds the next-page cursor in the response body (not a ``Link``
    header), so the default ``LinkHeaderPaginationAdapter`` cannot be used.

    Response body shape:

    ```json
    {
        "data": [...],
        "links": {
            "next": "/rest/orgs?starting_after=abc123&version=2024-10-15"
        }
    }
    ```

    The adapter parses ``links.next``, extracts the ``starting_after`` query
    parameter and returns it as the pagination data for the next request.
    Returns an empty dict when ``links.next`` is absent or empty, signalling
    no further pages.
    """

    pagination_parameter_name = configs.String(default="starting_after")

    @decorators.parameters_to_properties
    def __init__(self, pagination_parameter_name: str = "starting_after"):
        self.finalize_and_validate_configuration()

    def extract_next_page_data(
        self,
        response: "RequestsResponse",
        query: "Query",
    ) -> dict[str, Any]:
        """Extract the cursor value from ``links.next`` in the response body."""
        if not response.content:
            return {}
        try:
            body = response.json()
        except Exception:
            return {}

        if not isinstance(body, dict):
            return {}

        links = body.get("links", {})
        if not isinstance(links, dict):
            return {}

        next_url = links.get("next", "")
        if not next_url:
            return {}

        parsed = urlparse(next_url)
        params = parse_qs(parsed.query)
        cursor = params.get(self.pagination_parameter_name, [None])[0]

        if cursor:
            return {self.pagination_parameter_name: cursor}
        return {}
