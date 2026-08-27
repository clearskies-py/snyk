"""Snyk Broker Connection model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykBrokerConnection(Model):
    """
    Model for Snyk Broker Connections.

    This model represents broker connections integrated with an organization.
    Broker connections allow Snyk to access private repositories and registries.

    Uses the Snyk v2 REST API endpoint: `/orgs/{org_id}/brokers/connections`

    ```python
    import clearskies
    from clearskies_snyk.models import SnykBrokerConnection


    def my_handler(snyk_broker_connection: SnykBrokerConnection):
        # Fetch all broker connections for an org
        connections = snyk_broker_connection.where("org_id=org-id-123")
        for conn in connections:
            print(f"Connection: {conn.name} - Type: {conn.connection_type}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/brokers/connections"

    """
    The unique identifier for the broker connection.
    """
    id = String()

    """
    The ID of the organization this connection belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The name of the broker connection.
    """
    name = String()

    """
    The type of broker connection (e.g., github, gitlab, bitbucket).
    """
    connection_type = String()

    """
    The broker context identifier.
    """
    context = String()

    """
    The associated deployment ID.
    """
    deployment_id = String()

    """
    The identifier for the broker connection.
    """
    identifier = String()

    """
    Secrets associated with the connection.
    """
    secrets = Json()

    """
    Configuration for the connection.
    """
    configuration = Json()

    """
    The encrypted value of the secret.
    """
    encrypted = String()

    """
    Expiry timestamp for the secret.
    """
    expires_at = Datetime()

    """
    Nonce for the secret.
    """
    nonce = String()

    """
    Validation rules for the connection.
    """
    validations = Json()

    """
    Required fields for the connection type.
    """
    required = Json()

    """
    Sonarqube API token (for Sonarqube connections).
    """
    sonarqube_api_token = String()

    """
    Sonarqube host URL (for Sonarqube connections).
    """
    sonarqube_host_url = String()

    """
    Checkmarx configuration (for Checkmarx connections).
    """
    checkmarx = Json()

    """
    Checkmarx username (for Checkmarx connections).
    """
    checkmarx_username = String()

    """
    Checkmarx password (for Checkmarx connections).
    """
    checkmarx_password = String()
