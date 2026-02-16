"""Snyk Group User model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_group_reference


class SnykGroupUser(Model):
    """
    Model for Snyk Group Users.

    This model represents users within a Snyk group.
    Supports updating a user's role in a group.

    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/users/{id}

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupUser


    def my_handler(snyk_group_user: SnykGroupUser):
        # Get a specific user in a group
        user = snyk_group_user.where("group_id=group-id-123").find("id=user-id-456")
        print(f"User: {user.id}")

        # Access the parent group
        print(f"Group: {user.group.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_delete=False, can_query=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/users"

    """
    The unique identifier for the user.
    """
    id = String()

    """
    The ID of the group this user belongs to.
    """
    group_id = BelongsToId(
        snyk_group_reference.SnykGroupReference,
        is_searchable=True,
    )

    """
    The parent group this user belongs to.

    BelongsTo relationship to SnykGroup.
    """
    group = BelongsToModel("group_id")

    """
    The membership details including role.
    """
    membership = Json()
