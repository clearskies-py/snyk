"""Snyk Broker Deployment model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykBackend


class SnykBrokerDeployment(Model):
    """
    Model for Snyk Broker Deployments.

    This model represents broker deployments for a tenant.
    Broker deployments are instances of the Snyk Broker that connect
    to private resources.

    Uses the Snyk v2 REST API endpoint: `/tenants/{tenant_id}/brokers/deployments`

    ```python
    from clearskies_snyk.models import SnykBrokerDeployment

    # Fetch all broker deployments for a tenant
    deployments = SnykBrokerDeployment().where("tenant_id=tenant-id-123")
    for deployment in deployments:
        print(f"Deployment: {deployment.id}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "tenants/{tenant_id}/brokers/deployments"

    """
    The unique identifier for the broker deployment.
    """
    id = String()

    """
    The ID of the tenant this deployment belongs to.
    """
    tenant_id = String(is_searchable=True)

    """
    The install ID associated with this deployment.
    """
    install_id = String()

    """
    The org ID where the broker app is installed.
    """
    broker_app_installed_in_org_id = String()

    """
    Metadata information such as user/org id or metrics.
    """
    metadata = Json()
