"""Snyk Bitbucket Server Import model (v1 API).

This model is used to create import jobs for Bitbucket Server repositories.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1Backend


class SnykBitbucketServerImport(Model):
    """
    Model for creating Bitbucket Server import jobs (v1 API).

    This model creates import jobs that import Bitbucket Server repositories into Snyk for scanning.
    After creation, use SnykImportJob to check the import status.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/integrations/{integrationId}/import

    ## Usage

    ```python
    from clearskies_snyk.models.v1 import SnykBitbucketServerImport, SnykImportJob

    # Create an import job for a Bitbucket Server repository
    import_response = SnykBitbucketServerImport().create(
        {
            "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
            "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
            "target": {
                "project_key": "SNYK_REPOS",
                "repo_slug": "test",
                "branch": "main",
                "name": "Custom Project Name",  # optional
            },
            "files": [{"path": "package.json"}],
            "exclusion_globs": "fixtures,tests",
        }
    )

    # Check import job status
    job = SnykImportJob().find(
        f"org_id={org_id}&integration_id={integration_id}&id={import_response.id}"
    )
    ```

    ## Target Object

    The target object specifies the Bitbucket Server repository to import:
    - `project_key` (required): The project key in Bitbucket Server
    - `repo_slug` (required): The slug of the repository
    - `name` (optional): Custom name for the project in Snyk
    - `branch` (optional): Target branch name

    ## Files Array

    Optional list of specific manifest files to import. Each file object has:
    - `path`: Relative path to the manifest file (e.g., "package.json", "pom.xml")

    If not specified, Snyk will auto-detect all supported manifest files.

    ## Exclusion Globs

    A comma-separated list of up to 10 folder names to exclude from scanning.
    If not specified, defaults to "fixtures, tests, __tests__, node_modules".
    Use empty string to exclude no folders.

    ## Required Permissions

    - `View Organization`
    - `Add Project`
    - `Test Project`
    """

    id_column_name: str = "id"
    backend = SnykV1Backend(can_update=False, can_delete=False, can_query=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations/{integration_id}/import"

    """
    The unique identifier for the organization (required for routing).
    """
    org_id = String(is_searchable=True)

    """
    The unique identifier for the integration (required for routing).
    This can be found on the Integration page in the Settings area.
    """
    integration_id = String(is_searchable=True)

    """
    The target repository to import.
    Object with: project_key (required), repo_slug (required), name (optional), branch (optional).
    Example: {"project_key": "SNYK_REPOS", "repo_slug": "test", "branch": "main"}
    """
    target = Json()

    """
    Optional array of specific manifest files to import.
    Each file object has a 'path' field.
    Example: [{"path": "package.json"}, {"path": "requirements.txt"}]
    """
    files = Json()

    """
    Comma-separated list of up to 10 folder names to exclude from scanning.
    Default: "fixtures, tests, __tests__, node_modules"
    Use empty string to exclude no folders.
    """
    exclusion_globs = String()
