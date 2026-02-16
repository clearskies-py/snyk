"""Snyk Org Settings IaC model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgSettingsIac(Model):
    """
    Model for Snyk Organization IaC Settings.

    This model represents Infrastructure as Code settings at the organization level.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrgSettingsIac


    def my_handler(snyk_org_settings_iac: SnykOrgSettingsIac):
        # Fetch IaC settings for an organization
        settings = snyk_org_settings_iac.where("org_id=org-id-123").first()
        print(f"Custom Rules: {settings.custom_rules}")

        # Access the parent organization
        print(f"Org: {settings.org.name}")
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
        return "orgs/{org_id}/settings/iac"

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
    The type of settings.
    """
    settings_type = String()

    """
    Custom rules configuration.
    """
    custom_rules = Json()
