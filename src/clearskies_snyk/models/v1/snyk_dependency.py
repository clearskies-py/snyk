"""Snyk Dependency model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have
a direct equivalent for listing dependencies across an organization.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Integer, Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykDependency(Model):
    """
    Model for Snyk Dependencies (v1 API).

    This model represents dependencies (packages/modules) that your projects
    depend on. It provides information about the dependency including version,
    licenses, and associated vulnerabilities.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/dependencies

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykDependency

    # Fetch all dependencies for an organization
    dependencies = SnykDependency().where("org_id=org-id-123")
    for dep in dependencies:
        print(f"{dep.name}@{dep.version}: {dep.issues_critical} critical issues")
    ```

    ## Rate Limits

    Current rate limit is up to 150 requests per minute, per user.

    ## Required Permissions

    - `View Organization`
    - `View Project`
    - `View Project Snapshot`
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_update=False, can_delete=False, can_query=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/dependencies"

    """
    The unique identifier for the dependency (e.g., 'gulp@3.9.1').
    """
    id = String()

    """
    The ID of the organization this dependency belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The name of the package.
    """
    name = String()

    """
    The version of the package.
    """
    version = String()

    """
    The latest version available for the package.
    """
    latest_version = String()

    """
    The timestamp for when the latest version was published.
    """
    latest_version_published_date = String()

    """
    The timestamp for when the package was first published.
    """
    first_published_date = String()

    """
    True if the latest version is marked as deprecated.
    """
    is_deprecated = Boolean()

    """
    The version numbers that are marked as deprecated.
    """
    deprecated_versions = Json()

    """
    Identifiers of dependencies with issues that are depended upon.
    """
    dependencies_with_issues = Json()

    """
    The package type/manager (e.g., 'npm', 'maven', 'pip').
    """
    dependency_type = String()

    """
    The number of critical severity issues in this dependency.
    """
    issues_critical = Integer()

    """
    The number of high severity issues in this dependency.
    """
    issues_high = Integer()

    """
    The number of medium severity issues in this dependency.
    """
    issues_medium = Integer()

    """
    The number of low severity issues in this dependency.
    """
    issues_low = Integer()

    """
    The licenses of the dependency.
    Each license has: id, title, license type.
    """
    licenses = Json()

    """
    The projects which depend on this dependency.
    Each project has: id, name.
    """
    projects = Json()
