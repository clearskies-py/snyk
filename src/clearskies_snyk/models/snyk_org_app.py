"""Snyk Org App model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykOrgApp(Model):
    """
    Model for Snyk Organization Apps.

    This model represents Snyk Apps registered within an organization.
    Apps are integrations that can access Snyk APIs on behalf of users.

    Uses the Snyk v2 REST API endpoint: `/orgs/{org_id}/apps`

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgApp


    def my_handler(snyk_org_app: SnykOrgApp):
        # Fetch all apps for an org
        apps = snyk_org_app.where("org_id=org-id-123")
        for app in apps:
            print(f"App: {app.name} - Client ID: {app.client_id}")
    ```
    """

    id_column_name: str = "client_id"

    backend = SnykBackend(resource_type="app")

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/apps"

    """
    The client ID of the app (primary identifier).
    """
    client_id = String()

    """
    The ID of the organization this app belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The name of the app.
    """
    name = String()

    """
    The redirect URIs for OAuth flow.
    """
    redirect_uris = Json()

    """
    The scopes requested by the app.
    """
    scopes = Json()

    """
    Whether the app is public.
    """
    is_public = Boolean()

    """
    The access token TTL in seconds.
    """
    access_token_ttl_seconds = String()

    """
    Timestamp of when the app was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the app was last updated.
    """
    updated_at = Datetime()
