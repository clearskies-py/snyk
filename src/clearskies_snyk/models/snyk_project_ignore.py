"""Snyk Project Ignore model (v1 API).

Note: This model uses the Snyk v1 API. The v2 REST API does not have a direct
equivalent endpoint for project ignores.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykProjectIgnore(Model):
    """
    Model for Snyk Project Ignores (v1 API).

    This model represents ignored issues in a Snyk project.
    Uses the Snyk v1 API endpoint: /org/{orgId}/project/{projectId}/ignores

    ```python
    import clearskies
    from clearskies_snyk.models import SnykProjectIgnore


    def my_handler(snyk_project_ignore: SnykProjectIgnore):
        # Fetch ignores for a project
        ignores = snyk_project_ignore.where("org_id=org-id-123").where("project_id=project-id-456")
        for ignore in ignores:
            print(f"Ignored: {ignore.issue_id} - {ignore.ignored_path}")
    ```
    """

    id_column_name: str = "issue_id"

    backend = SnykV1Backend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/project/{project_id}/ignores"

    """
    The ID of the ignored issue.
    """
    issue_id = String()

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The ID of the group.
    """
    group_id = String()

    """
    The ID of the project.
    """
    project_id = String(is_searchable=True)

    """
    The path that is ignored.
    """
    ignored_path = String()

    """
    The slug of the ignore.
    """
    slug = String()

    """
    The URL of the ignore.
    """
    url = String()

    """
    Group information.
    """
    group = Json()
