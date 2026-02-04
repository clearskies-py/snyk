"""Snyk Self App model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykSelfApp(Model):
    """
    Model for Snyk Self Apps.

    This model represents apps installed by the current user.
    Uses the Snyk v2 REST API endpoint: /self/apps

    ```python
    from clearskies_snyk.models import SnykSelfApp

    # List apps installed by the current user
    apps = SnykSelfApp()
    for app in apps:
        print(f"App: {app.name}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'app_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(api_to_model_map={
            "type": "app_type",
        }, can_create=False, can_update=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "self/apps"

    """
    The unique identifier for the app (client_id).
    """
    id = String()

    """
    The type of resource (app).
    """
    app_type = String()

    """
    The name of the app.
    """
    name = String()

    """
    The client ID of the app.
    """
    client_id = String()

    """
    The redirect URIs for the app.
    """
    redirect_uris = Json()

    """
    The scopes granted to the app.
    """
    scopes = Json()

    """
    The access token TTL in seconds.
    """
    access_token_ttl_seconds = String()

    """
    The date the app was created.
    """
    created_at = Datetime()

    """
    The date the app was last updated.
    """
    updated_at = Datetime()
