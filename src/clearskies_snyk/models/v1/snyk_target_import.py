"""Snyk GitLab Import model (v1 API).

This model is used to create import jobs for GitLab repositories.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1ImportBackend


class SnykTargetImport(Model):
    """
    Model for creating GitLab import jobs (v1 API).

    This model creates import jobs that import GitLab repositories into Snyk for scanning.
    After creation, use SnykImportJob to check the import status.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/integrations/{integrationId}/import

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykGitLabImport, SnykImportJob


    def my_handler(snyk_gitlab_import: SnykGitLabImport, snyk_import_job: SnykImportJob):
        # Create an import job for a GitLab repository
        import_response = snyk_gitlab_import.create(
            {
                "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
                "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
                "target": {"id": 12345, "branch": "develop"},
                "files": [{"path": "package.json"}, {"path": "backend/requirements.txt"}],
                "exclusion_globs": "fixtures,tests,node_modules",
            }
        )

        # The job ID is returned in the response
        job_id = import_response.id
        org_id = import_response.org_id
        integration_id = import_response.integration_id

        # Check import job status
        job = snyk_import_job.find(f"org_id={org_id}&integration_id={integration_id}&id={job_id}")
        print(f"Status: {job.status}")
    ```

    ## Target Object

    The target object specifies the GitLab repository to import:
    - `id` (required): The numeric ID of the GitLab repository
    - `branch` (required): The branch to import

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

    id_column_name: str = "job_id"
    backend = SnykV1ImportBackend(can_update=False, can_delete=False, can_query=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "org/{org_id}/integrations/{integration_id}/import"

    """
    The Snyk id for the import job, returned in the Location header of the API response when creating an import job."""
    job_id = String()

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
    Object with: id (required, numeric), branch (required).
    Example: {"id": 12345, "branch": "develop"}
    """
    target = Json()
