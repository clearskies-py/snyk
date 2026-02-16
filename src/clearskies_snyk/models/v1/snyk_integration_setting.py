"""Snyk Integration Setting model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have a direct
equivalent endpoint for integration settings.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Integer, Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykIntegrationSetting(Model):
    """
    Model for Snyk Integration Settings (v1 API).

    This model represents settings for a specific integration in a Snyk organization.
    Uses the Snyk v1 API endpoint: /org/{orgId}/integrations/{integrationId}/settings

    ```python
    import clearskies
    from clearskies_snyk.models import SnykIntegrationSetting


    def my_handler(snyk_integration_setting: SnykIntegrationSetting):
        # Fetch settings for an integration
        settings = (
            snyk_integration_setting.where("org_id=org-id-123")
            .where("integration_id=int-id-456")
            .first()
        )
        print(f"Auto upgrade enabled: {settings.auto_dep_upgrade_enabled}")
    ```
    """

    id_column_name: str = "integration_id"

    backend = SnykV1Backend(can_create=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations/{integration_id}/settings"

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the integration.
    """
    integration_id = String(is_searchable=True)

    """
    Limit for automatic dependency upgrades.
    """
    auto_dep_upgrade_limit = Integer()

    """
    Dependencies to ignore for automatic upgrades.
    """
    auto_dep_upgrade_ignored_dependencies = Json()

    """
    Whether automatic dependency upgrades are enabled.
    """
    auto_dep_upgrade_enabled = Integer()

    """
    Minimum age for automatic dependency upgrades.
    """
    auto_dep_upgrade_min_age = Integer()

    """
    Whether to fail pull requests on any vulnerabilities.
    """
    pull_request_fail_on_any_vulns = Integer()

    """
    Whether to fail pull requests only for high severity issues.
    """
    pull_request_fail_only_for_high_severity = Integer()

    """
    Whether pull request testing is enabled.
    """
    pull_request_test_enabled = Integer()

    """
    Pull request assignment configuration.
    """
    pull_request_assignment = Json()

    """
    Auto remediation PR configuration.
    """
    auto_remediation_prs = Json()

    """
    Manual remediation PR configuration.
    """
    manual_remediation_prs = Json()

    """
    Whether Dockerfile SCM scanning is enabled.
    """
    dockerfile_scm_enabled = Integer()
