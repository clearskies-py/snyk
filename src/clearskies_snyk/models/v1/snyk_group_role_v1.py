"""Snyk Group Role model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API has a different
structure for roles.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykV1Backend


class SnykGroupRoleV1(Model):
    """
    Model for Snyk Group Roles (v1 API).

    This model represents roles available in a Snyk group. Roles define
    permissions that can be assigned to users within the group.

    Uses the Snyk v1 API endpoint: /group/{groupId}/roles

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykGroupRoleV1

    # Fetch all roles for a group
    roles = SnykGroupRoleV1().where("group_id=group-id-123")
    for role in roles:
        print(f"Role: {role.name} - {role.description}")
    ```

    ## Common Roles

    - `Org Collaborator`: Basic collaborator access
    - `Org Admin`: Full administrative access

    ## Required Permissions

    - READ access to the group
    """

    id_column_name: str = "public_id"
    backend = SnykV1Backend(
        api_to_model_map={
            "publicId": "public_id",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "group/{group_id}/roles"

    """
    The unique public identifier for the role.
    """
    public_id = String()

    """
    The ID of the group this role belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The name of the role (e.g., 'Org Collaborator', 'Org Admin').
    """
    name = String()

    """
    A description of the role's permissions.
    """
    description = String()

    """
    The timestamp when the role was created (ISO-8601 format).
    """
    created = String()

    """
    The timestamp when the role was last modified (ISO-8601 format).
    """
    modified = String()
