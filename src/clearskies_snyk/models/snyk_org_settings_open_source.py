"""Snyk Org Settings Open Source model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgSettingsOpenSource(Model):
    """
    Model for Snyk Organization Open Source Settings.

    This model represents Open Source settings at the organization level,
    including reachability analysis settings.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/settings/opensource

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgSettingsOpenSource


    def my_handler(snyk_org_settings_open_source: SnykOrgSettingsOpenSource):
        # Fetch Open Source settings for an organization
        settings = snyk_org_settings_open_source.where("org_id=org-id-123").first()
        print(f"Reachability Enabled: {settings.reachability_enabled}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'settings_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "settings_type",
        },
        can_create=False,
        can_update=False,
        can_delete=False,
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
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization these settings belong to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

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
