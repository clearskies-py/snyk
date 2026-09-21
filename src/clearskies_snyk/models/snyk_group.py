"""Snyk Group model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, HasMany, HasOne, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import (
    snyk_group_app_install_reference,
    snyk_group_audit_log_reference,
    snyk_group_export_reference,
    snyk_group_issue_reference,
    snyk_group_member_reference,
    snyk_group_membership_reference,
    snyk_group_org_membership_reference,
    snyk_group_policy_reference,
    snyk_group_role_v1_reference,
    snyk_group_service_account_reference,
    snyk_group_settings_iac_reference,
    snyk_group_settings_reference,
    snyk_group_sso_connection_reference,
    snyk_group_tag_reference,
    snyk_group_user_reference,
    snyk_org_reference,
    snyk_pull_request_template_reference,
)


class SnykGroup(Model):
    """
    Model for Snyk Groups.

    This model represents groups in Snyk. Groups are the top-level container
    that can contain multiple organizations.

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroup


    def my_handler(snyk_group: SnykGroup):
        # Fetch all groups
        groups = snyk_group
        for group in groups:
            print(f"Group: {group.name}")

        # Find a specific group
        group = groups.find("id=group-id-123")
        print(group.name)

        # Access related organizations
        for org in group.orgs:
            print(f"  Org: {org.name}")

        # Access group memberships
        for membership in group.memberships:
            print(f"  Member: {membership.name}")
    ```
    """

    id_column_name: str = "id"

    # groups: query=True, create=False, update=False, delete=False
    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups"

    """
    The unique identifier for the group.
    """
    id = String()

    """
    The human-readable name of the group.
    """
    name = String()

    """
    Related organizations for this group.

    HasMany relationship to SnykOrg.
    """
    orgs = HasMany(
        snyk_org_reference.SnykOrgReference,
        foreign_column_name="group_id",
    )

    """
    Group memberships.

    HasMany relationship to SnykGroupMembership.
    """
    memberships = HasMany(
        snyk_group_membership_reference.SnykGroupMembershipReference,
        foreign_column_name="group_id",
    )

    """
    Group service accounts.

    HasMany relationship to SnykGroupServiceAccount.
    """
    service_accounts = HasMany(
        snyk_group_service_account_reference.SnykGroupServiceAccountReference,
        foreign_column_name="group_id",
    )

    """
    Group issues.

    HasMany relationship to SnykGroupIssue.
    """
    issues = HasMany(
        snyk_group_issue_reference.SnykGroupIssueReference,
        foreign_column_name="group_id",
    )

    # V1 API relationships (these use the Snyk v1 API)

    """
    Group settings (v1 API).

    HasOne relationship to SnykGroupSettings.
    """
    settings = HasOne(
        snyk_group_settings_reference.SnykGroupSettingsReference,
        foreign_column_name="group_id",
    )

    """
    Tags in this group (v1 API).

    HasMany relationship to SnykGroupTag.
    """
    tags = HasMany(
        snyk_group_tag_reference.SnykGroupTagReference,
        foreign_column_name="group_id",
    )

    """
    Roles available in this group (v1 API).

    HasMany relationship to SnykGroupRoleV1.
    """
    roles = HasMany(
        snyk_group_role_v1_reference.SnykGroupRoleV1Reference,
        foreign_column_name="group_id",
    )

    """
    App installs for this group.

    HasMany relationship to SnykGroupAppInstall.
    """
    app_installs = HasMany(
        snyk_group_app_install_reference.SnykGroupAppInstallReference,
        foreign_column_name="group_id",
    )

    """
    Audit logs for this group.

    HasMany relationship to SnykGroupAuditLog.
    """
    audit_logs = HasMany(
        snyk_group_audit_log_reference.SnykGroupAuditLogReference,
        foreign_column_name="group_id",
    )

    """
    Export jobs for this group.

    HasMany relationship to SnykGroupExport.
    """
    exports = HasMany(
        snyk_group_export_reference.SnykGroupExportReference,
        foreign_column_name="group_id",
    )

    """
    Members of this group.

    HasMany relationship to SnykGroupMember.
    """
    members = HasMany(
        snyk_group_member_reference.SnykGroupMemberReference,
        foreign_column_name="group_id",
    )

    """
    Organization memberships in this group.

    HasMany relationship to SnykGroupOrgMembership.
    """
    org_memberships = HasMany(
        snyk_group_org_membership_reference.SnykGroupOrgMembershipReference,
        foreign_column_name="group_id",
    )

    """
    Policies for this group.

    HasMany relationship to SnykGroupPolicy.
    """
    policies = HasMany(
        snyk_group_policy_reference.SnykGroupPolicyReference,
        foreign_column_name="group_id",
    )

    """
    SSO connections for this group.

    HasMany relationship to SnykGroupSsoConnection.
    """
    sso_connections = HasMany(
        snyk_group_sso_connection_reference.SnykGroupSsoConnectionReference,
        foreign_column_name="group_id",
    )

    """
    Users in this group.

    HasMany relationship to SnykGroupUser.
    """
    users = HasMany(
        snyk_group_user_reference.SnykGroupUserReference,
        foreign_column_name="group_id",
    )

    """
    IaC settings for this group.

    HasOne relationship to SnykGroupSettingsIac.
    """
    settings_iac = HasOne(
        snyk_group_settings_iac_reference.SnykGroupSettingsIacReference,
        foreign_column_name="group_id",
    )

    """
    Pull request template for this group.

    HasOne relationship to SnykPullRequestTemplate.
    """
    pull_request_template = HasOne(
        snyk_pull_request_template_reference.SnykPullRequestTemplateReference,
        foreign_column_name="group_id",
    )

    """
    URL of the group avatar.
    """
    avatar_url = String()

    """
    URL of the group logo.
    """
    logo_url = String()

    """
    URL-friendly slug for the group.
    """
    slug = String()

    """
    Timestamp when the group was created.
    """
    created_at = Datetime()

    """
    Timestamp when the group was last updated.
    """
    updated_at = Datetime()

    """
    Contact email for the group.
    """
    email = String()

    """
    Username associated with the group.
    """
    username = String()

    """
    Filter by user ID.
    """
    user_id = String(is_searchable=True, is_temporary=True)

    """
    Filter by organization name.
    """
    org_name = String(is_searchable=True, is_temporary=True)

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
    Include group membership count in response.
    """
    include_group_membership_count = Boolean(is_searchable=True, is_temporary=True)

    """
    Cascade membership changes.
    """
    cascade = Boolean(is_searchable=True, is_temporary=True)

    """
    Filter by asset types.
    """
    asset_types = String(is_searchable=True, is_temporary=True)
