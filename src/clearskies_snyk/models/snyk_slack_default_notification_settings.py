"""Snyk Slack Default Notification Settings model."""

from typing import Self

from clearskies import Model
from clearskies.columns import String

from clearskies_snyk.backends import SnykBackend


class SnykSlackDefaultNotificationSettings(Model):
    """
    Model for Snyk Slack Default Notification Settings.

    This model represents the default Slack notification settings for an organization.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/slack_app/{bot_id}

    ```python
    import clearskies
    from clearskies_snyk.models import SnykSlackDefaultNotificationSettings


    def my_handler(snyk_slack_default_notification_settings: SnykSlackDefaultNotificationSettings):
        # Get default Slack notification settings
        settings = snyk_slack_default_notification_settings.where("org_id=org-123").where(
            "bot_id=bot-456"
        )
        for setting in settings:
            print(f"Channel: {setting.target_channel_name}, Severity: {setting.severity_threshold}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(api_to_model_map={"type": "settings_type"}, can_update=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/slack_app/{bot_id}"

    # Columns based on SlackDefaultSettingsData schema
    id = String()
    org_id = String(is_searchable=True)
    bot_id = String(is_searchable=True)
    settings_type = String()  # Mapped from 'type', e.g., "slack"

    # Attributes
    target_channel_id = String()  # URI format, e.g., "slack://channel?team=team-id&id=channel-id"
    target_channel_name = String()  # Name of the Slack channel
    severity_threshold = String()  # low, medium, high, critical
