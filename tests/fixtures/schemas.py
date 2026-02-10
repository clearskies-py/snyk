"""
Shared schema definitions and helpers for testing.

This module provides utilities for creating JSON:API compliant responses
that match the Snyk REST API format.
"""

from __future__ import annotations

from typing import Any

# JSON:API version used by Snyk
JSONAPI_VERSION: dict[str, str] = {"version": "1.0"}


def make_jsonapi_response(
    data: list[dict[str, Any]] | dict[str, Any],
    links: dict[str, str] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a JSON:API compliant response.

    Args:
        data: The primary data (single resource or list of resources)
        links: Optional pagination/navigation links
        meta: Optional metadata

    Returns:
        A dictionary in JSON:API format
    """
    response: dict[str, Any] = {
        "data": data,
        "jsonapi": JSONAPI_VERSION,
    }
    if links is not None:
        response["links"] = links
    if meta is not None:
        response["meta"] = meta
    return response


def make_resource(
    id: str,
    type: str,
    attributes: dict[str, Any],
    relationships: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a JSON:API resource object.

    Args:
        id: The resource identifier
        type: The resource type (e.g., "org", "project")
        attributes: The resource attributes
        relationships: Optional relationships to other resources

    Returns:
        A dictionary representing a JSON:API resource
    """
    resource: dict[str, Any] = {
        "id": id,
        "type": type,
        "attributes": attributes,
    }
    if relationships is not None:
        resource["relationships"] = relationships
    return resource


def make_relationship(
    id: str,
    type: str,
    links: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create a JSON:API relationship object.

    Args:
        id: The related resource identifier
        type: The related resource type
        links: Optional links for the relationship

    Returns:
        A dictionary representing a JSON:API relationship
    """
    relationship: dict[str, Any] = {"data": {"id": id, "type": type}}
    if links is not None:
        relationship["links"] = links
    return relationship


def make_pagination_links(
    base_url: str,
    starting_after: str | None = None,
    version: str = "2024-10-15",
) -> dict[str, str]:
    """
    Create pagination links for a response.

    Args:
        base_url: The base URL for the endpoint
        starting_after: The cursor for the next page (if any)
        version: The API version

    Returns:
        A dictionary of pagination links
    """
    links: dict[str, str] = {}
    if starting_after:
        links["next"] = f"{base_url}?starting_after={starting_after}&version={version}"
    return links


def make_error_response(
    status: str,
    detail: str,
    title: str | None = None,
    code: str | None = None,
    source: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Create a JSON:API error response.

    Args:
        status: HTTP status code as string
        detail: Human-readable error detail
        title: Optional error title
        code: Optional application-specific error code
        source: Optional source of the error

    Returns:
        A dictionary representing a JSON:API error response
    """
    error: dict[str, Any] = {
        "status": status,
        "detail": detail,
    }
    if title:
        error["title"] = title
    if code:
        error["code"] = code
    if source:
        error["source"] = source

    return {
        "jsonapi": JSONAPI_VERSION,
        "errors": [error],
    }


# Pre-defined error responses for common cases
ERROR_400 = make_error_response(
    status="400",
    detail="Bad Request",
    title="Invalid request",
)

ERROR_401 = make_error_response(
    status="401",
    detail="Unauthorized",
    title="Authentication required",
)

ERROR_403 = make_error_response(
    status="403",
    detail="Forbidden",
    title="Access denied",
)

ERROR_404 = make_error_response(
    status="404",
    detail="Not found",
    title="Resource not found",
)

ERROR_500 = make_error_response(
    status="500",
    detail="Internal server error",
    title="Server error",
)
