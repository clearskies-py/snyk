"""Snyk Bitbucket Cloud Import model (v1 API).

This model is used to create import jobs for Bitbucket Cloud repositories.
"""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykV1ImportBackend

from .snyk_target_import import SnykTargetImport


class SnykBitbucketCloudImport(SnykTargetImport):
    """
    Model for creating Bitbucket Cloud import jobs (v1 API).

    This model creates import jobs that import Bitbucket Cloud repositories into Snyk for scanning.
    After creation, use SnykImportJob to check the import status.

    Uses the Snyk v1 API endpoint: POST /org/{orgId}/integrations/{integrationId}/import

    ## Usage

    ```python
    import clearskies
    from clearskies_snyk.models.v1 import SnykBitbucketCloudImport, SnykImportJob


    def my_handler(
        snyk_bitbucket_cloud_import: SnykBitbucketCloudImport, snyk_import_job: SnykImportJob
    ):
        # Create an import job for a Bitbucket Cloud repository
        import_response = snyk_bitbucket_cloud_import.create(
            {
                "org_id": "4a18d42f-0706-4ad0-b127-24078731fbed",
                "integration_id": "9a3e5d90-b782-468a-a042-9a2073736f0b",
                "target": {"owner": "my-workspace-id", "name": "my-repo"},
                "files": [{"path": "package.json"}],
                "exclusion_globs": "fixtures,tests",
            }
        )

        # Check import job status
        org_id = import_response.org_id
        integration_id = import_response.integration_id
        job = snyk_import_job.find(
            f"org_id={org_id}&integration_id={integration_id}&id={import_response.id}"
        )
    ```

    ## Target Object

    The target object specifies the Bitbucket Cloud repository to import:
    - `owner` (required): The Workspace ID (not the workspace name)
    - `name` (required): The name of the repository

    ## Files Array

    Optional list of specific manifest files to import. Each file object has:
    - `path`: Relative path to the manifest file (e.g., "package.json", "pom.xml")

    If not specified, Snyk will auto-detect all supported manifest files.

    ## Exclusion Globs

    A comma-separated list of up to 10 folder names to exclude from scanning
    (each folder name must not exceed 100 characters). If not specified, defaults to
    "fixtures, tests, __tests__, node_modules". Use empty string to exclude no folders.

    ## Required Permissions

    - `View Organization`
    - `Add Project`
    - `Test Project`
    """

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
