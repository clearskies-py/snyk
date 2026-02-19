"""Snyk Membership Backend for clearskies v2."""

from typing import Any

import clearskies

from clearskies_snyk.backends import SnykBackend


class SnykMembershipBackend(SnykBackend):
    """
    Specialized backend for Snyk membership resources (group and org memberships).

    This backend extends [`SnykBackend`](snyk_backend.py) to handle the unique JSON:API structure
    used by membership endpoints, where data is sent in `relationships` instead of `attributes`.

    ## Why This Backend Exists

    Unlike most Snyk REST API resources that use the standard JSON:API format with attributes:
    ```json
    {
      "data": {
        "type": "project",
        "attributes": { "name": "...", "slug": "..." }
      }
    }
    ```

    Membership resources use relationships exclusively:
    ```json
    {
      "data": {
        "type": "org_membership",
        "relationships": {
          "user": { "data": { "id": "...", "type": "user" }},
          "role": { "data": { "id": "...", "type": "org_role" }},
          "org": { "data": { "id": "...", "type": "org" }}
        }
      }
    }
    ```

    ## Usage

    This backend is automatically configured for membership models:

    ```python
    from clearskies_snyk.backends import SnykMembershipBackend
    from clearskies_snyk.models import SnykGroupMembership, SnykOrgMembership

    # Used internally by SnykGroupMembership and SnykOrgMembership models
    backend = SnykMembershipBackend(resource_type="membership")
    ```

    ## Key Differences from Standard Backend

    1. **Create Operations**: Builds relationships structure with user, role, and org/group
    2. **Update Operations**: Only sends role relationship (memberships can only change roles)
    3. **Dynamic Types**: Automatically determines org vs group context and sets appropriate types
       - `org_membership` vs `group_membership`
       - `org_role` vs `group_role`

    ## Supported Operations

    - **Create**: Add a user to an organization or group with a specific role
    - **Update**: Change a user's role within an organization or group
    - **Delete**: Remove a user's membership
    - **Query**: List and filter memberships (handled by parent [`SnykBackend`](snyk_backend.py))
    """

    def map_create_request(self, data: dict[str, Any], model: "clearskies.Model") -> dict[str, Any]:  # type: ignore
        """
        Map create data to JSON:API format with relationships for memberships.

        Memberships don't use the standard `attributes` structure. Instead, they send
        all data as relationships (user, role, and org/group).

        Args:
            data: Dictionary containing user_id, role_id, and either org_id or group_id
            model: The model instance (used to determine destination type)

        Returns:
            JSON:API formatted request body with relationships structure

        Example:
            ```python
            # Input data for org membership
            {"user_id": "abc-123", "role_id": "def-456", "org_id": "ghi-789"}

            # Output format
            {
                "data": {
                    "type": "org_membership",
                    "relationships": {
                        "user": {"data": {"id": "abc-123", "type": "user"}},
                        "role": {"data": {"id": "def-456", "type": "org_role"}},
                        "org": {"data": {"id": "ghi-789", "type": "org"}},
                    },
                }
            }
            ```
        """
        # Determine if this is an org or group membership
        is_org = "org_id" in data and data["org_id"]
        membership_type = "org_membership" if is_org else "group_membership"
        role_type = "org_role" if is_org else "group_role"

        # Build the relationships structure
        relationships = {
            "user": {"data": {"id": data.get("user_id"), "type": "user"}},
            "role": {"data": {"id": data.get("role_id"), "type": role_type}},
        }

        # Add org or group relationship based on context
        if is_org:
            relationships["org"] = {"data": {"id": data.get("org_id"), "type": "org"}}
        else:
            # For group memberships, use group_id
            relationships["group"] = {"data": {"id": data.get("group_id"), "type": "group"}}

        return {"data": {"type": membership_type, "relationships": relationships}}

    def map_update_request(self, id: int | str, data: dict[str, Any], model: "clearskies.Model") -> dict[str, Any]:  # type: ignore
        """
        Map update data to JSON:API format with relationships for memberships.

        Membership updates only allow changing the role. The request includes an empty
        `attributes` object (required by the API) and only the role relationship.

        Args:
            id: The membership ID being updated
            data: Dictionary containing the new role_id (and possibly org_id/group_id for context)
            model: The model instance being updated

        Returns:
            JSON:API formatted request body with relationships structure

        Example:
            ```python
            # Input data
            {
                "role_id": "new-role-456",
                "org_id": "ghi-789",  # for context
            }

            # Output format
            {
                "data": {
                    "type": "org_membership",
                    "id": "membership-123",
                    "attributes": {},  # Required but empty
                    "relationships": {"role": {"data": {"id": "new-role-456", "type": "org_role"}}},
                }
            }
            ```
        """
        # Determine membership type from model data
        # Check if this is an org or group membership
        is_org = "org_id" in data and data["org_id"]
        if not is_org and hasattr(model, "org_id"):
            # Fallback: check if model has org_id attribute set
            is_org = bool(getattr(model, "org_id", None))

        membership_type = "org_membership" if is_org else "group_membership"
        role_type = "org_role" if is_org else "group_role"

        return {
            "data": {
                "type": membership_type,
                "id": str(id),
                "attributes": {},  # Required by the API but must be empty
                "relationships": {
                    "role": {"data": {"id": data.get("role_id"), "type": role_type}},
                },
            }
        }
