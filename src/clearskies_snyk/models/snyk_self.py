"""Snyk Self model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Select, String

from clearskies_snyk.backends import SnykBackend


class SnykSelf(Model):
    """
    Model for Snyk Self (Current User).

    This model represents the current authenticated user or service account
    making the API request.

    Uses the Snyk v2 REST API endpoint: /self

    ```python
    from clearskies_snyk.models import SnykSelf

    # Get the current user
    self_user = SnykSelf().find("id=self")
    print(f"Current user: {self_user.name} ({self_user.email})")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "self"

    """
    The unique identifier for the user/service account.
    """
    id = String()

    """
    The type of principal (user, service_account, or app_instance).
    """
    principal_type = Select(
        allowed_values=[
            "user",
            "service_account",
            "app_instance",
        ],
    )

    """
    The name of the user or service account.
    """
    name = String()

    """
    The email of the user (only for user type).
    """
    email = String()

    """
    The username of the user (only for user type).
    """
    username = String()

    """
    The avatar URL of the user (only for user type).
    """
    avatar_url = String()

    """
    The default organization context ID.
    """
    default_org_context = String()
