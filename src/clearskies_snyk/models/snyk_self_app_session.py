"""Snyk Self App Session model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Integer, Json, Select, String

from clearskies_snyk.backends import SnykBackend


class SnykSelfAppSession(Model):
    """
    Model for Snyk Self App Sessions.

    This model represents sessions for apps installed by the current user.
    Uses the Snyk v2 REST API endpoint: /self/apps/{app_id}/sessions

    ```python
    import clearskies
    from clearskies_snyk.models import SnykSelfAppSession


    def my_handler(snyk_self_app_session: SnykSelfAppSession):
        # List sessions for an app
        sessions = snyk_self_app_session.where("app_id=app-id-123")
        for session in sessions:
            print(f"Session: {session.id} created at {session.created_at}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'session_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "session_type",
        },
        can_create=False,
        can_update=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "self/apps/{app_id}/sessions"

    """
    The unique identifier for the session.
    """
    id = String()

    """
    The ID of the app this session belongs to.
    """
    app_id = String(is_searchable=True)

    """
    The type of resource (session).
    """
    session_type = String()

    """
    The date the session was created.
    """
    created_at = Datetime()

    """
    The date the session was last accessed.
    """
    accessed_at = Datetime()

    """
    Access token TTL in seconds.
    """
    access_token_ttl_seconds = Integer()

    """
    Client ID of the app.
    """
    client_id = String()

    """
    Client secret for the app.
    """
    client_secret = String()

    """
    Context scope for the app.
    """
    context = Select(allowed_values=["tenant", "user"])

    """
    OAuth grant type.
    """
    grant_type = Select(allowed_values=["authorization_code", "client_credentials"])

    """
    Whether the app is confidential.
    """
    is_confidential = Boolean()

    """
    Whether the app is public.
    """
    is_public = Boolean()

    """
    Name of the app.
    """
    name = String()

    """
    Public ID of the owning organization.
    """
    org_public_id = String()

    """
    Allowed redirect URIs.
    """
    redirect_uris = Json()

    """
    OAuth scopes for the app.
    """
    scopes = Json()

    """
    Expand related resources.
    """
    expand = String(is_searchable=True, is_temporary=True)
