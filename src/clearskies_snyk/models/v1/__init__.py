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
- `SnykImportJob`: Track project import jobs

## Usage

```python
from clearskies_snyk.models.v1 import (
    SnykWebhook,
    SnykDependency,
    SnykGroupRoleV1,
    SnykGroupTag,
    SnykGroupSettings,
)

# List webhooks
webhooks = SnykWebhook().where("org_id=my-org-id")

# List dependencies
deps = SnykDependency().where("org_id=my-org-id")

# List group roles
roles = SnykGroupRoleV1().where("group_id=my-group-id")

# List group tags
tags = SnykGroupTag().where("group_id=my-group-id")

# Get group settings
settings = SnykGroupSettings().find("my-group-id")
```
"""

from clearskies_snyk.models.v1.snyk_dependency import SnykDependency
from clearskies_snyk.models.v1.snyk_entitlement import SnykEntitlement
from clearskies_snyk.models.v1.snyk_group_role_v1 import SnykGroupRoleV1
from clearskies_snyk.models.v1.snyk_group_settings import SnykGroupSettings
from clearskies_snyk.models.v1.snyk_group_tag import SnykGroupTag
from clearskies_snyk.models.v1.snyk_import_job import SnykImportJob
from clearskies_snyk.models.v1.snyk_integration import SnykIntegration
from clearskies_snyk.models.v1.snyk_integration_setting import SnykIntegrationSetting
from clearskies_snyk.models.v1.snyk_license import SnykLicense
from clearskies_snyk.models.v1.snyk_org_v1 import SnykOrgV1
from clearskies_snyk.models.v1.snyk_v1_model import SnykV1Model
from clearskies_snyk.models.v1.snyk_webhook import SnykWebhook

__all__ = [
    "SnykDependency",
    "SnykEntitlement",
    "SnykGroupRoleV1",
    "SnykGroupSettings",
    "SnykGroupTag",
    "SnykImportJob",
    "SnykIntegration",
    "SnykIntegrationSetting",
    "SnykLicense",
    "SnykOrgV1",
    "SnykV1Model",
    "SnykWebhook",
]
