"""Snyk Group SSO Connection model."""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykBackend


class SnykGroupSsoConnection(Model):
    """
    Model for Snyk Group SSO Connections.

    This model represents SSO connections at the group level.
    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/sso_connections

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupSsoConnection


    def my_handler(snyk_group_sso_connection: SnykGroupSsoConnection):
        # List SSO connections for a group
        connections = snyk_group_sso_connection.where("group_id=group-id-123")
        for conn in connections:
            print(f"SSO Connection: {conn.name}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'connection_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "connection_type",
        },
        can_create=False,
        can_update=False,
        can_delete=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/sso_connections"

    """
    The unique identifier for the SSO connection.
    """
    id = String()

    """
    The ID of the group this SSO connection belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The type of resource (sso_connection).
    """
    connection_type = String()

    """
    The display name of the SSO connection.
    """
    name = String()
