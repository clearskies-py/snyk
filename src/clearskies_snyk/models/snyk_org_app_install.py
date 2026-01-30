"""Snyk Org App Install model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, String

from clearskies_snyk.backends import SnykBackend


class SnykOrgAppInstall(Model):
    """
    Model for Snyk Organization App Installs.

    This model represents installed Snyk Apps within an organization.
    App installs are instances of apps that have been authorized to access
    an organization's data.

    Uses the Snyk v2 REST API endpoint: `/orgs/{org_id}/apps/installs`

    ```python
    from clearskies_snyk.models import SnykOrgAppInstall

    # Fetch all app installs for an org
    installs = SnykOrgAppInstall().where("org_id=org-id-123")
    for install in installs:
        print(f"Install: {install.id} - App: {install.app_id}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/apps/installs"

    """
    The unique identifier for the app install.
    """
    id = String()

    """
    The ID of the organization this install belongs to.
    """
    org_id = String(is_searchable=True)

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
