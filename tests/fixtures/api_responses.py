"""
Factory functions for creating mock API responses.

This module provides factory classes for generating realistic mock responses
for each Snyk API resource type. These factories are used in tests to create
consistent, valid test data.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from tests.fixtures.schemas import (
    make_jsonapi_response,
    make_pagination_links,
    make_relationship,
    make_resource,
)


def _uuid() -> str:
    """Generate a random UUID string."""
    return str(uuid4())


def _timestamp() -> str:
    """Generate an ISO 8601 timestamp."""
    return datetime.utcnow().isoformat() + "Z"


class OrgResponseFactory:
    """Factory for organization API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        name: str = "Test Organization",
        slug: str = "test-org",
        group_id: str | None = None,
        is_personal: bool = False,
    ) -> dict[str, Any]:
        """
        Create a single organization response.

        Args:
            id: Organization ID (auto-generated if not provided)
            name: Organization name
            slug: URL-friendly slug
            group_id: Parent group ID
            is_personal: Whether this is a personal org

        Returns:
            JSON:API formatted single org response
        """
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="org",
                attributes={
                    "name": name,
                    "slug": slug,
                    "group_id": group_id or _uuid(),
                    "is_personal": is_personal,
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        starting_after: str | None = None,
        group_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of organizations response.

        Args:
            count: Number of organizations to generate
            starting_after: Pagination cursor for next page
            group_id: Common group ID for all orgs

        Returns:
            JSON:API formatted list response with pagination
        """
        orgs = [
            make_resource(
                id=_uuid(),
                type="org",
                attributes={
                    "name": f"Organization {i}",
                    "slug": f"org-{i}",
                    "group_id": group_id or _uuid(),
                    "is_personal": False,
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links("/rest/orgs", starting_after=starting_after)

        return make_jsonapi_response(orgs, links=links)


class GroupResponseFactory:
    """Factory for group API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        name: str = "Test Group",
    ) -> dict[str, Any]:
        """
        Create a single group response.

        Args:
            id: Group ID (auto-generated if not provided)
            name: Group name

        Returns:
            JSON:API formatted single group response
        """
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="group",
                attributes={
                    "name": name,
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        starting_after: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of groups response.

        Args:
            count: Number of groups to generate
            starting_after: Pagination cursor for next page

        Returns:
            JSON:API formatted list response with pagination
        """
        groups = [
            make_resource(
                id=_uuid(),
                type="group",
                attributes={
                    "name": f"Group {i}",
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links("/rest/groups", starting_after=starting_after)

        return make_jsonapi_response(groups, links=links)


class ProjectResponseFactory:
    """Factory for project API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        name: str = "test-project",
        org_id: str | None = None,
        origin: str = "github",
        status: str = "active",
        project_type: str = "npm",
        target_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a single project response.

        Args:
            id: Project ID (auto-generated if not provided)
            name: Project name
            org_id: Parent organization ID
            origin: Project origin (github, gitlab, cli, etc.)
            status: Project status (active, inactive)
            project_type: Project type (npm, pip, maven, etc.)
            target_id: Associated target ID

        Returns:
            JSON:API formatted single project response
        """
        org_id = org_id or _uuid()
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="project",
                attributes={
                    "name": name,
                    "origin": origin,
                    "status": status,
                    "type": project_type,
                    "created": _timestamp(),
                    "target_reference": "main",
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                    "target": make_relationship(target_id or _uuid(), "target"),
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        org_id: str | None = None,
        starting_after: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of projects response.

        Args:
            count: Number of projects to generate
            org_id: Common organization ID for all projects
            starting_after: Pagination cursor for next page

        Returns:
            JSON:API formatted list response with pagination
        """
        org_id = org_id or _uuid()
        projects = [
            make_resource(
                id=_uuid(),
                type="project",
                attributes={
                    "name": f"project-{i}",
                    "origin": "github",
                    "status": "active",
                    "type": "npm",
                    "created": _timestamp(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links(f"/rest/orgs/{org_id}/projects", starting_after=starting_after)

        return make_jsonapi_response(projects, links=links)


class TargetResponseFactory:
    """Factory for target API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        display_name: str = "test-repo",
        org_id: str | None = None,
        origin: str = "github",
        is_private: bool = True,
    ) -> dict[str, Any]:
        """
        Create a single target response.

        Args:
            id: Target ID (auto-generated if not provided)
            display_name: Target display name
            org_id: Parent organization ID
            origin: Target origin
            is_private: Whether the target is private

        Returns:
            JSON:API formatted single target response
        """
        org_id = org_id or _uuid()
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="target",
                attributes={
                    "display_name": display_name,
                    "origin": origin,
                    "is_private": is_private,
                    "created_at": _timestamp(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        org_id: str | None = None,
        starting_after: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of targets response.

        Args:
            count: Number of targets to generate
            org_id: Common organization ID for all targets
            starting_after: Pagination cursor for next page

        Returns:
            JSON:API formatted list response with pagination
        """
        org_id = org_id or _uuid()
        targets = [
            make_resource(
                id=_uuid(),
                type="target",
                attributes={
                    "display_name": f"repo-{i}",
                    "origin": "github",
                    "is_private": True,
                    "created_at": _timestamp(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links(f"/rest/orgs/{org_id}/targets", starting_after=starting_after)

        return make_jsonapi_response(targets, links=links)


class CollectionResponseFactory:
    """Factory for collection API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        name: str = "Test Collection",
        org_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a single collection response.

        Args:
            id: Collection ID (auto-generated if not provided)
            name: Collection name
            org_id: Parent organization ID

        Returns:
            JSON:API formatted single collection response
        """
        org_id = org_id or _uuid()
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="collection",
                attributes={
                    "name": name,
                    "created": _timestamp(),
                    "updated": _timestamp(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        org_id: str | None = None,
        starting_after: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of collections response.

        Args:
            count: Number of collections to generate
            org_id: Common organization ID for all collections
            starting_after: Pagination cursor for next page

        Returns:
            JSON:API formatted list response with pagination
        """
        org_id = org_id or _uuid()
        collections = [
            make_resource(
                id=_uuid(),
                type="collection",
                attributes={
                    "name": f"Collection {i}",
                    "created": _timestamp(),
                    "updated": _timestamp(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links(f"/rest/orgs/{org_id}/collections", starting_after=starting_after)

        return make_jsonapi_response(collections, links=links)


class IssueResponseFactory:
    """Factory for issue API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        title: str = "Test Issue",
        org_id: str | None = None,
        project_id: str | None = None,
        severity: str = "medium",
        status: str = "open",
        issue_type: str = "package_vulnerability",
    ) -> dict[str, Any]:
        """
        Create a single issue response.

        Args:
            id: Issue ID (auto-generated if not provided)
            title: Issue title
            org_id: Parent organization ID
            project_id: Associated project ID
            severity: Issue severity (low, medium, high, critical)
            status: Issue status (open, resolved, ignored)
            issue_type: Type of issue

        Returns:
            JSON:API formatted single issue response
        """
        org_id = org_id or _uuid()
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="issue",
                attributes={
                    "title": title,
                    "effective_severity_level": severity,
                    "status": status,
                    "type": issue_type,
                    "created_at": _timestamp(),
                    "updated_at": _timestamp(),
                    "ignored": False,
                    "key": _uuid(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                    "scan_item": make_relationship(project_id or _uuid(), "project"),
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        org_id: str | None = None,
        starting_after: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of issues response.

        Args:
            count: Number of issues to generate
            org_id: Common organization ID for all issues
            starting_after: Pagination cursor for next page

        Returns:
            JSON:API formatted list response with pagination
        """
        org_id = org_id or _uuid()
        severities = ["low", "medium", "high", "critical"]
        issues = [
            make_resource(
                id=_uuid(),
                type="issue",
                attributes={
                    "title": f"Issue {i}",
                    "effective_severity_level": severities[i % len(severities)],
                    "status": "open",
                    "type": "package_vulnerability",
                    "created_at": _timestamp(),
                    "updated_at": _timestamp(),
                    "ignored": False,
                    "key": _uuid(),
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links(f"/rest/orgs/{org_id}/issues", starting_after=starting_after)

        return make_jsonapi_response(issues, links=links)


class ServiceAccountResponseFactory:
    """Factory for service account API responses."""

    @staticmethod
    def single(
        id: str | None = None,
        name: str = "Test Service Account",
        org_id: str | None = None,
        role_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a single service account response.

        Args:
            id: Service account ID (auto-generated if not provided)
            name: Service account name
            org_id: Parent organization ID
            role_id: Associated role ID

        Returns:
            JSON:API formatted single service account response
        """
        org_id = org_id or _uuid()
        return make_jsonapi_response(
            make_resource(
                id=id or _uuid(),
                type="service_account",
                attributes={
                    "name": name,
                    "auth_type": "api_key",
                    "created_at": _timestamp(),
                    "access_token_ttl_seconds": 3600,
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                    "role": make_relationship(role_id or _uuid(), "role"),
                },
            )
        )

    @staticmethod
    def list(
        count: int = 3,
        org_id: str | None = None,
        starting_after: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a list of service accounts response.

        Args:
            count: Number of service accounts to generate
            org_id: Common organization ID for all service accounts
            starting_after: Pagination cursor for next page

        Returns:
            JSON:API formatted list response with pagination
        """
        org_id = org_id or _uuid()
        service_accounts = [
            make_resource(
                id=_uuid(),
                type="service_account",
                attributes={
                    "name": f"Service Account {i}",
                    "auth_type": "api_key",
                    "created_at": _timestamp(),
                    "access_token_ttl_seconds": 3600,
                },
                relationships={
                    "organization": make_relationship(org_id, "org"),
                },
            )
            for i in range(count)
        ]

        links = make_pagination_links(f"/rest/orgs/{org_id}/service_accounts", starting_after=starting_after)

        return make_jsonapi_response(service_accounts, links=links)
