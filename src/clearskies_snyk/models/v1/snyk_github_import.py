"""Snyk GitHub Import model (v1 API).

This model is used to create import jobs for GitHub and GitHub Enterprise repositories.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1ImportBackend


class SnykGitHubImport(Model):
    """
    Model for creating GitHub/GitHub Enterprise import jobs (v1 API).

    This model creates import jobs that import GitHub repositories into Snyk for scanning.
    After creation, use SnykImportJob to check the import status.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/integrations/{integrationId}/import

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykGitHubImport, SnykImportJob

    # Build the DI container
    di = clearskies.di.StandardDependencies()

    # Create an import job for a GitHub repository
    github_import = di.build(SnykGitHubImport)
    import_job = github_import.create(
        {
            "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
            "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
            "target": {"owner": "my-org", "name": "my-repo", "branch": "main"},
            "files": [{"path": "package.json"}, {"path": "backend/requirements.txt"}],
            "exclusion_globs": "fixtures,tests,__tests__,node_modules",
        }
    )

    # Check import job status
    import_job_model = di.build(
        SnykImportJob, org_id=import_job.org_id, integration_id=import_job.integration_id
    )
    job = import_job_model.find(import_job.id)
    print(f"Status: {job.status}")
    for log in job.logs:
        print(f"  {log['name']}: {log['status']}")
    ```

    ## Target Object

    The target object specifies the GitHub repository to import:
    - `owner` (required): The account owner of the repository
    - `name` (required): The name of the repository
    - `branch` (required): The branch to import (usually the default branch)

    ## Files Array

    Optional list of specific manifest files to import. Each file object has:
    - `path`: Relative path to the manifest file (e.g., "package.json", "pom.xml")

    If not specified, Snyk will auto-detect all supported manifest files.

    ## Exclusion Globs

    A comma-separated list of up to 10 folder names to exclude from scanning
    (each folder name must not exceed 100 characters). If not specified, it will
    default to "fixtures, tests, __tests__, node_modules". If an empty string is
    provided, no folders will be excluded.

    ## Required Permissions

    - `View Organization`
    - `Add Project`
    - `Test Project`

    ## Notes

    - Requires a Snyk personal access/API token for GitHub Cloud integrations
    - Contact support if you need to import a non-default branch
    """

    id_column_name: str = "id"
    backend = SnykV1ImportBackend(can_update=False, can_delete=False, can_query=False)

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
    Object with: owner (required), name (required), branch (required).
    Example: {"owner": "my-org", "name": "my-repo", "branch": "main"}
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
