"""Snyk Access Request model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Select, String

from clearskies_snyk.backends import SnykBackend


class SnykAccessRequest(Model):
    """
    Model for Snyk Access Requests.

    This model represents access requests for the current user.
    Uses the Snyk v2 REST API endpoint: /self/access_requests

    ```python
    from clearskies_snyk.models import SnykAccessRequest

    # List access requests for the current user
    requests = SnykAccessRequest()
    for req in requests:
        print(f"Access Request: {req.id} - Status: {req.status}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'request_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "request_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "self/access_requests"

    """
    The unique identifier for the access request.
    """
    id = String()

    """
    The type of resource (access_request).
    """
    request_type = String()

    """
    The status of the access request.
    """
    status = Select(allowed_values=["pending", "expired"])
