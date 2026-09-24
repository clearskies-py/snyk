"""Reference classes for Snyk models.

Reference classes are used to break circular import dependencies by providing
lazy loading of model classes.
"""

from clearskies_snyk.models.references.snyk_ai_bom_reference import SnykAiBomReference
from clearskies_snyk.models.references.snyk_broker_connection_reference import (
    SnykBrokerConnectionReference,
)
from clearskies_snyk.models.references.snyk_broker_deployment_reference import (
    SnykBrokerDeploymentReference,
)
from clearskies_snyk.models.references.snyk_cloud_environment_reference import (
    SnykCloudEnvironmentReference,
)
from clearskies_snyk.models.references.snyk_cloud_resource_reference import (
    SnykCloudResourceReference,
)
from clearskies_snyk.models.references.snyk_cloud_scan_reference import (
    SnykCloudScanReference,
)
from clearskies_snyk.models.references.snyk_collection_reference import (
    SnykCollectionReference,
)
from clearskies_snyk.models.references.snyk_container_image_reference import (
    SnykContainerImageReference,
)
from clearskies_snyk.models.references.snyk_container_image_target_ref_reference import (
    SnykContainerImageTargetRefReference,
)
from clearskies_snyk.models.references.snyk_dependency_reference import (
    SnykDependencyReference,
)
from clearskies_snyk.models.references.snyk_entitlement_reference import (
    SnykEntitlementReference,
)
from clearskies_snyk.models.references.snyk_fix_pull_request_reference import (
    SnykFixPullRequestReference,
)
from clearskies_snyk.models.references.snyk_group_app_install_reference import (
    SnykGroupAppInstallReference,
)
from clearskies_snyk.models.references.snyk_group_audit_log_reference import (
    SnykGroupAuditLogReference,
)
from clearskies_snyk.models.references.snyk_group_export_reference import (
    SnykGroupExportReference,
)
from clearskies_snyk.models.references.snyk_group_issue_reference import (
    SnykGroupIssueReference,
)
from clearskies_snyk.models.references.snyk_group_member_reference import (
    SnykGroupMemberReference,
)
from clearskies_snyk.models.references.snyk_group_membership_reference import (
    SnykGroupMembershipReference,
)
from clearskies_snyk.models.references.snyk_group_org_membership_reference import (
    SnykGroupOrgMembershipReference,
)
from clearskies_snyk.models.references.snyk_group_policy_reference import (
    SnykGroupPolicyReference,
)
from clearskies_snyk.models.references.snyk_group_reference import SnykGroupReference
from clearskies_snyk.models.references.snyk_group_role_v1_reference import (
    SnykGroupRoleV1Reference,
)
from clearskies_snyk.models.references.snyk_group_service_account_reference import (
    SnykGroupServiceAccountReference,
)
from clearskies_snyk.models.references.snyk_group_settings_iac_reference import (
    SnykGroupSettingsIacReference,
)
from clearskies_snyk.models.references.snyk_group_settings_reference import (
    SnykGroupSettingsReference,
)
from clearskies_snyk.models.references.snyk_group_sso_connection_reference import (
    SnykGroupSsoConnectionReference,
)
from clearskies_snyk.models.references.snyk_group_sso_connection_user_reference import (
    SnykGroupSsoConnectionUserReference,
)
from clearskies_snyk.models.references.snyk_group_tag_reference import (
    SnykGroupTagReference,
)
from clearskies_snyk.models.references.snyk_group_user_reference import (
    SnykGroupUserReference,
)
from clearskies_snyk.models.references.snyk_integration_reference import (
    SnykIntegrationReference,
)
from clearskies_snyk.models.references.snyk_learn_assignment_reference import (
    SnykLearnAssignmentReference,
)
from clearskies_snyk.models.references.snyk_license_reference import (
    SnykLicenseReference,
)
from clearskies_snyk.models.references.snyk_org_app_bot_reference import (
    SnykOrgAppBotReference,
)
from clearskies_snyk.models.references.snyk_org_app_install_reference import (
    SnykOrgAppInstallReference,
)
from clearskies_snyk.models.references.snyk_org_app_reference import SnykOrgAppReference
from clearskies_snyk.models.references.snyk_org_audit_log_reference import (
    SnykOrgAuditLogReference,
)
from clearskies_snyk.models.references.snyk_org_export_reference import (
    SnykOrgExportReference,
)
from clearskies_snyk.models.references.snyk_org_invite_reference import (
    SnykOrgInviteReference,
)
from clearskies_snyk.models.references.snyk_org_issue_reference import (
    SnykOrgIssueReference,
)
from clearskies_snyk.models.references.snyk_org_member_reference import (
    SnykOrgMemberReference,
)
from clearskies_snyk.models.references.snyk_org_membership_reference import (
    SnykOrgMembershipReference,
)
from clearskies_snyk.models.references.snyk_org_policy_event_reference import (
    SnykOrgPolicyEventReference,
)
from clearskies_snyk.models.references.snyk_org_policy_reference import (
    SnykOrgPolicyReference,
)
from clearskies_snyk.models.references.snyk_org_reference import SnykOrgReference
from clearskies_snyk.models.references.snyk_org_service_account_reference import (
    SnykOrgServiceAccountReference,
)
from clearskies_snyk.models.references.snyk_org_settings_iac_reference import (
    SnykOrgSettingsIacReference,
)
from clearskies_snyk.models.references.snyk_org_settings_open_source_reference import (
    SnykOrgSettingsOpenSourceReference,
)
from clearskies_snyk.models.references.snyk_org_settings_sast_reference import (
    SnykOrgSettingsSastReference,
)
from clearskies_snyk.models.references.snyk_org_user_reference import (
    SnykOrgUserReference,
)
from clearskies_snyk.models.references.snyk_project_history_reference import (
    SnykProjectHistoryReference,
)
from clearskies_snyk.models.references.snyk_project_ignore_reference import (
    SnykProjectIgnoreReference,
)
from clearskies_snyk.models.references.snyk_project_reference import (
    SnykProjectReference,
)
from clearskies_snyk.models.references.snyk_project_sbom_reference import (
    SnykProjectSbomReference,
)
from clearskies_snyk.models.references.snyk_pull_request_template_reference import (
    SnykPullRequestTemplateReference,
)
from clearskies_snyk.models.references.snyk_sbom_test_reference import (
    SnykSbomTestReference,
)
from clearskies_snyk.models.references.snyk_self_app_session_reference import (
    SnykSelfAppSessionReference,
)
from clearskies_snyk.models.references.snyk_slack_channel_reference import (
    SnykSlackChannelReference,
)
from clearskies_snyk.models.references.snyk_target_reference import SnykTargetReference
from clearskies_snyk.models.references.snyk_tenant_membership_reference import (
    SnykTenantMembershipReference,
)
from clearskies_snyk.models.references.snyk_tenant_reference import SnykTenantReference
from clearskies_snyk.models.references.snyk_tenant_role_reference import (
    SnykTenantRoleReference,
)
from clearskies_snyk.models.references.snyk_test_job_reference import (
    SnykTestJobReference,
)
from clearskies_snyk.models.references.snyk_webhook_reference import (
    SnykWebhookReference,
)

__all__ = [
    "SnykAiBomReference",
    "SnykBrokerConnectionReference",
    "SnykBrokerDeploymentReference",
    "SnykCloudEnvironmentReference",
    "SnykCloudResourceReference",
    "SnykCloudScanReference",
    "SnykCollectionReference",
    "SnykContainerImageReference",
    "SnykContainerImageTargetRefReference",
    "SnykDependencyReference",
    "SnykEntitlementReference",
    "SnykFixPullRequestReference",
    "SnykGroupAppInstallReference",
    "SnykGroupAuditLogReference",
    "SnykGroupExportReference",
    "SnykGroupIssueReference",
    "SnykGroupMemberReference",
    "SnykGroupMembershipReference",
    "SnykGroupOrgMembershipReference",
    "SnykGroupPolicyReference",
    "SnykGroupReference",
    "SnykGroupRoleV1Reference",
    "SnykGroupServiceAccountReference",
    "SnykGroupSettingsIacReference",
    "SnykGroupSettingsReference",
    "SnykGroupSsoConnectionReference",
    "SnykGroupSsoConnectionUserReference",
    "SnykGroupTagReference",
    "SnykGroupUserReference",
    "SnykIntegrationReference",
    "SnykLearnAssignmentReference",
    "SnykLicenseReference",
    "SnykOrgAppBotReference",
    "SnykOrgAppInstallReference",
    "SnykOrgAppReference",
    "SnykOrgAuditLogReference",
    "SnykOrgExportReference",
    "SnykOrgInviteReference",
    "SnykOrgIssueReference",
    "SnykOrgMemberReference",
    "SnykOrgMembershipReference",
    "SnykOrgPolicyEventReference",
    "SnykOrgPolicyReference",
    "SnykOrgReference",
    "SnykOrgServiceAccountReference",
    "SnykOrgSettingsIacReference",
    "SnykOrgSettingsOpenSourceReference",
    "SnykOrgSettingsSastReference",
    "SnykOrgUserReference",
    "SnykProjectHistoryReference",
    "SnykProjectIgnoreReference",
    "SnykProjectReference",
    "SnykProjectSbomReference",
    "SnykPullRequestTemplateReference",
    "SnykSbomTestReference",
    "SnykSelfAppSessionReference",
    "SnykSlackChannelReference",
    "SnykTargetReference",
    "SnykTenantMembershipReference",
    "SnykTenantReference",
    "SnykTenantRoleReference",
    "SnykTestJobReference",
    "SnykWebhookReference",
]
