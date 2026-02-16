"""Snyk Org Membership model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgMembership(Model):
    """
    Model for Snyk Organization Memberships.

    This model represents memberships in a Snyk organization.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgMembership


    def my_handler(snyk_org_membership: SnykOrgMembership):
        # Fetch all memberships for an organization
        memberships = snyk_org_membership.where("org_id=org-id-123")
        for membership in memberships:
            print(f"User: {membership.user_id} - Role: {membership.role_id}")

        # Access the parent organization
        print(f"Org: {membership.org_model.name}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'membership_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "membership_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/memberships"

    """
    The unique identifier for the membership.
    """
    id = String()

    """
    The ID of the group.
    """
    group_id = String()

    """
    The ID of the organization this membership belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this membership belongs to.

    BelongsTo relationship to SnykOrg.
    Note: Named 'org_model' to avoid conflict with 'org' Json column.
    """
    org_model = BelongsToModel("org_id")

    """
    User information as JSON object.
    """
    user = Json(is_temporary=True)

    """
    Role information as JSON object.
    """
    role = Json(is_temporary=True)

    """
    Organization information as JSON object.
    """
    org = Json(is_temporary=True)

    """
    The type of membership.
    """
    membership_type = String()

    """
    The ID of the user.
    """
    user_id = String()

    """
    The ID of the role.
    """
    role_id = String()

    """
    Timestamp of when the membership was created.
    """
    created_at = Datetime(is_temporary=True)
