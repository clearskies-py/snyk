"""Snyk SBOM Test model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend


class SnykSbomTest(Model):
    """
    Model for Snyk SBOM Tests.

    This model represents SBOM (Software Bill of Materials) test jobs.
    SBOM tests analyze a provided SBOM document for vulnerabilities.

    Uses the Snyk v2 REST API endpoint: `/orgs/{org_id}/sbom_tests`

    ```python
    import clearskies
    from clearskies_snyk.models import SnykSbomTest

    def my_handler(snyk_sbom_test: SnykSbomTest):
        # Fetch SBOM test status
        test = snyk_sbom_test.find("org_id=org-id-123", "job_id=job-id-456")
        print(f"Test Status: {test.status}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(
        resource_type="sbom_test",
        can_update=False,
        can_delete=False
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/sbom_tests"

    """
    The unique identifier for the SBOM test job.
    """
    id = String()

    """
    The ID of the organization this test belongs to.
    """
    org_id = String(is_searchable=True)

    """
    The status of the SBOM test.
    """
    status = Select(allowed_values=["pending", "processing", "finished", "failed"])

    """
    Timestamp of when the test was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the test was completed.
    """
    finished_at = Datetime()

    """
    The SBOM document to test.
    """
    sbom = Json()

    """
    SBOM format.
    """
    format = Select(
        allowed_values=[
            "cyclonedx1.6+json",
            "cyclonedx1.6+xml",
            "cyclonedx1.5+json",
            "cyclonedx1.5+xml",
            "cyclonedx1.4+json",
            "cyclonedx1.4+xml",
            "spdx2.3+json",
        ],
        is_searchable=True,
        is_temporary=True,
    )

    """
    Exclude certain fields.
    """
    exclude = Select(allowed_values=["licenses"], is_searchable=True, is_temporary=True)

    """
    Include Go module-level dependencies.
    """
    go_module_level = Boolean(is_searchable=True, is_temporary=True)
