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
