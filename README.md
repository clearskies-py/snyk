# clearskies-snyk

A [clearskies](https://github.com/cmancone/clearskies) module for interacting with the [Snyk API](https://docs.snyk.io/snyk-api).

This module provides pre-built models and backends for seamless integration with both the Snyk REST API and the legacy v1 API, allowing you to easily query and manage Snyk resources like organizations, projects, groups, issues, and more.

## Features

- **REST API Backend** (`SnykBackend`): Full support for Snyk's JSON:API-compliant REST API with cursor-based pagination
- **V1 API Backend** (`SnykV1Backend`): Support for Snyk's legacy v1 API with offset-based pagination
- **75+ Pre-built Models**: Ready-to-use models for organizations, projects, groups, issues, policies, service accounts, and more
- **Automatic Authentication**: Configurable via environment variables with support for secret managers
- **Automatic Pagination**: Seamlessly iterate through large result sets

## Installation

```bash
pip install clearskies-snyk
```

Or with uv:

```bash
uv add clearskies-snyk
```

## Quick Start

### Authentication

Set up authentication using environment variables:

```bash
# Option 1: Direct API key
export SNYK_AUTH_KEY=your-snyk-api-key

# Option 2: Secret manager path (recommended for production)
export SNYK_AUTH_SECRET_PATH=/path/to/secret
```

### Basic Usage

```python
import clearskies
from clearskies_snyk.models import SnykOrg, SnykProject, SnykGroup

# List all organizations
for org in SnykOrg():
    print(f"Org: {org.name} ({org.slug})")

# Get projects for an organization
projects = SnykProject(org_id="your-org-id")
for project in projects:
    print(f"Project: {project.name} - {project.project_type}")

# List groups
for group in SnykGroup():
    print(f"Group: {group.name}")
```

### Working with Issues

```python
from clearskies_snyk.models import SnykOrgIssue, SnykGroupIssue

# Get issues for an organization
org_issues = SnykOrgIssue(org_id="your-org-id")
for issue in org_issues:
    print(f"Issue: {issue.title} - Severity: {issue.effective_severity_level}")

# Get issues across a group
group_issues = SnykGroupIssue(group_id="your-group-id")
for issue in group_issues:
    print(f"Issue: {issue.title}")
```

### Using the V1 API

Some endpoints are only available through the legacy v1 API:

```python
from clearskies_snyk.models.v1 import SnykIntegration, SnykWebhook, SnykLicense

# List integrations for an organization
integrations = SnykIntegration(org_id="your-org-id")
for integration in integrations:
    print(f"Integration: {integration.name} ({integration.integration_type})")

# List webhooks
webhooks = SnykWebhook(org_id="your-org-id")
for webhook in webhooks:
    print(f"Webhook: {webhook.url}")
```

### Custom Backend Configuration

```python
import clearskies
from clearskies_snyk.backends import SnykBackend

# Custom authentication
backend = SnykBackend(
    authentication=clearskies.authentication.SecretBearer(
        environment_key="MY_SNYK_KEY",
        header_prefix="token ",
    )
)

# Custom API version
backend = SnykBackend(api_version="2024-10-15")
```

## Available Models

### REST API Models

| Category | Models |
|----------|--------|
| **Organizations** | `SnykOrg`, `SnykOrgMember`, `SnykOrgMembership`, `SnykOrgUser`, `SnykOrgInvite` |
| **Projects** | `SnykProject`, `SnykProjectHistory`, `SnykProjectIgnore`, `SnykProjectSbom` |
| **Groups** | `SnykGroup`, `SnykGroupMember`, `SnykGroupMembership`, `SnykGroupUser`, `SnykGroupOrgMembership` |
| **Issues** | `SnykOrgIssue`, `SnykGroupIssue` |
| **Policies** | `SnykOrgPolicy`, `SnykOrgPolicyEvent`, `SnykGroupPolicy` |
| **Service Accounts** | `SnykOrgServiceAccount`, `SnykGroupServiceAccount` |
| **Apps** | `SnykOrgApp`, `SnykOrgAppBot`, `SnykOrgAppInstall`, `SnykGroupAppInstall`, `SnykSelfApp` |
| **Cloud** | `SnykCloudEnvironment`, `SnykCloudResource`, `SnykCloudScan` |
| **Containers** | `SnykContainerImage`, `SnykCustomBaseImage` |
| **Settings** | `SnykOrgSettingsIac`, `SnykOrgSettingsSast`, `SnykOrgSettingsOpenSource`, `SnykGroupSettingsIac` |
| **Tenants** | `SnykTenant`, `SnykTenantMembership`, `SnykTenantRole` |
| **Other** | `SnykCollection`, `SnykTarget`, `SnykPackage`, `SnykAiBom`, `SnykLearnAssignment`, and more |

### V1 API Models

| Model | Description |
|-------|-------------|
| `SnykIntegration` | SCM and CI/CD integrations |
| `SnykIntegrationSetting` | Integration configuration settings |
| `SnykWebhook` | Webhook configurations |
| `SnykLicense` | License information |
| `SnykDependency` | Project dependencies |
| `SnykEntitlement` | Organization entitlements |
| `SnykGroupRoleV1` | Group roles (v1 format) |
| `SnykGroupSettings` | Group settings |
| `SnykGroupTag` | Group tags |
| `SnykImportJob` | Project import jobs |

## Development

To set up your development environment:

```bash
# Install uv if not already installed
pip install uv

# Create a virtual environment and install all dependencies
uv sync

# Install dev dependencies
uv pip install .[dev]

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

## Documentation

For full API documentation, visit the [Snyk API Documentation](https://docs.snyk.io/snyk-api).

## License

MIT License - see [LICENSE](LICENSE) for details.
