"""Snyk Org Settings SAST model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, String

from clearskies_snyk.backends import SnykBackend


class SnykOrgSettingsSast(Model):
    """
    Model for Snyk Organization SAST (Snyk Code) Settings.

    This model represents SAST/Snyk Code settings at the organization level.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/settings/sast

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgSettingsSast


    def my_handler(snyk_org_settings_sast: SnykOrgSettingsSast):
        # Fetch SAST settings for an organization
        settings = snyk_org_settings_sast.where("org_id=org-id-123").first()
        print(f"SAST Enabled: {settings.sast_enabled}")
        print(f"Autofix Enabled: {settings.autofix_enabled}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'settings_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "settings_type",
        },
        can_create=False,
        can_delete=False,
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/settings/sast"

    """
    The unique identifier for the settings.
    """
    id = String()

    """
    The ID of the organization these settings belong to.
    """
    org_id = String(is_searchable=True)

    """
    The type of settings (sast_settings).
    """
    settings_type = String()

    """
    Whether SAST (Snyk Code) is enabled for the organization.
    """
    sast_enabled = Boolean()

    """
    Whether autofix is enabled for the organization.
    """
    autofix_enabled = Boolean()
