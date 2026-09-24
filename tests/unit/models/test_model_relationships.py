"""
Tests for model relationship wiring.

Validates that BelongsToId, BelongsToModel, HasMany, and HasOne columns
are correctly wired on all models that have URL-path FK relationships.
"""

from __future__ import annotations

import pytest


class TestImportSmoke:
    """Smoke test: all models and references import without circular dependency errors."""

    def test_all_models_importable(self) -> None:
        """Import the entire models package without error."""
        from clearskies_snyk import models  # noqa: F401

    def test_all_references_importable(self) -> None:
        """Import the entire references package without error."""
        from clearskies_snyk.models import references  # noqa: F401


# ---------------------------------------------------------------------------
# BelongsToId + BelongsToModel wiring
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "model_path,fk_column,model_column",
    [
        # org_id → SnykOrg
        ("snyk_ai_bom", "org_id", "org"),
        ("snyk_broker_connection", "org_id", "org"),
        ("snyk_collection_relationship_project", "org_id", "org"),
        ("snyk_container_image_target_ref", "org_id", "org"),
        ("snyk_fix_pull_request", "org_id", "org"),
        ("snyk_learn_assignment", "org_id", "org"),
        ("snyk_org_app", "org_id", "org"),
        ("snyk_org_app_bot", "org_id", "org"),
        ("snyk_org_app_install", "org_id", "org"),
        ("snyk_org_export", "org_id", "org"),
        ("snyk_org_member", "org_id", "org"),
        ("snyk_org_settings_open_source", "org_id", "org"),
        ("snyk_org_settings_sast", "org_id", "org"),
        ("snyk_package", "org_id", "org"),
        ("snyk_project_history", "org_id", "org"),
        ("snyk_project_ignore", "org_id", "org"),
        ("snyk_project_sbom", "org_id", "org"),
        ("snyk_sbom_test", "org_id", "org"),
        ("snyk_slack_channel", "org_id", "org"),
        ("snyk_slack_default_notification_settings", "org_id", "org"),
        ("snyk_slack_project_notification_settings", "org_id", "org"),
        ("snyk_test_job", "org_id", "org"),
        # Already-existing org_id BelongsTo relationships (regression guard)
        ("snyk_cloud_environment", "org_id", "org"),
        ("snyk_cloud_resource", "org_id", "org"),
        ("snyk_cloud_scan", "org_id", "org"),
        ("snyk_collection", "org_id", "org"),
        ("snyk_container_image", "org_id", "org"),
        ("snyk_org_audit_log", "org_id", "org"),
        ("snyk_org_invite", "org_id", "org"),
        ("snyk_org_issue", "org_id", "org"),
        # snyk_org_membership: org column is Json (API response field), no BelongsToModel
        ("snyk_org_policy", "org_id", "org"),
        ("snyk_org_policy_event", "org_id", "org"),
        ("snyk_org_service_account", "org_id", "org"),
        ("snyk_org_settings_iac", "org_id", "org"),
        ("snyk_org_user", "org_id", "org"),
        ("snyk_project", "org_id", "org"),
        ("snyk_target", "org_id", "org"),
        # group_id → SnykGroup
        ("snyk_group_app_install", "group_id", "group"),
        ("snyk_group_export", "group_id", "group"),
        ("snyk_group_member", "group_id", "group"),
        ("snyk_group_org_membership", "group_id", "group"),
        ("snyk_group_settings_iac", "group_id", "group"),
        ("snyk_group_sso_connection", "group_id", "group"),
        ("snyk_group_sso_connection_user", "group_id", "group"),
        ("snyk_pull_request_template", "group_id", "group"),
        # Already-existing group_id BelongsTo relationships (regression guard)
        ("snyk_group_audit_log", "group_id", "group"),
        ("snyk_group_issue", "group_id", "group"),
        # snyk_group_membership: group column is Json (API response field), no BelongsToModel
        ("snyk_group_policy", "group_id", "group"),
        ("snyk_group_service_account", "group_id", "group"),
        ("snyk_group_user", "group_id", "group"),
        ("snyk_org", "group_id", "group"),
        # project_id → SnykProject
        ("snyk_fix_pull_request", "project_id", "project"),
        ("snyk_project_history", "project_id", "project"),
        ("snyk_project_ignore", "project_id", "project"),
        ("snyk_project_sbom", "project_id", "project"),
        # target_id → SnykTarget (regression guard)
        ("snyk_project", "target_id", "target"),
        # tenant_id → SnykTenant
        ("snyk_broker_connection_integration", "tenant_id", "tenant"),
        ("snyk_broker_deployment", "tenant_id", "tenant"),
    ],
)
def test_belongs_to_relationship_exists(model_path: str, fk_column: str, model_column: str) -> None:
    """BelongsToId FK column and matching BelongsToModel column both exist."""
    import importlib

    from clearskies.columns import BelongsToId, BelongsToModel

    module = importlib.import_module(f"clearskies_snyk.models.{model_path}")
    model_class = next(
        cls
        for name, cls in vars(module).items()
        if isinstance(cls, type)
        and issubclass(cls, __import__("clearskies", fromlist=["Model"]).Model)
        and cls.__name__ != "Model"
    )

    fk_col = getattr(model_class, fk_column, None)
    assert fk_col is not None, f"{model_class.__name__}.{fk_column} not found"
    assert isinstance(fk_col, BelongsToId), (
        f"{model_class.__name__}.{fk_column} should be BelongsToId, got {type(fk_col).__name__}"
    )

    rel_col = getattr(model_class, model_column, None)
    assert rel_col is not None, f"{model_class.__name__}.{model_column} not found"
    assert isinstance(rel_col, BelongsToModel), (
        f"{model_class.__name__}.{model_column} should be BelongsToModel, got {type(rel_col).__name__}"
    )


# ---------------------------------------------------------------------------
# HasMany / HasOne on parent models
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "model_path,model_class_name,rel_name,rel_type_name",
    [
        # SnykOrg new HasMany/HasOne
        ("snyk_org", "SnykOrg", "apps", "HasMany"),
        ("snyk_org", "SnykOrg", "app_bots", "HasMany"),
        ("snyk_org", "SnykOrg", "app_installs", "HasMany"),
        ("snyk_org", "SnykOrg", "audit_logs", "HasMany"),
        ("snyk_org", "SnykOrg", "exports", "HasMany"),
        ("snyk_org", "SnykOrg", "members", "HasMany"),
        ("snyk_org", "SnykOrg", "policies", "HasMany"),
        ("snyk_org", "SnykOrg", "users", "HasMany"),
        ("snyk_org", "SnykOrg", "cloud_environments", "HasMany"),
        ("snyk_org", "SnykOrg", "cloud_resources", "HasMany"),
        ("snyk_org", "SnykOrg", "cloud_scans", "HasMany"),
        ("snyk_org", "SnykOrg", "settings_open_source", "HasOne"),
        ("snyk_org", "SnykOrg", "settings_sast", "HasOne"),
        ("snyk_org", "SnykOrg", "test_jobs", "HasMany"),
        ("snyk_org", "SnykOrg", "sbom_tests", "HasMany"),
        ("snyk_org", "SnykOrg", "learn_assignments", "HasMany"),
        ("snyk_org", "SnykOrg", "broker_connections", "HasMany"),
        # SnykOrg existing HasMany (regression guard)
        ("snyk_org", "SnykOrg", "projects", "HasMany"),
        ("snyk_org", "SnykOrg", "targets", "HasMany"),
        ("snyk_org", "SnykOrg", "collections", "HasMany"),
        ("snyk_org", "SnykOrg", "memberships", "HasMany"),
        ("snyk_org", "SnykOrg", "service_accounts", "HasMany"),
        ("snyk_org", "SnykOrg", "issues", "HasMany"),
        ("snyk_org", "SnykOrg", "settings_iac", "HasOne"),
        # SnykGroup new HasMany/HasOne
        ("snyk_group", "SnykGroup", "app_installs", "HasMany"),
        ("snyk_group", "SnykGroup", "audit_logs", "HasMany"),
        ("snyk_group", "SnykGroup", "exports", "HasMany"),
        ("snyk_group", "SnykGroup", "members", "HasMany"),
        ("snyk_group", "SnykGroup", "org_memberships", "HasMany"),
        ("snyk_group", "SnykGroup", "policies", "HasMany"),
        ("snyk_group", "SnykGroup", "sso_connections", "HasMany"),
        ("snyk_group", "SnykGroup", "users", "HasMany"),
        ("snyk_group", "SnykGroup", "settings_iac", "HasOne"),
        ("snyk_group", "SnykGroup", "pull_request_template", "HasOne"),
        # SnykGroup existing HasMany (regression guard)
        ("snyk_group", "SnykGroup", "orgs", "HasMany"),
        ("snyk_group", "SnykGroup", "memberships", "HasMany"),
        ("snyk_group", "SnykGroup", "service_accounts", "HasMany"),
        ("snyk_group", "SnykGroup", "issues", "HasMany"),
        # SnykProject new HasMany/HasOne
        ("snyk_project", "SnykProject", "history", "HasMany"),
        ("snyk_project", "SnykProject", "ignores", "HasMany"),
        ("snyk_project", "SnykProject", "sbom", "HasOne"),
        ("snyk_project", "SnykProject", "issues", "HasMany"),
        # Nested-resource HasMany
        ("snyk_group_membership", "SnykGroupMembership", "orgs", "HasMany"),
        ("snyk_container_image", "SnykContainerImage", "target_refs", "HasMany"),
        ("snyk_group_sso_connection", "SnykGroupSsoConnection", "users", "HasMany"),
        ("snyk_org_policy", "SnykOrgPolicy", "events", "HasMany"),
        ("snyk_self_app", "SnykSelfApp", "sessions", "HasMany"),
        ("snyk_org", "SnykOrg", "invites", "HasMany"),
        ("snyk_org", "SnykOrg", "ai_boms", "HasMany"),
        # SnykTarget existing HasMany (regression guard)
        ("snyk_target", "SnykTarget", "projects", "HasMany"),
        # SnykTenant new HasMany
        ("snyk_tenant", "SnykTenant", "broker_deployments", "HasMany"),
        # SnykTenant existing HasMany (regression guard)
        ("snyk_tenant", "SnykTenant", "memberships", "HasMany"),
        ("snyk_tenant", "SnykTenant", "roles", "HasMany"),
    ],
)
def test_parent_has_relationship(model_path: str, model_class_name: str, rel_name: str, rel_type_name: str) -> None:
    """Parent model has the expected HasMany or HasOne column."""
    import importlib

    from clearskies.columns import HasMany, HasOne

    rel_type = HasMany if rel_type_name == "HasMany" else HasOne

    module = importlib.import_module(f"clearskies_snyk.models.{model_path}")
    model_class = getattr(module, model_class_name)

    rel_col = getattr(model_class, rel_name, None)
    assert rel_col is not None, f"{model_class_name}.{rel_name} not found"
    assert isinstance(rel_col, rel_type), (
        f"{model_class_name}.{rel_name} should be {rel_type_name}, got {type(rel_col).__name__}"
    )
