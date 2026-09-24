"""Snyk version URL adapter — appends ?version= to write/delete URLs."""

from __future__ import annotations

from collections.abc import Mapping

from clearskies import configs, decorators
from clearskies.backends.adapters import UrlAdapter


class SnykVersionUrlAdapter(UrlAdapter):
    """
    URL adapter for the Snyk REST API that appends ``?version=`` to create/update/delete URLs.

    Records (and count) URLs receive their ``version`` parameter through
    ``SnykBackend.pagination_to_request_parameters`` instead, which keeps the version
    alongside the other query parameters.

    ``SnykBackend`` wires this adapter by default.  If you pass your own ``url_adapter``,
    subclass this one (or append ``version`` yourself): otherwise write requests will be
    sent without the version parameter and rejected by the Snyk API.

    ```python
    backend = SnykBackend(
        url_adapter=SnykVersionUrlAdapter(
            base_url="https://api.snyk.io/rest/",
            api_version="2026-03-25",
        )
    )
    ```
    """

    api_version = configs.String(default="2026-03-25")

    @decorators.parameters_to_properties
    def __init__(self, base_url: str = "", url_suffix: str = "", api_version: str = "2026-03-25"):
        self.finalize_and_validate_configuration()

    def finalize_url(
        self,
        url: str,
        available_routing_data: Mapping[str, str | int],
        operation: str,
    ) -> tuple[str, list[str]]:
        """Build URL via parent, then append ``?version=`` for write/delete operations."""
        final_url, used = super().finalize_url(url, available_routing_data, operation)

        # Records (and count, which reuses records_url) get version from pagination_to_request_parameters.
        if operation == "records":
            return (final_url, used)

        separator = "&" if "?" in final_url else "?"
        return (f"{final_url}{separator}version={self.api_version}", used)
