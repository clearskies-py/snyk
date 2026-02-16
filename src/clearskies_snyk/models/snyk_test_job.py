"""Snyk Test Job model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykTestJob(Model):
    """
    Model for Snyk Test Job.

    This model represents a test job that tracks the status of an asynchronous test.
    Tests are created via the Test API and their status can be polled using this endpoint.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/test_jobs/{job_id}

    ```python
    import clearskies
    from clearskies_snyk.models import SnykTestJob


    def my_handler(snyk_test_job: SnykTestJob):
        # Get test job status
        job = snyk_test_job.find("org_id=org-123&job_id=job-456")
        print(f"Job status: {job.status}")
        if job.status == "finished":
            print(f"Test ID: {job.test_id}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend(api_to_model_map={"type": "job_type"}, can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/test_jobs"

    # Columns based on JobData schema
    id = String()  # Job ID (UUID)
    org_id = String(is_searchable=True)
    job_id = String(is_searchable=True)  # Alias for id in path
    job_type = String()  # Mapped from 'type', e.g., "test_jobs"

    # Attributes from JobAttributes
    status = String()  # pending, started, finished, errored
    created_at = Datetime()

    # Relationships - contains test reference when job is finished
    relationships = Json()  # Contains test relationship with id and type
    test_id = String()  # Extracted from relationships.test.data.id when finished
