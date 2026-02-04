"""Snyk Organization model for v1 API."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykOrgV1(Model):
    """
    Model representing a Snyk Organization from the v1 API.

    The v1 API returns organizations with a different structure than the REST API,
    including a nested `group` object.

    ## Usage

    ```python
    from clearskies_snyk.models import SnykOrgV1

    # Get all organizations
    for org in SnykOrgV1.all():
        print(f"{org.name} ({org.slug})")

    # Get a specific organization by ID
    org = SnykOrgV1.find("org-id-123")
    ```

    ## API Endpoint

    - GET /v1/orgs - List all organizations
    - GET /v1/org/{orgId} - Get a specific organization
    """

    id_column_name: str = "id"

    backend = SnykV1Backend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the API endpoint path for organizations."""
        return "orgs"

    id = String()
    name = String()
    slug = String()
    url = String()
    group = Json()
