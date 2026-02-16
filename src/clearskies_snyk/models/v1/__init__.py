"""Snyk v1 API models.

This module contains models that use the Snyk v1 API endpoints.
These models provide access to functionality that is not available
in the v2 REST API.

## Available Models

### Integration Management
- `SnykIntegration`: Manage integrations (GitHub, GitLab, etc.)
- `SnykIntegrationSetting`: Configure integration settings

### Organization
- `SnykOrgV1`: Organization details via v1 API

### Group Management
- `SnykGroupRoleV1`: List roles available in a group
- `SnykGroupTag`: List and manage tags in a group
- `SnykGroupSettings`: View and update group settings

### Webhooks
- `SnykWebhook`: Manage outbound webhooks

### Entitlements
- `SnykEntitlement`: Check organization feature entitlements

### Dependencies & Licenses
- `SnykDependency`: List dependencies across projects
- `SnykLicense`: List licenses across projects

### Import Jobs
- `SnykImportJob`: Track project import job status
- `SnykGitHubImport`: Create import jobs for GitHub/GitHub Enterprise
- `SnykGitLabImport`: Create import jobs for GitLab
- `SnykBitbucketCloudImport`: Create import jobs for Bitbucket Cloud
- `SnykBitbucketServerImport`: Create import jobs for Bitbucket Server
- `SnykAzureReposImport`: Create import jobs for Azure Repos
- `SnykDockerHubImport`: Create import jobs for Docker Hub
- `SnykContainerRegistryImport`: Create import jobs for container registries

## Usage

```python
import clearskies
from clearskies_snyk.models.v1 import (
    SnykWebhook,
    SnykDependency,
    SnykGroupRoleV1,
    SnykGroupTag,
    SnykGroupSettings,
    SnykGitHubImport,
    SnykImportJob,
)

# Build DI container
di = clearskies.di.StandardDependencies()

# List webhooks
webhooks = di.build(SnykWebhook, org_id="my-org-id")
for webhook in webhooks:
    print(webhook.url)

# List dependencies
deps = di.build(SnykDependency, org_id="my-org-id")

# Create import job
github_import = di.build(SnykGitHubImport)
import_job = github_import.create(
    {
        "org_id": "my-org-id",
        "integration_id": "my-integration-id",
        "target": {"owner": "my-org", "name": "my-repo", "branch": "main"},
    }
)

# Check import job status
job_model = di.build(SnykImportJob, org_id="my-org-id", integration_id="my-integration-id")
job = job_model.find(import_job.id)
print(f"Status: {job.status}")
```
"""

from clearskies_snyk.models.v1.snyk_azure_repos_import import SnykAzureReposImport
from clearskies_snyk.models.v1.snyk_bitbucket_cloud_import import SnykBitbucketCloudImport
from clearskies_snyk.models.v1.snyk_bitbucket_server_import import SnykBitbucketServerImport
from clearskies_snyk.models.v1.snyk_container_registry_import import SnykContainerRegistryImport
from clearskies_snyk.models.v1.snyk_dependency import SnykDependency
from clearskies_snyk.models.v1.snyk_dockerhub_import import SnykDockerHubImport
from clearskies_snyk.models.v1.snyk_entitlement import SnykEntitlement
from clearskies_snyk.models.v1.snyk_github_import import SnykGitHubImport
from clearskies_snyk.models.v1.snyk_gitlab_import import SnykGitLabImport
from clearskies_snyk.models.v1.snyk_group_role_v1 import SnykGroupRoleV1
from clearskies_snyk.models.v1.snyk_group_settings import SnykGroupSettings
from clearskies_snyk.models.v1.snyk_group_tag import SnykGroupTag
from clearskies_snyk.models.v1.snyk_import_job import SnykImportJob
from clearskies_snyk.models.v1.snyk_integration import SnykIntegration
from clearskies_snyk.models.v1.snyk_integration_setting import SnykIntegrationSetting
from clearskies_snyk.models.v1.snyk_license import SnykLicense
from clearskies_snyk.models.v1.snyk_org_v1 import SnykOrgV1
from clearskies_snyk.models.v1.snyk_webhook import SnykWebhook

__all__ = [
    "SnykAzureReposImport",
    "SnykBitbucketCloudImport",
    "SnykBitbucketServerImport",
    "SnykContainerRegistryImport",
    "SnykDependency",
    "SnykDockerHubImport",
    "SnykEntitlement",
    "SnykGitHubImport",
    "SnykGitLabImport",
    "SnykGroupRoleV1",
    "SnykGroupSettings",
    "SnykGroupTag",
    "SnykImportJob",
    "SnykIntegration",
    "SnykIntegrationSetting",
    "SnykLicense",
    "SnykOrgV1",
    "SnykWebhook",
]
