"""Snyk Group Settings model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
a direct equivalent for group settings management.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Integer, Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykGroupSettings(Model):
    """
    Model for Snyk Group Settings (v1 API).

    This model represents settings for a Snyk group, including session
    length and request access configuration.

    Uses the Snyk v1 API endpoint: /group/{groupId}/settings

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykGroupSettings

    # Get settings for a group
    settings = SnykGroupSettings().find("group-id-123")
    print(f"Session length: {settings.session_length} minutes")
    print(f"Request access enabled: {settings.request_access_enabled}")

    # Update settings
    settings.session_length = 60
    settings.save()
    ```

    ## Settings

    - `session_length`: Session timeout in minutes (1-43200, default 43200 = 30 days)
    - `request_access`: Whether users can request access to orgs in the group

    ## Required Permissions

    - Admin access to the group
    - Edit access to request access settings (for updating request_access)
    """

    id_column_name: str = "group_id"
    backend = SnykV1Backend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "group/{group_id}/settings"

    """
    The ID of the group these settings belong to.
    """
    group_id = String(is_searchable=True)

    """
    The session length for the group in minutes.
    Must be between 1 and 43200 (30 days).
    Setting to null inherits from global default of 30 days.
    """
    session_length = Integer()

    """
    Request access settings for the group.
    Contains 'enabled' boolean field.
    """
    request_access = Json()

    """
    Whether users can request access to Snyk orgs in this group
    that they are not a member of.
    """
    request_access_enabled = Boolean()
