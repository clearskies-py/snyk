"""Snyk Group Settings IaC model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykGroupSettingsIac(Model):
    """
    Model for Snyk Group IaC Settings.

    This model represents Infrastructure as Code settings at the group level.
    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/settings/iac

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupSettingsIac


    def my_handler(snyk_group_settings_iac: SnykGroupSettingsIac):
        # Fetch IaC settings for a group
        settings = snyk_group_settings_iac.where("group_id=group-id-123").first()
        print(f"Custom Rules Enabled: {settings.custom_rules_is_enabled}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'settings_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        resource_type="iac",
        api_to_model_map={
            "type": "settings_type",
        },
        can_create=False,
        can_delete=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/settings/iac"

    """
    The unique identifier for the settings.
    """
    id = String()

    """
    The ID of the group these settings belong to.
    """
    group_id = String(is_searchable=True)

    """
    The type of settings (iac_settings).
    """
    settings_type = String()

    """
    Custom rules configuration as JSON.
    Contains: is_enabled, oci_registry_url, oci_registry_tag
    """
    custom_rules = Json()

    """
    Whether custom rules are enabled.
    """
    custom_rules_is_enabled = Boolean()

    """
    The OCI registry URL for custom rules.
    """
    custom_rules_oci_registry_url = String()

    """
    The OCI registry tag for custom rules.
    """
    custom_rules_oci_registry_tag = String()

    """
    The last time the settings were updated.
    """
    updated = Datetime()
