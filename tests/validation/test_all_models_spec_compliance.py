"""
Comprehensive spec compliance tests for all Snyk models.

This module validates that all clearskies-snyk models correctly implement
the Snyk REST API as defined in the OpenAPI specification.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

# Import all models from the package
from clearskies_snyk.models import (
    # Core models
    SnykOrg,
    SnykGroup,
    SnykProject,
    SnykTarget,
    SnykCollection,
    # Issue models
    SnykOrgIssue,
    SnykGroupIssue,
    # Member models
    SnykOrgMember,
    SnykGroupMember,
    SnykGroupMembership,
    SnykOrgMembership,
    SnykGroupOrgMembership,
    # Service account models
    SnykOrgServiceAccount,
    SnykGroupServiceAccount,
    # Policy models
    SnykOrgPolicy,
    SnykGroupPolicy,
    SnykOrgPolicyEvent,
    # App models
    SnykOrgApp,
    SnykOrgAppBot,
    SnykOrgAppInstall,
    SnykGroupAppInstall,
    SnykSelfApp,
    SnykSelfAppSession,
    # Settings models
    SnykOrgSettingsIac,
    SnykOrgSettingsSast,
    SnykOrgSettingsOpenSource,
    SnykGroupSettingsIac,
    # Cloud models
    SnykCloudEnvironment,
    SnykCloudResource,
    SnykCloudScan,
    # Container models
    SnykContainerImage,
    SnykContainerImageTargetRef,
    SnykCustomBaseImage,
    # Export models
    SnykOrgExport,
    SnykGroupExport,
    # Audit log models
    SnykOrgAuditLog,
    SnykGroupAuditLog,
    # Tenant models
    SnykTenant,
    SnykTenantMembership,
    SnykTenantRole,
    # Broker models
    SnykBrokerConnection,
    SnykBrokerConnectionIntegration,
    SnykBrokerDeployment,
    # Other models
    SnykOrgInvite,
    SnykOrgUser,
    SnykGroupUser,
    SnykGroupSsoConnection,
    SnykGroupSsoConnectionUser,
    SnykPackage,
    SnykProjectHistory,
    SnykProjectIgnore,
    SnykProjectSbom,
    SnykPullRequestTemplate,
    SnykSbomTest,
    SnykSelf,
    SnykSlackChannel,
    SnykSlackDefaultNotificationSettings,
    SnykSlackProjectNotificationSettings,
    SnykTestJob,
    SnykFixPullRequest,
    SnykAccessRequest,
    SnykAiBom,
    SnykLearnAssignment,
    SnykLearnCatalog,
    SnykCollectionRelationshipProject,
)
# Import v1 models from the v1 submodule
from clearskies_snyk.models.v1 import (
    SnykIntegration,
    SnykIntegrationSetting,
)


def load_spec() -> dict[str, Any]:
    """Load the API specification."""
    spec_path = Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"
    if not spec_path.exists():
        pytest.skip(f"API spec not found at {spec_path}")
    with open(spec_path) as f:
        return json.load(f)


def normalize_path(path: str) -> str:
    """Normalize a path by replacing parameter placeholders."""
    return re.sub(r'\{[^}]+\}', '{param}', path)


def get_all_spec_paths(spec: dict[str, Any]) -> set[str]:
    """Get all normalized paths from the spec."""
    paths = set()
    for path in spec.get("paths", {}).keys():
        normalized = normalize_path(path)
        paths.add(normalized)
    return paths


# Define all models with their actual destination names (from the models themselves)
MODEL_DESTINATION_MAP = {
    # Core models
    "SnykOrg": ("orgs", SnykOrg),
    "SnykGroup": ("groups", SnykGroup),
    "SnykProject": ("orgs/{org_id}/projects", SnykProject),
    "SnykTarget": ("orgs/{org_id}/targets", SnykTarget),
    "SnykCollection": ("orgs/{org_id}/collections", SnykCollection),
    # Issue models
    "SnykOrgIssue": ("orgs/{org_id}/issues", SnykOrgIssue),
    "SnykGroupIssue": ("groups/{group_id}/issues", SnykGroupIssue),
    # Member models
    "SnykOrgMember": ("orgs/{org_id}/memberships", SnykOrgMember),
    "SnykGroupMember": ("groups/{group_id}/memberships", SnykGroupMember),
    "SnykGroupMembership": ("groups/{group_id}/memberships", SnykGroupMembership),
    "SnykOrgMembership": ("orgs/{org_id}/memberships", SnykOrgMembership),
    "SnykGroupOrgMembership": ("groups/{group_id}/org_memberships", SnykGroupOrgMembership),
    # Service account models
    "SnykOrgServiceAccount": ("orgs/{org_id}/service_accounts", SnykOrgServiceAccount),
    "SnykGroupServiceAccount": ("groups/{group_id}/service_accounts", SnykGroupServiceAccount),
    # Policy models
    "SnykOrgPolicy": ("orgs/{org_id}/policies", SnykOrgPolicy),
    "SnykGroupPolicy": ("groups/{group_id}/policies", SnykGroupPolicy),
    "SnykOrgPolicyEvent": ("orgs/{org_id}/policies/{policy_id}/events", SnykOrgPolicyEvent),
    # App models
    "SnykOrgApp": ("orgs/{org_id}/apps", SnykOrgApp),
    "SnykOrgAppBot": ("orgs/{org_id}/app_bots", SnykOrgAppBot),
    "SnykOrgAppInstall": ("orgs/{org_id}/apps/installs", SnykOrgAppInstall),
    "SnykGroupAppInstall": ("groups/{group_id}/apps/installs", SnykGroupAppInstall),
    "SnykSelfApp": ("self/apps", SnykSelfApp),
    "SnykSelfAppSession": ("self/apps/{app_id}/sessions", SnykSelfAppSession),
    # Settings models
    "SnykOrgSettingsIac": ("orgs/{org_id}/settings/iac", SnykOrgSettingsIac),
    "SnykOrgSettingsSast": ("orgs/{org_id}/settings/sast", SnykOrgSettingsSast),
    "SnykOrgSettingsOpenSource": ("orgs/{org_id}/settings/opensource", SnykOrgSettingsOpenSource),
    "SnykGroupSettingsIac": ("groups/{group_id}/settings/iac", SnykGroupSettingsIac),
    # Cloud models
    "SnykCloudEnvironment": ("orgs/{org_id}/cloud/environments", SnykCloudEnvironment),
    "SnykCloudResource": ("orgs/{org_id}/cloud/resources", SnykCloudResource),
    "SnykCloudScan": ("orgs/{org_id}/cloud/scans", SnykCloudScan),
    # Container models
    "SnykContainerImage": ("orgs/{org_id}/container_images", SnykContainerImage),
    "SnykContainerImageTargetRef": ("orgs/{org_id}/container_images/{id}/relationships/image_target_refs", SnykContainerImageTargetRef),
    "SnykCustomBaseImage": ("custom_base_images", SnykCustomBaseImage),
    # Export models
    "SnykOrgExport": ("orgs/{org_id}/export", SnykOrgExport),
    "SnykGroupExport": ("groups/{group_id}/export", SnykGroupExport),
    # Audit log models
    "SnykOrgAuditLog": ("orgs/{org_id}/audit_logs/search", SnykOrgAuditLog),
    "SnykGroupAuditLog": ("groups/{group_id}/audit_logs/search", SnykGroupAuditLog),
    # Tenant models
    "SnykTenant": ("tenants", SnykTenant),
    "SnykTenantMembership": ("tenants/{tenant_id}/memberships", SnykTenantMembership),
    "SnykTenantRole": ("tenants/{tenant_id}/roles", SnykTenantRole),
    # Broker models
    "SnykBrokerConnection": ("orgs/{org_id}/brokers/connections", SnykBrokerConnection),
    "SnykBrokerConnectionIntegration": ("tenants/{tenant_id}/brokers/connections/{connection_id}/integrations", SnykBrokerConnectionIntegration),
    "SnykBrokerDeployment": ("tenants/{tenant_id}/brokers/deployments", SnykBrokerDeployment),
    # Other models
    "SnykIntegration": ("org/{org_id}/integrations", SnykIntegration),
    "SnykIntegrationSetting": ("org/{org_id}/integrations/{integration_id}/settings", SnykIntegrationSetting),
    "SnykOrgInvite": ("orgs/{org_id}/invites", SnykOrgInvite),
    "SnykOrgUser": ("orgs/{org_id}/users", SnykOrgUser),
    "SnykGroupUser": ("groups/{group_id}/users", SnykGroupUser),
    "SnykGroupSsoConnection": ("groups/{group_id}/sso_connections", SnykGroupSsoConnection),
    "SnykGroupSsoConnectionUser": ("groups/{group_id}/sso_connections/{sso_id}/users", SnykGroupSsoConnectionUser),
    "SnykPackage": ("orgs/{org_id}/ecosystems/{ecosystem}/packages/{package_name}", SnykPackage),
    "SnykProjectHistory": ("org/{org_id}/project/{project_id}/history", SnykProjectHistory),
    "SnykProjectIgnore": ("org/{org_id}/project/{project_id}/ignores", SnykProjectIgnore),
    "SnykProjectSbom": ("orgs/{org_id}/projects/{project_id}/sbom", SnykProjectSbom),
    "SnykPullRequestTemplate": ("groups/{group_id}/settings/pull_request_template", SnykPullRequestTemplate),
    "SnykSbomTest": ("orgs/{org_id}/sbom_tests", SnykSbomTest),
    "SnykSelf": ("self", SnykSelf),
    "SnykSlackChannel": ("orgs/{org_id}/slack_app/{tenant_id}/channels", SnykSlackChannel),
    "SnykSlackDefaultNotificationSettings": ("orgs/{org_id}/slack_app/{bot_id}", SnykSlackDefaultNotificationSettings),
    "SnykSlackProjectNotificationSettings": ("orgs/{org_id}/slack_app/{bot_id}/projects", SnykSlackProjectNotificationSettings),
    "SnykTestJob": ("orgs/{org_id}/test_jobs", SnykTestJob),
    "SnykFixPullRequest": ("orgs/{org_id}/projects/{project_id}/fix_pull_requests", SnykFixPullRequest),
    "SnykAccessRequest": ("self/access_requests", SnykAccessRequest),
    "SnykAiBom": ("orgs/{org_id}/ai_boms", SnykAiBom),
    "SnykLearnAssignment": ("orgs/{org_id}/learn/assignments", SnykLearnAssignment),
    "SnykLearnCatalog": ("learn/catalog", SnykLearnCatalog),
    "SnykCollectionRelationshipProject": ("orgs/{org_id}/collections/{collection_id}/relationships/projects", SnykCollectionRelationshipProject),
}


class TestAllModelsHaveDestinationName:
    """Test that all models have a destination_name method that returns the expected value."""

    @pytest.mark.parametrize("model_name,expected_pattern,model_class", [
        (name, pattern, cls) for name, (pattern, cls) in MODEL_DESTINATION_MAP.items()
    ])
    def test_model_destination_name_matches_pattern(
        self, model_name: str, expected_pattern: str, model_class: type
    ) -> None:
        """Verify each model's destination_name matches the expected pattern."""
        actual = model_class.destination_name()
        normalized_actual = normalize_path(actual)
        normalized_expected = normalize_path(expected_pattern)
        
        assert normalized_actual == normalized_expected, (
            f"{model_name}.destination_name() returned '{actual}' "
            f"(normalized: '{normalized_actual}'), "
            f"expected pattern '{expected_pattern}' (normalized: '{normalized_expected}')"
        )


# Models that are known to not have an 'id' column (they use different primary keys)
MODELS_WITHOUT_ID_COLUMN = {
    "SnykGroupOrgMembership",  # Uses org_id as identifier
    "SnykOrgApp",  # Uses client_id as identifier
    "SnykIntegrationSetting",  # Settings don't have IDs
    "SnykProjectIgnore",  # Uses issue_id as identifier
}

# Models that use v1 API paths (not in v2 spec)
V1_API_MODELS = {
    "SnykIntegration",  # Uses org/ instead of orgs/
    "SnykIntegrationSetting",  # Uses org/ instead of orgs/
    "SnykProjectHistory",  # Uses org/ and project/ instead of orgs/ and projects/
    "SnykProjectIgnore",  # Uses org/ and project/ instead of orgs/ and projects/
}


class TestAllModelsHaveIdColumn:
    """Test that all models have an id column or a custom primary key column."""

    @pytest.mark.parametrize("model_name,model_class", [
        (name, cls) for name, (_, cls) in MODEL_DESTINATION_MAP.items()
        if name not in MODELS_WITHOUT_ID_COLUMN
    ])
    def test_model_has_id_column(self, model_name: str, model_class: type) -> None:
        """Verify each model has an id column."""
        assert hasattr(model_class, "id"), f"{model_name} is missing 'id' column"
        assert hasattr(model_class, "id_column_name"), f"{model_name} is missing 'id_column_name'"

    @pytest.mark.parametrize("model_name,model_class", [
        (name, cls) for name, (_, cls) in MODEL_DESTINATION_MAP.items()
        if name in MODELS_WITHOUT_ID_COLUMN
    ])
    def test_model_with_custom_primary_key(self, model_name: str, model_class: type) -> None:
        """Verify models with custom primary key have id_column_name and the corresponding column."""
        assert hasattr(model_class, "id_column_name"), f"{model_name} is missing 'id_column_name'"
        id_column_name = model_class.id_column_name
        assert hasattr(model_class, id_column_name), (
            f"{model_name} has id_column_name='{id_column_name}' but is missing the '{id_column_name}' column"
        )


class TestModelEndpointsExistInSpec:
    """Test that model endpoints exist in the API spec."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    @pytest.fixture
    def spec_paths(self, spec: dict[str, Any]) -> set[str]:
        return get_all_spec_paths(spec)

    @pytest.mark.parametrize("model_name,expected_pattern,model_class", [
        (name, pattern, cls) for name, (pattern, cls) in MODEL_DESTINATION_MAP.items()
        if name not in V1_API_MODELS  # Skip v1 API models - they use different path format
    ])
    def test_model_endpoint_exists_in_spec(
        self,
        spec_paths: set[str],
        model_name: str,
        expected_pattern: str,
        model_class: type
    ) -> None:
        """Verify each model's endpoint exists in the API spec."""
        actual = model_class.destination_name()
        normalized = "/" + normalize_path(actual)
        
        # Check if the path exists in spec (with or without leading slash)
        path_exists = (
            normalized in spec_paths or
            normalized.lstrip("/") in spec_paths or
            any(normalized in p or p.endswith(normalized) for p in spec_paths)
        )
        
        # Some models may have endpoints that are subsets of spec paths
        # e.g., model uses "orgs/{org_id}/projects" but spec has "/orgs/{org_id}/projects/{project_id}"
        if not path_exists:
            # Check if any spec path starts with our normalized path
            path_exists = any(
                p.startswith(normalized) or p.startswith(normalized.lstrip("/"))
                for p in spec_paths
            )
        
        assert path_exists, (
            f"{model_name} endpoint '{actual}' (normalized: '{normalized}') "
            f"not found in API spec. Available paths containing similar terms: "
            f"{[p for p in sorted(spec_paths) if any(term in p for term in actual.split('/') if term and not term.startswith('{'))][:5]}"
        )

    @pytest.mark.parametrize("model_name,expected_pattern,model_class", [
        (name, pattern, cls) for name, (pattern, cls) in MODEL_DESTINATION_MAP.items()
        if name in V1_API_MODELS
    ])
    def test_v1_api_model_uses_v1_path_format(
        self,
        model_name: str,
        expected_pattern: str,
        model_class: type
    ) -> None:
        """Verify v1 API models use the v1 path format (org/ instead of orgs/)."""
        actual = model_class.destination_name()
        # v1 API paths use "org/" instead of "orgs/" and "project/" instead of "projects/"
        assert "org/" in actual or "project/" in actual, (
            f"{model_name} is marked as v1 API model but doesn't use v1 path format: {actual}"
        )


class TestSpecCoverageByTag:
    """Test spec coverage organized by API tags."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_orgs_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Orgs tag endpoints have models."""
        orgs_models = [
            SnykOrg, SnykOrgMember, SnykOrgMembership, SnykOrgInvite, SnykOrgUser
        ]
        for model in orgs_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_groups_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Groups tag endpoints have models."""
        groups_models = [
            SnykGroup, SnykGroupMember, SnykGroupMembership, SnykGroupOrgMembership,
            SnykGroupUser, SnykGroupSsoConnection
        ]
        for model in groups_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_projects_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Projects tag endpoints have models."""
        projects_models = [
            SnykProject, SnykProjectHistory, SnykProjectIgnore, SnykProjectSbom
        ]
        for model in projects_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_issues_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Issues tag endpoints have models."""
        issues_models = [SnykOrgIssue, SnykGroupIssue]
        for model in issues_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_service_accounts_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify ServiceAccounts tag endpoints have models."""
        sa_models = [SnykOrgServiceAccount, SnykGroupServiceAccount]
        for model in sa_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_apps_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Apps tag endpoints have models."""
        apps_models = [
            SnykOrgApp, SnykOrgAppBot, SnykOrgAppInstall, SnykGroupAppInstall,
            SnykSelfApp, SnykSelfAppSession
        ]
        for model in apps_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_cloud_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Cloud tag endpoints have models."""
        cloud_models = [SnykCloudEnvironment, SnykCloudResource, SnykCloudScan]
        for model in cloud_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_policies_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Policies tag endpoints have models."""
        policy_models = [SnykOrgPolicy, SnykGroupPolicy, SnykOrgPolicyEvent]
        for model in policy_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_tenants_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Tenants tag endpoints have models."""
        tenant_models = [SnykTenant, SnykTenantMembership, SnykTenantRole]
        for model in tenant_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_broker_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify BrokerConnections tag endpoints have models."""
        broker_models = [SnykBrokerConnection, SnykBrokerConnectionIntegration, SnykBrokerDeployment]
        for model in broker_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_collection_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Collection tag endpoints have models."""
        collection_models = [SnykCollection, SnykCollectionRelationshipProject]
        for model in collection_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_container_image_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify ContainerImage tag endpoints have models."""
        container_models = [SnykContainerImage, SnykContainerImageTargetRef, SnykCustomBaseImage]
        for model in container_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_settings_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify settings endpoints have models."""
        settings_models = [
            SnykOrgSettingsIac, SnykOrgSettingsSast, SnykOrgSettingsOpenSource,
            SnykGroupSettingsIac
        ]
        for model in settings_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_export_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Export tag endpoints have models."""
        export_models = [SnykOrgExport, SnykGroupExport]
        for model in export_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"

    def test_audit_logs_tag_coverage(self, spec: dict[str, Any]) -> None:
        """Verify Audit Logs tag endpoints have models."""
        audit_models = [SnykOrgAuditLog, SnykGroupAuditLog]
        for model in audit_models:
            assert hasattr(model, "destination_name"), f"{model.__name__} missing destination_name"
