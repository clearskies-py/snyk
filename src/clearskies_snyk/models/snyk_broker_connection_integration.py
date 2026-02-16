"""Snyk Broker Connection Integration model."""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykBackend


class SnykBrokerConnectionIntegration(Model):
    """
    Model for Snyk Broker Connection Integrations.

    This model represents integrations using a broker connection.
    It shows which org integrations are using a specific broker connection.

    Uses the Snyk v2 REST API endpoint:
    `/tenants/{tenant_id}/brokers/connections/{connection_id}/integrations`

    ```python
    import clearskies
    from clearskies_snyk.models import SnykBrokerConnectionIntegration


    def my_handler(snyk_broker_connection_integration: SnykBrokerConnectionIntegration):
        # Fetch all integrations for a broker connection
        integrations = snyk_broker_connection_integration.where(
            "tenant_id=tenant-id-123", "connection_id=conn-id-456"
        )
        for integration in integrations:
            print(f"Integration: {integration.id} - Type: {integration.integration_type}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "tenants/{tenant_id}/brokers/connections/{connection_id}/integrations"

    """
    The unique identifier for the integration.
    """
    id = String()

    """
    The ID of the tenant.
    """
    tenant_id = String(is_searchable=True)

    """
    The ID of the broker connection.
    """
    connection_id = String(is_searchable=True)

    """
    The ID of the organization using this integration.
    """
    org_id = String()

    """
    The type of integration (e.g., github, gitlab).
    """
    integration_type = String()
