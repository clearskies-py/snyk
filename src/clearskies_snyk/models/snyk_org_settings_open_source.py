"""Snyk Org Settings Open Source model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykOrgSettingsOpenSource(Model):
    """
    Model for Snyk Organization Open Source Settings.

    This model represents Open Source settings at the organization level,
    including reachability analysis settings.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/settings/opensource

    ```python
    from clearskies_snyk.models import SnykOrgSettingsOpenSource

    # Fetch Open Source settings for an organization
    settings = SnykOrgSettingsOpenSource().where("org_id=org-id-123").first()
    print(f"Reachability Enabled: {settings.reachability_enabled}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'settings_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "settings_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/settings/opensource"

    """
    The unique identifier for the settings.
    """
    id = String()

    """
    The ID of the organization these settings belong to.
    """
    org_id = String(is_searchable=True)

    """
    The type of settings (opensource_settings).
    """
    settings_type = String()

    """
    Reachability settings as JSON.
    """
    reachability = Json()

    """
    Whether reachability analysis is enabled.
    When enabled, projects in this org will be scanned for reachable vulnerabilities.
    """
    reachability_enabled = Boolean()
