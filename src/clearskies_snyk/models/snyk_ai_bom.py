"""Snyk AI-BOM model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Json, String

from clearskies_snyk.backends import SnykBackend


class SnykAiBom(Model):
    """
    Model for Snyk AI-BOM (AI Bill of Materials).

    This model represents an AI-BOM that can be created from source code or SCM targets.
    AI-BOMs are created asynchronously via background jobs.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/ai_boms

    ```python
    from clearskies_snyk.models import SnykAiBom

    # Create an AI-BOM (triggers async job)
    ai_bom = SnykAiBom()
    ai_bom.save({"org_id": "org-123", "bundle_id": "sha256-hash-of-bundle"})
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(api_to_model_map={"type": "bom_type"}, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/ai_boms"

    # Columns based on the response schema
    id = String()  # Job ID
    org_id = String(is_searchable=True)
    bom_type = String()  # Mapped from 'type', e.g., "ai_bom_job"

    # Attributes from JobAttributes
    status = String()  # processing, finished, errored

    # Request attributes for file bundle
    bundle_id = String()  # sha256 hash of the uploaded bundle

    # Request attributes for SCM bundle
    target_id = String()  # Target ID for SCM-based AI-BOM
    target_version = String()  # Branch or commit hash to scan

    # For upload endpoint
    repo_name = String()  # Repository name (required for upload endpoint)

    # Relationships
    relationships = Json()  # Contains ai_bom relationship data
