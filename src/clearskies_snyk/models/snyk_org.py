"""Snyk Organization model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, HasMany, HasOne, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import (
    snyk_collection_reference,
    snyk_container_image_reference,
    snyk_dependency_reference,
    snyk_entitlement_reference,
    snyk_group_reference,
    snyk_integration_reference,
    snyk_license_reference,
    snyk_org_issue_reference,
    snyk_org_membership_reference,
    snyk_org_service_account_reference,
    snyk_org_settings_iac_reference,
    snyk_project_reference,
    snyk_target_reference,
    snyk_webhook_reference,
)


class SnykOrg(Model):
    """
    Model for Snyk Organizations.

    This model represents organizations in Snyk. Organizations are the primary
    container for projects, targets, and other resources in Snyk.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykOrg


    def my_handler(snyk_org: SnykOrg):
        # Fetch all organizations
        for org in snyk_org:
            print(f"Org: {org.name} ({org.slug})")

        # Find a specific organization by ID
        org = snyk_org.find("id=org-id-123")
        print(org.name)

        # Access the parent group
        print(f"Group: {org.group.name}")

        # Access related projects
        for project in org.projects:
            print(f"  Project: {project.name}")
    ```
    """

    id_column_name: str = "id"

    # orgs: query=True, create=False, update=True, delete=False
    backend = SnykBackend(can_create=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs"

    """
    The unique identifier for the organization.
    """
    id = String()

    """
    The ID of the group this organization belongs to.
    """
    group_id = BelongsToId(
        snyk_group_reference.SnykGroupReference,
        is_searchable=True,
    )

    """
    The parent group this organization belongs to.

    BelongsTo relationship to SnykGroup.
    """
    group = BelongsToModel("group_id")

    """
    The human-readable name of the organization.
    """
    name = String()

    """
    The URL-friendly slug for the organization.
    """
    slug = String()

    """
    Whether this is a personal organization.
    """
    is_personal = Boolean()

    """
    Related projects for this organization.

    HasMany relationship to SnykProject.
    """
    projects = HasMany(
        snyk_project_reference.SnykProjectReference,
        foreign_column_name="org_id",
    )

    """
    Related targets for this organization.

    HasMany relationship to SnykTarget.
    """
    targets = HasMany(
        snyk_target_reference.SnykTargetReference,
        foreign_column_name="org_id",
    )

    """
    Related collections for this organization.

    HasMany relationship to SnykCollection.
    """
    collections = HasMany(
        snyk_collection_reference.SnykCollectionReference,
        foreign_column_name="org_id",
    )

    """
    Related container images for this organization.

    HasMany relationship to SnykContainerImage.
    """
    container_images = HasMany(
        snyk_container_image_reference.SnykContainerImageReference,
        foreign_column_name="org_id",
    )

    """
    Organization memberships.

    HasMany relationship to SnykOrgMembership.
    """
    memberships = HasMany(
        snyk_org_membership_reference.SnykOrgMembershipReference,
        foreign_column_name="org_id",
    )

    """
    Organization service accounts.

    HasMany relationship to SnykOrgServiceAccount.
    """
    service_accounts = HasMany(
        snyk_org_service_account_reference.SnykOrgServiceAccountReference,
        foreign_column_name="org_id",
    )

    """
    Organization issues.

    HasMany relationship to SnykOrgIssue.
    """
    issues = HasMany(
        snyk_org_issue_reference.SnykOrgIssueReference,
        foreign_column_name="org_id",
    )

    """
    IAC settings for this organization.

    HasOne relationship to SnykOrgSettingsIac.
    """
    settings_iac = HasOne(
        snyk_org_settings_iac_reference.SnykOrgSettingsIacReference,
        foreign_column_name="org_id",
    )

    # V1 API relationships (these use the Snyk v1 API)

    """
    Webhooks for this organization (v1 API).

    HasMany relationship to SnykWebhook.
    """
    webhooks = HasMany(
        snyk_webhook_reference.SnykWebhookReference,
        foreign_column_name="org_id",
    )

    """
    Entitlements (feature flags) for this organization (v1 API).

    HasMany relationship to SnykEntitlement.
    """
    entitlements = HasMany(
        snyk_entitlement_reference.SnykEntitlementReference,
        foreign_column_name="org_id",
    )

    """
    Dependencies across all projects in this organization (v1 API).

    HasMany relationship to SnykDependency.
    """
    dependencies = HasMany(
        snyk_dependency_reference.SnykDependencyReference,
        foreign_column_name="org_id",
    )

    """
    Licenses found in dependencies across this organization (v1 API).

    HasMany relationship to SnykLicense.
    """
    licenses = HasMany(
        snyk_license_reference.SnykLicenseReference,
        foreign_column_name="org_id",
    )

    """
    Integrations configured for this organization (v1 API).

    HasMany relationship to SnykIntegration.
    """
    integrations = HasMany(
        snyk_integration_reference.SnykIntegrationReference,
        foreign_column_name="org_id",
    )
