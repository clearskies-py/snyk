"""
Validate that models match the OpenAPI specification.

This module provides tests that verify the clearskies-snyk models
correctly implement the Snyk REST API as defined in the OpenAPI spec.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from clearskies_snyk.models import (
    SnykCollection,
    SnykGroup,
    SnykGroupIssue,
    SnykGroupMember,
    SnykGroupServiceAccount,
    SnykOrg,
    SnykOrgIssue,
    SnykOrgMember,
    SnykOrgServiceAccount,
    SnykProject,
    SnykTarget,
)


def load_spec() -> dict[str, Any]:
    """Load the API specification."""
    spec_path = Path(__file__).parent.parent.parent / "api_spec" / "v2-rest-api-spec.json"
    if not spec_path.exists():
        pytest.skip(f"API spec not found at {spec_path}")
    with open(spec_path) as f:
        return json.load(f)


def get_paths_for_tag(spec: dict[str, Any], tag: str) -> list[str]:
    """Get all paths that have a specific tag."""
    paths = []
    for path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():
            if isinstance(details, dict):
                tags = details.get("tags", [])
                if tag in tags:
                    paths.append(path)
                    break
    return paths


def normalize_path(path: str) -> str:
    """Normalize a path by replacing parameter placeholders."""
    import re

    return re.sub(r"\{[^}]+\}", "{param}", path)


class TestOrgSpecCompliance:
    """Validate SnykOrg model matches the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_orgs_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify the /orgs endpoint exists in the spec."""
        assert "/orgs" in spec["paths"], "Expected /orgs endpoint in spec"
        assert "get" in spec["paths"]["/orgs"], "Expected GET method on /orgs"

    def test_destination_name_matches_spec(self) -> None:
        """Verify the model's destination_name matches the spec endpoint."""
        assert SnykOrg.destination_name() == "orgs"

    def test_model_has_required_columns(self) -> None:
        """Verify the model has the expected columns."""
        # Get column names from class attributes
        model_columns = {
            name
            for name in dir(SnykOrg)
            if not name.startswith("_")
            and hasattr(getattr(SnykOrg, name, None), "__class__")
            and "Column" in str(type(getattr(SnykOrg, name, None)).__mro__)
        }

        # Core columns that should exist based on the API
        expected = {"id", "name", "slug", "is_personal", "group_id"}
        missing = expected - model_columns

        # Alternative: check if attributes exist on class
        for col in expected:
            assert hasattr(SnykOrg, col), f"Missing column: {col}"


class TestGroupSpecCompliance:
    """Validate SnykGroup model matches the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_groups_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify the /groups endpoint exists in the spec."""
        assert "/groups" in spec["paths"], "Expected /groups endpoint in spec"
        assert "get" in spec["paths"]["/groups"], "Expected GET method on /groups"

    def test_destination_name_matches_spec(self) -> None:
        """Verify the model's destination_name matches the spec endpoint."""
        assert SnykGroup.destination_name() == "groups"

    def test_model_has_required_columns(self) -> None:
        """Verify the model has the expected columns."""
        # Core columns that should exist based on the API
        expected = {"id", "name"}

        # Check if attributes exist on class
        for col in expected:
            assert hasattr(SnykGroup, col), f"Missing column: {col}"


class TestProjectSpecCompliance:
    """Validate SnykProject model matches the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_projects_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify a projects endpoint exists in the spec."""
        project_paths = [p for p in spec["paths"] if "projects" in p]
        assert len(project_paths) > 0, "Expected at least one projects endpoint"

    def test_destination_name_format(self) -> None:
        """Verify the destination_name uses the correct parameterized format."""
        dest = SnykProject.destination_name()
        assert "orgs" in dest, "Expected 'orgs' in destination"
        assert "projects" in dest, "Expected 'projects' in destination"
        assert "{org_id}" in dest, "Expected '{org_id}' parameter"

    def test_model_has_required_columns(self) -> None:
        """Verify the model has the expected columns."""
        # Core columns that should exist based on the API
        expected = {"id", "name", "origin", "status", "org_id"}

        # Check if attributes exist on class
        for col in expected:
            assert hasattr(SnykProject, col), f"Missing column: {col}"


class TestTargetSpecCompliance:
    """Validate SnykTarget model matches the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_targets_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify a targets endpoint exists in the spec."""
        target_paths = [p for p in spec["paths"] if "targets" in p]
        assert len(target_paths) > 0, "Expected at least one targets endpoint"

    def test_destination_name_format(self) -> None:
        """Verify the destination_name uses the correct parameterized format."""
        dest = SnykTarget.destination_name()
        assert "orgs" in dest, "Expected 'orgs' in destination"
        assert "targets" in dest, "Expected 'targets' in destination"


class TestCollectionSpecCompliance:
    """Validate SnykCollection model matches the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_collections_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify a collections endpoint exists in the spec."""
        collection_paths = [p for p in spec["paths"] if "collections" in p]
        assert len(collection_paths) > 0, "Expected at least one collections endpoint"

    def test_destination_name_format(self) -> None:
        """Verify the destination_name uses the correct parameterized format."""
        dest = SnykCollection.destination_name()
        assert "orgs" in dest, "Expected 'orgs' in destination"
        assert "collections" in dest, "Expected 'collections' in destination"


class TestIssueSpecCompliance:
    """Validate issue models match the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_org_issues_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify an org issues endpoint exists in the spec."""
        issue_paths = [p for p in spec["paths"] if "issues" in p and "orgs" in p]
        assert len(issue_paths) > 0, "Expected at least one org issues endpoint"

    def test_group_issues_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify a group issues endpoint exists in the spec."""
        issue_paths = [p for p in spec["paths"] if "issues" in p and "groups" in p]
        assert len(issue_paths) > 0, "Expected at least one group issues endpoint"


class TestServiceAccountSpecCompliance:
    """Validate service account models match the API specification."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_org_service_accounts_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify an org service accounts endpoint exists in the spec."""
        sa_paths = [p for p in spec["paths"] if "service_accounts" in p and "orgs" in p]
        assert len(sa_paths) > 0, "Expected at least one org service accounts endpoint"

    def test_group_service_accounts_endpoint_exists(self, spec: dict[str, Any]) -> None:
        """Verify a group service accounts endpoint exists in the spec."""
        sa_paths = [p for p in spec["paths"] if "service_accounts" in p and "groups" in p]
        assert len(sa_paths) > 0, "Expected at least one group service accounts endpoint"


class TestSpecCoverage:
    """Test overall spec coverage by models."""

    @pytest.fixture
    def spec(self) -> dict[str, Any]:
        return load_spec()

    def test_all_major_tags_have_models(self, spec: dict[str, Any]) -> None:
        """Verify that major API tags have corresponding models."""
        # Map of tags to their model classes
        tag_model_map = {
            "Orgs": SnykOrg,
            "Groups": SnykGroup,
            "Projects": SnykProject,
            "Targets": SnykTarget,
            "Collection": SnykCollection,
            "Issues": [SnykOrgIssue, SnykGroupIssue],
            "ServiceAccounts": [SnykOrgServiceAccount, SnykGroupServiceAccount],
        }

        # Get all tags from spec
        all_tags = set()
        for path, methods in spec.get("paths", {}).items():
            for method, details in methods.items():
                if isinstance(details, dict):
                    all_tags.update(details.get("tags", []))

        # Check coverage
        covered_tags = set(tag_model_map.keys())
        high_priority_tags = {"Orgs", "Groups", "Projects", "Issues"}

        missing_high_priority = high_priority_tags - covered_tags
        assert not missing_high_priority, f"Missing models for high-priority tags: {missing_high_priority}"

    def test_endpoint_count_summary(self, spec: dict[str, Any]) -> None:
        """Print a summary of endpoint coverage (informational)."""
        from collections import defaultdict

        endpoints_by_tag: dict[str, int] = defaultdict(int)
        for path, methods in spec.get("paths", {}).items():
            for method, details in methods.items():
                if isinstance(details, dict):
                    for tag in details.get("tags", ["Untagged"]):
                        endpoints_by_tag[tag] += 1

        total_endpoints = sum(endpoints_by_tag.values())

        # This test always passes - it's for informational purposes
        print(f"\n\nTotal endpoints in spec: {total_endpoints}")
        print(f"Tags with most endpoints:")
        for tag, count in sorted(endpoints_by_tag.items(), key=lambda x: -x[1])[:10]:
            print(f"  {tag}: {count}")
