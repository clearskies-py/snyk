"""Snyk-specific JSON:API response adapter."""

from __future__ import annotations

from typing import Any

from clearskies.backends.adapters import JsonApiResponseAdapter


class SnykJsonApiResponseAdapter(JsonApiResponseAdapter):
    """
    JSON:API response adapter for the Snyk REST API.

    Extends :class:`~clearskies.backends.adapters.JsonApiResponseAdapter` to
    additionally promote relationship IDs into flat ``{name}_id`` fields.

    The stock adapter intentionally drops ``relationships`` because they are
    not part of the column-mapping layer.  The Snyk REST API uses relationships
    to express foreign keys, so we need to pull them out:

    ```json
    {
        "data": [{
            "id": "proj-1",
            "type": "project",
            "attributes": {"name": "my-repo"},
            "relationships": {
                "organization": {"data": {"id": "org-abc", "type": "org"}}
            }
        }]
    }
    ```

    becomes:

    ```python
    {"id": "proj-1", "type": "project", "name": "my-repo", "org_id": "org-abc"}
    ```

    The ``_RELATIONSHIP_NAME_MAP`` maps Snyk relationship names to the model
    column prefix used for the ``_id`` field (e.g. ``"organization"`` →
    ``"org"`` so the field becomes ``"org_id"`` not ``"organization_id"``).
    """

    _RELATIONSHIP_NAME_MAP: dict[str, str] = {
        "organization": "org",
    }

    def extract_records(self, response_data: Any) -> list[dict[str, Any]] | None:
        """
        Return a flattened list of records from a JSON:API ``data`` envelope.

        Handles all JSON:API data shapes:
        - ``{"data": [...]}`` → flattened list
        - ``{"data": {...}}`` → single-element list (for ``find()`` calls)
        - ``{"data": null}``  → empty list

        Returns ``None`` for responses that don't have a ``data`` key, handing
        control back to the built-in ``ApiBackend`` extraction logic.
        """
        if not isinstance(response_data, dict):
            return None
        if "data" not in response_data:
            return None
        data = response_data["data"]
        if data is None:
            return []
        if isinstance(data, list):
            return [self._normalize_record(item) for item in data]
        if isinstance(data, dict):
            return [self._normalize_record(data)]
        return None

    def _normalize_record(self, data_block: dict[str, Any]) -> dict[str, Any]:
        """Flatten JSON:API resource object and extract relationship IDs."""
        normalized = super()._normalize_record(data_block)

        relationships = data_block.get("relationships", {})
        if not isinstance(relationships, dict):
            return normalized

        for rel_name, rel_data in relationships.items():
            if not isinstance(rel_data, dict):
                continue
            rel_inner = rel_data.get("data", {})
            if isinstance(rel_inner, dict) and "id" in rel_inner:
                mapped = self._RELATIONSHIP_NAME_MAP.get(rel_name, rel_name)
                normalized[f"{mapped}_id"] = rel_inner["id"]

        return normalized
