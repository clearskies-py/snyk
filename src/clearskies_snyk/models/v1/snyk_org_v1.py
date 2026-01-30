"""Snyk Organization model for v1 API."""

import clearskies

from clearskies_snyk.models.v1.snyk_v1_model import SnykV1Model


class SnykOrgV1(SnykV1Model):
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

    @classmethod
    def destination_name(cls) -> str:
        """Return the API endpoint path for organizations."""
        return "orgs"

    name = clearskies.columns.String()
    slug = clearskies.columns.String()
    url = clearskies.columns.String()
    group = clearskies.columns.Json()
