"""Snyk Slack Channel model."""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykBackend


class SnykSlackChannel(Model):
    """
    Model for Snyk Slack Channel.

    This model represents a Slack channel that the Snyk Slack App can access.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/slack_app/{tenant_id}/channels/{channel_id}

    ```python
    from clearskies_snyk.models import SnykSlackChannel

    # List Slack channels accessible by the Snyk Slack App
    channels = SnykSlackChannel().where("org_id=org-123").where("tenant_id=tenant-456")
    for channel in channels:
        print(f"Channel: {channel.name}, Type: {channel.channel_type}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(api_to_model_map={"type": "channel_type"}, can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/slack_app/{tenant_id}/channels"

    # Columns based on SlackChannel schema
    id = String()  # URI format, e.g., "slack://channel?team=T123456&id=C123456"
    org_id = String(is_searchable=True)
    tenant_id = String(is_searchable=True)
    channel_type = String()  # Mapped from 'type', e.g., "slack_channel"

    # Attributes
    name = String()  # Name of the Slack Channel
    slack_channel_type = String()  # public, private, direct_message, multiparty_direct_message
