"""Snyk Org App Bot model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, String

from clearskies_snyk.backends import SnykBackend


class SnykOrgAppBot(Model):
    """
    Model for Snyk Organization App Bots.

    This model represents app bots within an organization.
    App bots are service accounts created by apps to perform
    automated actions.

    Uses the Snyk v2 REST API endpoint: `/orgs/{org_id}/app_bots`

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgAppBot


    def my_handler(snyk_org_app_bot: SnykOrgAppBot):
        # Fetch all app bots for an org
        bots = snyk_org_app_bot.where("org_id=org-id-123")
        for bot in bots:
            print(f"Bot: {bot.id} - App: {bot.app_id}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(can_create=False, can_update=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/app_bots"

    """
    The unique identifier for the app bot.
    """
    id = String()

    """
    The ID of the organization this bot belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the app that created this bot.
    """
    app_id = String()

    """
    The name of the app bot.
    """
    name = String()

    """
    Timestamp of when the bot was created.
    """
    created_at = Datetime()
