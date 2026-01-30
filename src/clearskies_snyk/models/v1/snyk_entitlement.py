"""Snyk Entitlement model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
entitlement endpoints.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, String

from clearskies_snyk.backends import SnykV1Backend


class SnykEntitlement(Model):
    """
    Model for Snyk Entitlements (v1 API).

    This model represents entitlements (feature flags) for a Snyk organization.
    Entitlements determine which features are available to an organization.

    Uses the Snyk v1 API endpoint: /org/{orgId}/entitlements

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykEntitlement

    # Fetch all entitlements for an organization
    entitlements = SnykEntitlement().where("org_id=org-id-123")
    for entitlement in entitlements:
        print(f"{entitlement.name}: {entitlement.value}")
    ```

    ## Common Entitlements

    - `licenses`: Access to license compliance features
    - `reports`: Access to reporting features
    - `fullVulnDB`: Access to full vulnerability database

    ## Required Permissions

    - `View Organization`
    - `View Entitlements`
    """

    id_column_name: str = "name"
    backend = SnykV1Backend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/entitlements"

    """
    The name of the entitlement (e.g., 'licenses', 'reports', 'fullVulnDB').
    """
    name = String()

    """
    The ID of the organization this entitlement belongs to.
    """
    org_id = String(is_searchable=True)

    """
    Whether the entitlement is enabled for the organization.
    """
    value = Boolean()
