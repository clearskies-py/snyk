"""
Tests for reference models.

This module tests the reference model classes that provide lazy loading
of model classes to avoid circular imports.
"""

from __future__ import annotations

import pytest


class TestSnykGroupReference:
    """Tests for SnykGroupReference."""

    def test_get_model_class_returns_snyk_group(self) -> None:
        """Test that get_model_class returns SnykGroup."""
        from clearskies_snyk.models.references.snyk_group_reference import SnykGroupReference
        from clearskies_snyk.models.snyk_group import SnykGroup

        ref = SnykGroupReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroup


class TestSnykOrgReference:
    """Tests for SnykOrgReference."""

    def test_get_model_class_returns_snyk_org(self) -> None:
        """Test that get_model_class returns SnykOrg."""
        from clearskies_snyk.models.references.snyk_org_reference import SnykOrgReference
        from clearskies_snyk.models.snyk_org import SnykOrg

        ref = SnykOrgReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrg


class TestSnykProjectReference:
    """Tests for SnykProjectReference."""

    def test_get_model_class_returns_snyk_project(self) -> None:
        """Test that get_model_class returns SnykProject."""
        from clearskies_snyk.models.references.snyk_project_reference import SnykProjectReference
        from clearskies_snyk.models.snyk_project import SnykProject

        ref = SnykProjectReference()
        model_class = ref.get_model_class()
        assert model_class is SnykProject


class TestSnykTargetReference:
    """Tests for SnykTargetReference."""

    def test_get_model_class_returns_snyk_target(self) -> None:
        """Test that get_model_class returns SnykTarget."""
        from clearskies_snyk.models.references.snyk_target_reference import SnykTargetReference
        from clearskies_snyk.models.snyk_target import SnykTarget

        ref = SnykTargetReference()
        model_class = ref.get_model_class()
        assert model_class is SnykTarget


class TestSnykCollectionReference:
    """Tests for SnykCollectionReference."""

    def test_get_model_class_returns_snyk_collection(self) -> None:
        """Test that get_model_class returns SnykCollection."""
        from clearskies_snyk.models.references.snyk_collection_reference import SnykCollectionReference
        from clearskies_snyk.models.snyk_collection import SnykCollection

        ref = SnykCollectionReference()
        model_class = ref.get_model_class()
        assert model_class is SnykCollection


class TestSnykContainerImageReference:
    """Tests for SnykContainerImageReference."""

    def test_get_model_class_returns_snyk_container_image(self) -> None:
        """Test that get_model_class returns SnykContainerImage."""
        from clearskies_snyk.models.references.snyk_container_image_reference import SnykContainerImageReference
        from clearskies_snyk.models.snyk_container_image import SnykContainerImage

        ref = SnykContainerImageReference()
        model_class = ref.get_model_class()
        assert model_class is SnykContainerImage


class TestSnykGroupIssueReference:
    """Tests for SnykGroupIssueReference."""

    def test_get_model_class_returns_snyk_group_issue(self) -> None:
        """Test that get_model_class returns SnykGroupIssue."""
        from clearskies_snyk.models.references.snyk_group_issue_reference import SnykGroupIssueReference
        from clearskies_snyk.models.snyk_group_issue import SnykGroupIssue

        ref = SnykGroupIssueReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupIssue


class TestSnykOrgIssueReference:
    """Tests for SnykOrgIssueReference."""

    def test_get_model_class_returns_snyk_org_issue(self) -> None:
        """Test that get_model_class returns SnykOrgIssue."""
        from clearskies_snyk.models.references.snyk_org_issue_reference import SnykOrgIssueReference
        from clearskies_snyk.models.snyk_org_issue import SnykOrgIssue

        ref = SnykOrgIssueReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgIssue


class TestSnykGroupMembershipReference:
    """Tests for SnykGroupMembershipReference."""

    def test_get_model_class_returns_snyk_group_membership(self) -> None:
        """Test that get_model_class returns SnykGroupMembership."""
        from clearskies_snyk.models.references.snyk_group_membership_reference import SnykGroupMembershipReference
        from clearskies_snyk.models.snyk_group_membership import SnykGroupMembership

        ref = SnykGroupMembershipReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupMembership


class TestSnykOrgMembershipReference:
    """Tests for SnykOrgMembershipReference."""

    def test_get_model_class_returns_snyk_org_membership(self) -> None:
        """Test that get_model_class returns SnykOrgMembership."""
        from clearskies_snyk.models.references.snyk_org_membership_reference import SnykOrgMembershipReference
        from clearskies_snyk.models.snyk_org_membership import SnykOrgMembership

        ref = SnykOrgMembershipReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgMembership


class TestSnykGroupPolicyReference:
    """Tests for SnykGroupPolicyReference."""

    def test_get_model_class_returns_snyk_group_policy(self) -> None:
        """Test that get_model_class returns SnykGroupPolicy."""
        from clearskies_snyk.models.references.snyk_group_policy_reference import SnykGroupPolicyReference
        from clearskies_snyk.models.snyk_group_policy import SnykGroupPolicy

        ref = SnykGroupPolicyReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupPolicy


class TestSnykOrgPolicyReference:
    """Tests for SnykOrgPolicyReference."""

    def test_get_model_class_returns_snyk_org_policy(self) -> None:
        """Test that get_model_class returns SnykOrgPolicy."""
        from clearskies_snyk.models.references.snyk_org_policy_reference import SnykOrgPolicyReference
        from clearskies_snyk.models.snyk_org_policy import SnykOrgPolicy

        ref = SnykOrgPolicyReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgPolicy


class TestSnykGroupServiceAccountReference:
    """Tests for SnykGroupServiceAccountReference."""

    def test_get_model_class_returns_snyk_group_service_account(self) -> None:
        """Test that get_model_class returns SnykGroupServiceAccount."""
        from clearskies_snyk.models.references.snyk_group_service_account_reference import (
            SnykGroupServiceAccountReference,
        )
        from clearskies_snyk.models.snyk_group_service_account import SnykGroupServiceAccount

        ref = SnykGroupServiceAccountReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupServiceAccount


class TestSnykOrgServiceAccountReference:
    """Tests for SnykOrgServiceAccountReference."""

    def test_get_model_class_returns_snyk_org_service_account(self) -> None:
        """Test that get_model_class returns SnykOrgServiceAccount."""
        from clearskies_snyk.models.references.snyk_org_service_account_reference import SnykOrgServiceAccountReference
        from clearskies_snyk.models.snyk_org_service_account import SnykOrgServiceAccount

        ref = SnykOrgServiceAccountReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgServiceAccount


class TestSnykOrgInviteReference:
    """Tests for SnykOrgInviteReference."""

    def test_get_model_class_returns_snyk_org_invite(self) -> None:
        """Test that get_model_class returns SnykOrgInvite."""
        from clearskies_snyk.models.references.snyk_org_invite_reference import SnykOrgInviteReference
        from clearskies_snyk.models.snyk_org_invite import SnykOrgInvite

        ref = SnykOrgInviteReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgInvite


class TestSnykOrgSettingsIacReference:
    """Tests for SnykOrgSettingsIacReference."""

    def test_get_model_class_returns_snyk_org_settings_iac(self) -> None:
        """Test that get_model_class returns SnykOrgSettingsIac."""
        from clearskies_snyk.models.references.snyk_org_settings_iac_reference import SnykOrgSettingsIacReference
        from clearskies_snyk.models.snyk_org_settings_iac import SnykOrgSettingsIac

        ref = SnykOrgSettingsIacReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgSettingsIac


class TestSnykTenantReference:
    """Tests for SnykTenantReference."""

    def test_get_model_class_returns_snyk_tenant(self) -> None:
        """Test that get_model_class returns SnykTenant."""
        from clearskies_snyk.models.references.snyk_tenant_reference import SnykTenantReference
        from clearskies_snyk.models.snyk_tenant import SnykTenant

        ref = SnykTenantReference()
        model_class = ref.get_model_class()
        assert model_class is SnykTenant


class TestSnykTenantMembershipReference:
    """Tests for SnykTenantMembershipReference."""

    def test_get_model_class_returns_snyk_tenant_membership(self) -> None:
        """Test that get_model_class returns SnykTenantMembership."""
        from clearskies_snyk.models.references.snyk_tenant_membership_reference import SnykTenantMembershipReference
        from clearskies_snyk.models.snyk_tenant_membership import SnykTenantMembership

        ref = SnykTenantMembershipReference()
        model_class = ref.get_model_class()
        assert model_class is SnykTenantMembership


class TestSnykTenantRoleReference:
    """Tests for SnykTenantRoleReference."""

    def test_get_model_class_returns_snyk_tenant_role(self) -> None:
        """Test that get_model_class returns SnykTenantRole."""
        from clearskies_snyk.models.references.snyk_tenant_role_reference import SnykTenantRoleReference
        from clearskies_snyk.models.snyk_tenant_role import SnykTenantRole

        ref = SnykTenantRoleReference()
        model_class = ref.get_model_class()
        assert model_class is SnykTenantRole


class TestSnykCloudEnvironmentReference:
    """Tests for SnykCloudEnvironmentReference."""

    def test_get_model_class_returns_snyk_cloud_environment(self) -> None:
        """Test that get_model_class returns SnykCloudEnvironment."""
        from clearskies_snyk.models.references.snyk_cloud_environment_reference import SnykCloudEnvironmentReference
        from clearskies_snyk.models.snyk_cloud_environment import SnykCloudEnvironment

        ref = SnykCloudEnvironmentReference()
        model_class = ref.get_model_class()
        assert model_class is SnykCloudEnvironment


# V1 Model References


class TestSnykWebhookReference:
    """Tests for SnykWebhookReference."""

    def test_get_model_class_returns_snyk_webhook(self) -> None:
        """Test that get_model_class returns SnykWebhook."""
        from clearskies_snyk.models.references.snyk_webhook_reference import SnykWebhookReference
        from clearskies_snyk.models.v1.snyk_webhook import SnykWebhook

        ref = SnykWebhookReference()
        model_class = ref.get_model_class()
        assert model_class is SnykWebhook


class TestSnykEntitlementReference:
    """Tests for SnykEntitlementReference."""

    def test_get_model_class_returns_snyk_entitlement(self) -> None:
        """Test that get_model_class returns SnykEntitlement."""
        from clearskies_snyk.models.references.snyk_entitlement_reference import SnykEntitlementReference
        from clearskies_snyk.models.v1.snyk_entitlement import SnykEntitlement

        ref = SnykEntitlementReference()
        model_class = ref.get_model_class()
        assert model_class is SnykEntitlement


class TestSnykDependencyReference:
    """Tests for SnykDependencyReference."""

    def test_get_model_class_returns_snyk_dependency(self) -> None:
        """Test that get_model_class returns SnykDependency."""
        from clearskies_snyk.models.references.snyk_dependency_reference import SnykDependencyReference
        from clearskies_snyk.models.v1.snyk_dependency import SnykDependency

        ref = SnykDependencyReference()
        model_class = ref.get_model_class()
        assert model_class is SnykDependency


class TestSnykLicenseReference:
    """Tests for SnykLicenseReference."""

    def test_get_model_class_returns_snyk_license(self) -> None:
        """Test that get_model_class returns SnykLicense."""
        from clearskies_snyk.models.references.snyk_license_reference import SnykLicenseReference
        from clearskies_snyk.models.v1.snyk_license import SnykLicense

        ref = SnykLicenseReference()
        model_class = ref.get_model_class()
        assert model_class is SnykLicense


class TestSnykIntegrationReference:
    """Tests for SnykIntegrationReference."""

    def test_get_model_class_returns_snyk_integration(self) -> None:
        """Test that get_model_class returns SnykIntegration."""
        from clearskies_snyk.models.references.snyk_integration_reference import SnykIntegrationReference
        from clearskies_snyk.models.v1.snyk_integration import SnykIntegration

        ref = SnykIntegrationReference()
        model_class = ref.get_model_class()
        assert model_class is SnykIntegration


class TestSnykGroupSettingsReference:
    """Tests for SnykGroupSettingsReference."""

    def test_get_model_class_returns_snyk_group_settings(self) -> None:
        """Test that get_model_class returns SnykGroupSettings."""
        from clearskies_snyk.models.references.snyk_group_settings_reference import SnykGroupSettingsReference
        from clearskies_snyk.models.v1.snyk_group_settings import SnykGroupSettings

        ref = SnykGroupSettingsReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupSettings


class TestSnykGroupTagReference:
    """Tests for SnykGroupTagReference."""

    def test_get_model_class_returns_snyk_group_tag(self) -> None:
        """Test that get_model_class returns SnykGroupTag."""
        from clearskies_snyk.models.references.snyk_group_tag_reference import SnykGroupTagReference
        from clearskies_snyk.models.v1.snyk_group_tag import SnykGroupTag

        ref = SnykGroupTagReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupTag


class TestSnykGroupRoleV1Reference:
    """Tests for SnykGroupRoleV1Reference."""

    def test_get_model_class_returns_snyk_group_role_v1(self) -> None:
        """Test that get_model_class returns SnykGroupRoleV1."""
        from clearskies_snyk.models.references.snyk_group_role_v1_reference import SnykGroupRoleV1Reference
        from clearskies_snyk.models.v1.snyk_group_role_v1 import SnykGroupRoleV1

        ref = SnykGroupRoleV1Reference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupRoleV1


class TestSnykAiBomReference:
    """Tests for SnykAiBomReference."""

    def test_get_model_class_returns_snyk_ai_bom(self) -> None:
        """Test that get_model_class returns SnykAiBom."""
        from clearskies_snyk.models.references.snyk_ai_bom_reference import SnykAiBomReference
        from clearskies_snyk.models.snyk_ai_bom import SnykAiBom

        ref = SnykAiBomReference()
        model_class = ref.get_model_class()
        assert model_class is SnykAiBom


class TestSnykBrokerConnectionReference:
    """Tests for SnykBrokerConnectionReference."""

    def test_get_model_class_returns_snyk_broker_connection(self) -> None:
        """Test that get_model_class returns SnykBrokerConnection."""
        from clearskies_snyk.models.references.snyk_broker_connection_reference import SnykBrokerConnectionReference
        from clearskies_snyk.models.snyk_broker_connection import SnykBrokerConnection

        ref = SnykBrokerConnectionReference()
        model_class = ref.get_model_class()
        assert model_class is SnykBrokerConnection


class TestSnykBrokerDeploymentReference:
    """Tests for SnykBrokerDeploymentReference."""

    def test_get_model_class_returns_snyk_broker_deployment(self) -> None:
        """Test that get_model_class returns SnykBrokerDeployment."""
        from clearskies_snyk.models.references.snyk_broker_deployment_reference import SnykBrokerDeploymentReference
        from clearskies_snyk.models.snyk_broker_deployment import SnykBrokerDeployment

        ref = SnykBrokerDeploymentReference()
        model_class = ref.get_model_class()
        assert model_class is SnykBrokerDeployment


class TestSnykCloudResourceReference:
    """Tests for SnykCloudResourceReference."""

    def test_get_model_class_returns_snyk_cloud_resource(self) -> None:
        """Test that get_model_class returns SnykCloudResource."""
        from clearskies_snyk.models.references.snyk_cloud_resource_reference import SnykCloudResourceReference
        from clearskies_snyk.models.snyk_cloud_resource import SnykCloudResource

        ref = SnykCloudResourceReference()
        model_class = ref.get_model_class()
        assert model_class is SnykCloudResource


class TestSnykCloudScanReference:
    """Tests for SnykCloudScanReference."""

    def test_get_model_class_returns_snyk_cloud_scan(self) -> None:
        """Test that get_model_class returns SnykCloudScan."""
        from clearskies_snyk.models.references.snyk_cloud_scan_reference import SnykCloudScanReference
        from clearskies_snyk.models.snyk_cloud_scan import SnykCloudScan

        ref = SnykCloudScanReference()
        model_class = ref.get_model_class()
        assert model_class is SnykCloudScan


class TestSnykFixPullRequestReference:
    """Tests for SnykFixPullRequestReference."""

    def test_get_model_class_returns_snyk_fix_pull_request(self) -> None:
        """Test that get_model_class returns SnykFixPullRequest."""
        from clearskies_snyk.models.references.snyk_fix_pull_request_reference import SnykFixPullRequestReference
        from clearskies_snyk.models.snyk_fix_pull_request import SnykFixPullRequest

        ref = SnykFixPullRequestReference()
        model_class = ref.get_model_class()
        assert model_class is SnykFixPullRequest


class TestSnykGroupAppInstallReference:
    """Tests for SnykGroupAppInstallReference."""

    def test_get_model_class_returns_snyk_group_app_install(self) -> None:
        """Test that get_model_class returns SnykGroupAppInstall."""
        from clearskies_snyk.models.references.snyk_group_app_install_reference import SnykGroupAppInstallReference
        from clearskies_snyk.models.snyk_group_app_install import SnykGroupAppInstall

        ref = SnykGroupAppInstallReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupAppInstall


class TestSnykGroupAuditLogReference:
    """Tests for SnykGroupAuditLogReference."""

    def test_get_model_class_returns_snyk_group_audit_log(self) -> None:
        """Test that get_model_class returns SnykGroupAuditLog."""
        from clearskies_snyk.models.references.snyk_group_audit_log_reference import SnykGroupAuditLogReference
        from clearskies_snyk.models.snyk_group_audit_log import SnykGroupAuditLog

        ref = SnykGroupAuditLogReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupAuditLog


class TestSnykGroupExportReference:
    """Tests for SnykGroupExportReference."""

    def test_get_model_class_returns_snyk_group_export(self) -> None:
        """Test that get_model_class returns SnykGroupExport."""
        from clearskies_snyk.models.references.snyk_group_export_reference import SnykGroupExportReference
        from clearskies_snyk.models.snyk_group_export import SnykGroupExport

        ref = SnykGroupExportReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupExport


class TestSnykGroupMemberReference:
    """Tests for SnykGroupMemberReference."""

    def test_get_model_class_returns_snyk_group_member(self) -> None:
        """Test that get_model_class returns SnykGroupMember."""
        from clearskies_snyk.models.references.snyk_group_member_reference import SnykGroupMemberReference
        from clearskies_snyk.models.snyk_group_member import SnykGroupMember

        ref = SnykGroupMemberReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupMember


class TestSnykGroupOrgMembershipReference:
    """Tests for SnykGroupOrgMembershipReference."""

    def test_get_model_class_returns_snyk_group_org_membership(self) -> None:
        """Test that get_model_class returns SnykGroupOrgMembership."""
        from clearskies_snyk.models.references.snyk_group_org_membership_reference import (
            SnykGroupOrgMembershipReference,
        )
        from clearskies_snyk.models.snyk_group_org_membership import SnykGroupOrgMembership

        ref = SnykGroupOrgMembershipReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupOrgMembership


class TestSnykGroupSettingsIacReference:
    """Tests for SnykGroupSettingsIacReference."""

    def test_get_model_class_returns_snyk_group_settings_iac(self) -> None:
        """Test that get_model_class returns SnykGroupSettingsIac."""
        from clearskies_snyk.models.references.snyk_group_settings_iac_reference import SnykGroupSettingsIacReference
        from clearskies_snyk.models.snyk_group_settings_iac import SnykGroupSettingsIac

        ref = SnykGroupSettingsIacReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupSettingsIac


class TestSnykGroupSsoConnectionReference:
    """Tests for SnykGroupSsoConnectionReference."""

    def test_get_model_class_returns_snyk_group_sso_connection(self) -> None:
        """Test that get_model_class returns SnykGroupSsoConnection."""
        from clearskies_snyk.models.references.snyk_group_sso_connection_reference import (
            SnykGroupSsoConnectionReference,
        )
        from clearskies_snyk.models.snyk_group_sso_connection import SnykGroupSsoConnection

        ref = SnykGroupSsoConnectionReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupSsoConnection


class TestSnykGroupSsoConnectionUserReference:
    """Tests for SnykGroupSsoConnectionUserReference."""

    def test_get_model_class_returns_snyk_group_sso_connection_user(self) -> None:
        """Test that get_model_class returns SnykGroupSsoConnectionUser."""
        from clearskies_snyk.models.references.snyk_group_sso_connection_user_reference import (
            SnykGroupSsoConnectionUserReference,
        )
        from clearskies_snyk.models.snyk_group_sso_connection_user import SnykGroupSsoConnectionUser

        ref = SnykGroupSsoConnectionUserReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupSsoConnectionUser


class TestSnykGroupUserReference:
    """Tests for SnykGroupUserReference."""

    def test_get_model_class_returns_snyk_group_user(self) -> None:
        """Test that get_model_class returns SnykGroupUser."""
        from clearskies_snyk.models.references.snyk_group_user_reference import SnykGroupUserReference
        from clearskies_snyk.models.snyk_group_user import SnykGroupUser

        ref = SnykGroupUserReference()
        model_class = ref.get_model_class()
        assert model_class is SnykGroupUser


class TestSnykLearnAssignmentReference:
    """Tests for SnykLearnAssignmentReference."""

    def test_get_model_class_returns_snyk_learn_assignment(self) -> None:
        """Test that get_model_class returns SnykLearnAssignment."""
        from clearskies_snyk.models.references.snyk_learn_assignment_reference import SnykLearnAssignmentReference
        from clearskies_snyk.models.snyk_learn_assignment import SnykLearnAssignment

        ref = SnykLearnAssignmentReference()
        model_class = ref.get_model_class()
        assert model_class is SnykLearnAssignment


class TestSnykOrgAppReference:
    """Tests for SnykOrgAppReference."""

    def test_get_model_class_returns_snyk_org_app(self) -> None:
        """Test that get_model_class returns SnykOrgApp."""
        from clearskies_snyk.models.references.snyk_org_app_reference import SnykOrgAppReference
        from clearskies_snyk.models.snyk_org_app import SnykOrgApp

        ref = SnykOrgAppReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgApp


class TestSnykOrgAppBotReference:
    """Tests for SnykOrgAppBotReference."""

    def test_get_model_class_returns_snyk_org_app_bot(self) -> None:
        """Test that get_model_class returns SnykOrgAppBot."""
        from clearskies_snyk.models.references.snyk_org_app_bot_reference import SnykOrgAppBotReference
        from clearskies_snyk.models.snyk_org_app_bot import SnykOrgAppBot

        ref = SnykOrgAppBotReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgAppBot


class TestSnykOrgAppInstallReference:
    """Tests for SnykOrgAppInstallReference."""

    def test_get_model_class_returns_snyk_org_app_install(self) -> None:
        """Test that get_model_class returns SnykOrgAppInstall."""
        from clearskies_snyk.models.references.snyk_org_app_install_reference import SnykOrgAppInstallReference
        from clearskies_snyk.models.snyk_org_app_install import SnykOrgAppInstall

        ref = SnykOrgAppInstallReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgAppInstall


class TestSnykOrgAuditLogReference:
    """Tests for SnykOrgAuditLogReference."""

    def test_get_model_class_returns_snyk_org_audit_log(self) -> None:
        """Test that get_model_class returns SnykOrgAuditLog."""
        from clearskies_snyk.models.references.snyk_org_audit_log_reference import SnykOrgAuditLogReference
        from clearskies_snyk.models.snyk_org_audit_log import SnykOrgAuditLog

        ref = SnykOrgAuditLogReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgAuditLog


class TestSnykOrgExportReference:
    """Tests for SnykOrgExportReference."""

    def test_get_model_class_returns_snyk_org_export(self) -> None:
        """Test that get_model_class returns SnykOrgExport."""
        from clearskies_snyk.models.references.snyk_org_export_reference import SnykOrgExportReference
        from clearskies_snyk.models.snyk_org_export import SnykOrgExport

        ref = SnykOrgExportReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgExport


class TestSnykOrgMemberReference:
    """Tests for SnykOrgMemberReference."""

    def test_get_model_class_returns_snyk_org_member(self) -> None:
        """Test that get_model_class returns SnykOrgMember."""
        from clearskies_snyk.models.references.snyk_org_member_reference import SnykOrgMemberReference
        from clearskies_snyk.models.snyk_org_member import SnykOrgMember

        ref = SnykOrgMemberReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgMember


class TestSnykOrgSettingsOpenSourceReference:
    """Tests for SnykOrgSettingsOpenSourceReference."""

    def test_get_model_class_returns_snyk_org_settings_open_source(self) -> None:
        """Test that get_model_class returns SnykOrgSettingsOpenSource."""
        from clearskies_snyk.models.references.snyk_org_settings_open_source_reference import (
            SnykOrgSettingsOpenSourceReference,
        )
        from clearskies_snyk.models.snyk_org_settings_open_source import SnykOrgSettingsOpenSource

        ref = SnykOrgSettingsOpenSourceReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgSettingsOpenSource


class TestSnykOrgSettingsSastReference:
    """Tests for SnykOrgSettingsSastReference."""

    def test_get_model_class_returns_snyk_org_settings_sast(self) -> None:
        """Test that get_model_class returns SnykOrgSettingsSast."""
        from clearskies_snyk.models.references.snyk_org_settings_sast_reference import SnykOrgSettingsSastReference
        from clearskies_snyk.models.snyk_org_settings_sast import SnykOrgSettingsSast

        ref = SnykOrgSettingsSastReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgSettingsSast


class TestSnykOrgUserReference:
    """Tests for SnykOrgUserReference."""

    def test_get_model_class_returns_snyk_org_user(self) -> None:
        """Test that get_model_class returns SnykOrgUser."""
        from clearskies_snyk.models.references.snyk_org_user_reference import SnykOrgUserReference
        from clearskies_snyk.models.snyk_org_user import SnykOrgUser

        ref = SnykOrgUserReference()
        model_class = ref.get_model_class()
        assert model_class is SnykOrgUser


class TestSnykProjectHistoryReference:
    """Tests for SnykProjectHistoryReference."""

    def test_get_model_class_returns_snyk_project_history(self) -> None:
        """Test that get_model_class returns SnykProjectHistory."""
        from clearskies_snyk.models.references.snyk_project_history_reference import SnykProjectHistoryReference
        from clearskies_snyk.models.snyk_project_history import SnykProjectHistory

        ref = SnykProjectHistoryReference()
        model_class = ref.get_model_class()
        assert model_class is SnykProjectHistory


class TestSnykProjectIgnoreReference:
    """Tests for SnykProjectIgnoreReference."""

    def test_get_model_class_returns_snyk_project_ignore(self) -> None:
        """Test that get_model_class returns SnykProjectIgnore."""
        from clearskies_snyk.models.references.snyk_project_ignore_reference import SnykProjectIgnoreReference
        from clearskies_snyk.models.snyk_project_ignore import SnykProjectIgnore

        ref = SnykProjectIgnoreReference()
        model_class = ref.get_model_class()
        assert model_class is SnykProjectIgnore


class TestSnykProjectSbomReference:
    """Tests for SnykProjectSbomReference."""

    def test_get_model_class_returns_snyk_project_sbom(self) -> None:
        """Test that get_model_class returns SnykProjectSbom."""
        from clearskies_snyk.models.references.snyk_project_sbom_reference import SnykProjectSbomReference
        from clearskies_snyk.models.snyk_project_sbom import SnykProjectSbom

        ref = SnykProjectSbomReference()
        model_class = ref.get_model_class()
        assert model_class is SnykProjectSbom


class TestSnykPullRequestTemplateReference:
    """Tests for SnykPullRequestTemplateReference."""

    def test_get_model_class_returns_snyk_pull_request_template(self) -> None:
        """Test that get_model_class returns SnykPullRequestTemplate."""
        from clearskies_snyk.models.references.snyk_pull_request_template_reference import (
            SnykPullRequestTemplateReference,
        )
        from clearskies_snyk.models.snyk_pull_request_template import SnykPullRequestTemplate

        ref = SnykPullRequestTemplateReference()
        model_class = ref.get_model_class()
        assert model_class is SnykPullRequestTemplate


class TestSnykSbomTestReference:
    """Tests for SnykSbomTestReference."""

    def test_get_model_class_returns_snyk_sbom_test(self) -> None:
        """Test that get_model_class returns SnykSbomTest."""
        from clearskies_snyk.models.references.snyk_sbom_test_reference import SnykSbomTestReference
        from clearskies_snyk.models.snyk_sbom_test import SnykSbomTest

        ref = SnykSbomTestReference()
        model_class = ref.get_model_class()
        assert model_class is SnykSbomTest


class TestSnykSlackChannelReference:
    """Tests for SnykSlackChannelReference."""

    def test_get_model_class_returns_snyk_slack_channel(self) -> None:
        """Test that get_model_class returns SnykSlackChannel."""
        from clearskies_snyk.models.references.snyk_slack_channel_reference import SnykSlackChannelReference
        from clearskies_snyk.models.snyk_slack_channel import SnykSlackChannel

        ref = SnykSlackChannelReference()
        model_class = ref.get_model_class()
        assert model_class is SnykSlackChannel


class TestSnykTestJobReference:
    """Tests for SnykTestJobReference."""

    def test_get_model_class_returns_snyk_test_job(self) -> None:
        """Test that get_model_class returns SnykTestJob."""
        from clearskies_snyk.models.references.snyk_test_job_reference import SnykTestJobReference
        from clearskies_snyk.models.snyk_test_job import SnykTestJob

        ref = SnykTestJobReference()
        model_class = ref.get_model_class()
        assert model_class is SnykTestJob
