"""Reference classes for Snyk models.

Reference classes are used to break circular import dependencies by providing
lazy loading of model classes.
"""

from clearskies_snyk.models.references.snyk_cloud_environment_reference import (
    SnykCloudEnvironmentReference,
)
from clearskies_snyk.models.references.snyk_collection_reference import (
    SnykCollectionReference,
)
from clearskies_snyk.models.references.snyk_container_image_reference import (
    SnykContainerImageReference,
)
from clearskies_snyk.models.references.snyk_dependency_reference import (
    SnykDependencyReference,
)
from clearskies_snyk.models.references.snyk_entitlement_reference import (
    SnykEntitlementReference,
)
from clearskies_snyk.models.references.snyk_group_issue_reference import (
    SnykGroupIssueReference,
)
from clearskies_snyk.models.references.snyk_group_membership_reference import (
    SnykGroupMembershipReference,
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
from clearskies_snyk.models.references.snyk_group_settings_reference import (
    SnykGroupSettingsReference,
)
from clearskies_snyk.models.references.snyk_group_tag_reference import (
    SnykGroupTagReference,
)
from clearskies_snyk.models.references.snyk_integration_reference import (
    SnykIntegrationReference,
)
from clearskies_snyk.models.references.snyk_license_reference import (
    SnykLicenseReference,
)
from clearskies_snyk.models.references.snyk_org_invite_reference import (
    SnykOrgInviteReference,
)
from clearskies_snyk.models.references.snyk_org_issue_reference import (
    SnykOrgIssueReference,
)
from clearskies_snyk.models.references.snyk_org_membership_reference import (
    SnykOrgMembershipReference,
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
from clearskies_snyk.models.references.snyk_project_reference import (
    SnykProjectReference,
)
from clearskies_snyk.models.references.snyk_target_reference import SnykTargetReference
from clearskies_snyk.models.references.snyk_tenant_membership_reference import (
    SnykTenantMembershipReference,
)
from clearskies_snyk.models.references.snyk_tenant_reference import SnykTenantReference
from clearskies_snyk.models.references.snyk_tenant_role_reference import (
    SnykTenantRoleReference,
)
from clearskies_snyk.models.references.snyk_webhook_reference import (
    SnykWebhookReference,
)

__all__ = [
    "SnykCloudEnvironmentReference",
    "SnykCollectionReference",
    "SnykContainerImageReference",
    "SnykDependencyReference",
    "SnykEntitlementReference",
    "SnykGroupIssueReference",
    "SnykGroupMembershipReference",
    "SnykGroupPolicyReference",
    "SnykGroupReference",
    "SnykGroupRoleV1Reference",
    "SnykGroupServiceAccountReference",
    "SnykGroupSettingsReference",
    "SnykGroupTagReference",
    "SnykIntegrationReference",
    "SnykLicenseReference",
    "SnykOrgInviteReference",
    "SnykOrgIssueReference",
    "SnykOrgMembershipReference",
    "SnykOrgPolicyReference",
    "SnykOrgReference",
    "SnykOrgServiceAccountReference",
    "SnykOrgSettingsIacReference",
    "SnykProjectReference",
    "SnykTargetReference",
    "SnykTenantMembershipReference",
    "SnykTenantReference",
    "SnykTenantRoleReference",
    "SnykWebhookReference",
]
