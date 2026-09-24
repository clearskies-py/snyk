"""Snyk Organization model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, HasMany, HasOne, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import (
    snyk_broker_connection_reference,
    snyk_cloud_environment_reference,
    snyk_cloud_resource_reference,
    snyk_cloud_scan_reference,
    snyk_collection_reference,
    snyk_container_image_reference,
    snyk_dependency_reference,
    snyk_entitlement_reference,
    snyk_group_reference,
    snyk_integration_reference,
    snyk_learn_assignment_reference,
    snyk_license_reference,
    snyk_org_app_bot_reference,
    snyk_org_app_install_reference,
    snyk_org_app_reference,
    snyk_org_audit_log_reference,
    snyk_org_export_reference,
    snyk_org_issue_reference,
    snyk_org_member_reference,
    snyk_org_membership_reference,
    snyk_org_policy_reference,
    snyk_org_service_account_reference,
    snyk_org_settings_iac_reference,
    snyk_org_settings_open_source_reference,
    snyk_org_settings_sast_reference,
    snyk_org_user_reference,
    snyk_project_reference,
    snyk_sbom_test_reference,
    snyk_target_reference,
    snyk_test_job_reference,
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
    backend = SnykBackend(resource_type="org", can_create=False, can_delete=False)

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

    """
    Apps registered in this organization.

    HasMany relationship to SnykOrgApp.
    """
    apps = HasMany(
        snyk_org_app_reference.SnykOrgAppReference,
        foreign_column_name="org_id",
    )

    """
    App bots in this organization.

    HasMany relationship to SnykOrgAppBot.
    """
    app_bots = HasMany(
        snyk_org_app_bot_reference.SnykOrgAppBotReference,
        foreign_column_name="org_id",
    )

    """
    App installs in this organization.

    HasMany relationship to SnykOrgAppInstall.
    """
    app_installs = HasMany(
        snyk_org_app_install_reference.SnykOrgAppInstallReference,
        foreign_column_name="org_id",
    )

    """
    Audit logs for this organization.

    HasMany relationship to SnykOrgAuditLog.
    """
    audit_logs = HasMany(
        snyk_org_audit_log_reference.SnykOrgAuditLogReference,
        foreign_column_name="org_id",
    )

    """
    Export jobs for this organization.

    HasMany relationship to SnykOrgExport.
    """
    exports = HasMany(
        snyk_org_export_reference.SnykOrgExportReference,
        foreign_column_name="org_id",
    )

    """
    Members of this organization.

    HasMany relationship to SnykOrgMember.
    """
    members = HasMany(
        snyk_org_member_reference.SnykOrgMemberReference,
        foreign_column_name="org_id",
    )

    """
    Policies for this organization.

    HasMany relationship to SnykOrgPolicy.
    """
    policies = HasMany(
        snyk_org_policy_reference.SnykOrgPolicyReference,
        foreign_column_name="org_id",
    )

    """
    Users in this organization.

    HasMany relationship to SnykOrgUser.
    """
    users = HasMany(
        snyk_org_user_reference.SnykOrgUserReference,
        foreign_column_name="org_id",
    )

    """
    Cloud environments for this organization.

    HasMany relationship to SnykCloudEnvironment.
    """
    cloud_environments = HasMany(
        snyk_cloud_environment_reference.SnykCloudEnvironmentReference,
        foreign_column_name="org_id",
    )

    """
    Cloud resources for this organization.

    HasMany relationship to SnykCloudResource.
    """
    cloud_resources = HasMany(
        snyk_cloud_resource_reference.SnykCloudResourceReference,
        foreign_column_name="org_id",
    )

    """
    Cloud scans for this organization.

    HasMany relationship to SnykCloudScan.
    """
    cloud_scans = HasMany(
        snyk_cloud_scan_reference.SnykCloudScanReference,
        foreign_column_name="org_id",
    )

    """
    Open source settings for this organization.

    HasOne relationship to SnykOrgSettingsOpenSource.
    """
    settings_open_source = HasOne(
        snyk_org_settings_open_source_reference.SnykOrgSettingsOpenSourceReference,
        foreign_column_name="org_id",
    )

    """
    SAST settings for this organization.

    HasOne relationship to SnykOrgSettingsSast.
    """
    settings_sast = HasOne(
        snyk_org_settings_sast_reference.SnykOrgSettingsSastReference,
        foreign_column_name="org_id",
    )

    """
    Test jobs for this organization.

    HasMany relationship to SnykTestJob.
    """
    test_jobs = HasMany(
        snyk_test_job_reference.SnykTestJobReference,
        foreign_column_name="org_id",
    )

    """
    SBOM tests for this organization.

    HasMany relationship to SnykSbomTest.
    """
    sbom_tests = HasMany(
        snyk_sbom_test_reference.SnykSbomTestReference,
        foreign_column_name="org_id",
    )

    """
    Learn assignments for this organization.

    HasMany relationship to SnykLearnAssignment.
    """
    learn_assignments = HasMany(
        snyk_learn_assignment_reference.SnykLearnAssignmentReference,
        foreign_column_name="org_id",
    )

    """
    Broker connections for this organization.

    HasMany relationship to SnykBrokerConnection.
    """
    broker_connections = HasMany(
        snyk_broker_connection_reference.SnykBrokerConnectionReference,
        foreign_column_name="org_id",
    )

    """
    Whether access requests are enabled for the org.
    """
    access_requests_enabled = Boolean()

    """
    Timestamp when the org was created.
    """
    created_at = Datetime()

    """
    Timestamp when the org was last updated.
    """
    updated_at = Datetime()

    """
    Filter by user email.
    """
    email = String(is_searchable=True, is_temporary=True)

    """
    Filter by user ID.
    """
    user_id = String(is_searchable=True, is_temporary=True)

    """
    Filter by username.
    """
    username = String(is_searchable=True, is_temporary=True)

    """
    Filter by role name.
    """
    role_name = String(is_searchable=True, is_temporary=True)

    """
    Sort field.
    """
    sort_by = String(is_searchable=True, is_temporary=True)

    """
    Sort order.
    """
    sort_order = String(is_searchable=True, is_temporary=True)

    """
    Expand related resources.
    """
    expand = String(is_searchable=True, is_temporary=True)
