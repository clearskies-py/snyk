"""Snyk Integration model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have a direct
equivalent endpoint for integrations at the organization level.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykIntegration(Model):
    """
    Model for Snyk Integrations (v1 API).

    This model represents integrations in a Snyk organization (e.g., GitHub, GitLab, etc.).
    Uses the Snyk v1 API endpoint: /org/{orgId}/integrations

    ```python
    import clearskies
    from clearskies_snyk.models import SnykIntegration


    def my_handler(snyk_integration: SnykIntegration):
        # Fetch all integrations for an organization
        integrations = snyk_integration.where("org_id=org-id-123")
        for integration in integrations:
            print(f"Integration: {integration.integration_type}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'integration_type' to avoid shadowing Python's builtin type
    backend = SnykV1Backend(
        api_to_model_map={
            "type": "integration_type",
        },
        can_delete=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations"

    """
    The unique identifier for the integration.
    """
    id = String()

    """
    The ID of the organization this integration belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The type of integration (e.g., github, gitlab, bitbucket).
    """
    integration_type = String()

    """
    Credentials for the integration (only used during creation).
    """
    credentials = Json()
