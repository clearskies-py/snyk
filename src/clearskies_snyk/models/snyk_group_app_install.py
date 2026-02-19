"""Snyk Group App Install model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupAppInstall(Model):
    """
    Model for Snyk Group App Installs.

    This model represents installed Snyk Apps at the group level.
    Group app installs allow apps to access data across all organizations
    within a group.

    Uses the Snyk v2 REST API endpoint: `/groups/{group_id}/apps/installs`

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupAppInstall


    def my_handler(snyk_group_app_install: SnykGroupAppInstall):
        # Fetch all app installs for a group
        installs = snyk_group_app_install.where("group_id=group-id-123")
        for install in installs:
            print(f"Install: {install.id} - App: {install.app_id}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(resource_type="app_install", can_update=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/apps/installs"

    """
    The unique identifier for the app install.
    """
    id = String()

    """
    The ID of the group this install belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The ID of the app that was installed.
    """
    app_id = String()

    """
    The client ID of the installed app.
    """
    client_id = String()

    """
    Timestamp of when the app was installed.
    """
    created_at = Datetime()
