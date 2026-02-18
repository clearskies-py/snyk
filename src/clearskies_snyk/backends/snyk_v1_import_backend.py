"""Snyk v1 API backend for import job creation.

This backend extends SnykV1Backend to handle the special case where the Snyk
import API returns a 201 status with an empty body and the job ID in the Location header.
"""

from typing import Any

import requests
from clearskies import Model
from clearskies.query.result.record_query_result import RecordQueryResult

from clearskies_snyk.backends import SnykV1Backend


class SnykV1ImportBackend(SnykV1Backend):
    """
    Backend for Snyk import job creation (v1 API).

    This backend extends SnykV1Backend to handle the special response format
    used by the import endpoints. When creating an import job, the Snyk API
    returns a 201 status with an empty body and places the job ID in the
    `Location` response header.

    ## Usage

    This backend is used internally by the import models (SnykGitHubImport, etc.)
    and should not need to be used directly.

    ## Response Handling

    When a POST request is made to create an import job:
    - Status: 201 Created
    - Body: Empty (`{}`)
    - Header: `Location: URL for the status API call of the import`

    The job ID is extracted from the Location header URL, which has the format:
    `/org/{orgId}/integrations/{integrationId}/import/{jobId}`
    """

    def create(self, data: dict[str, Any], model: Model) -> RecordQueryResult:
        """
        Create a new import job.

        This overrides the default create method to handle the special case where
        the Snyk import API returns an empty body and places the job ID in the
        Location header.

        Args:
            data: The data to create the import job with
            model: The model instance

        Returns:
            RecordQueryResult containing the job ID and routing parameters

        Raises:
            ValueError: If the Location header is missing or malformed
        """
        data = {**data}
        url, used_routing_parameters = self.create_url(data, model)
        request_method = self.create_method(data, model)
        for parameter in used_routing_parameters:
            del data[parameter]

        response = self.execute_request(url, request_method, json=data, headers=self.headers)

        # The import API always returns a 201 with empty body and job ID in Location header
        # According to API spec, the response content is always empty and only the Location header is provided
        location = response.headers.get("Location", "")

        if not location:
            raise ValueError(
                "Snyk API import endpoint returned no Location header. "
                "According to API specification, the import endpoint must return a Location header with the job ID. "
                f"Response status: {response.status_code}, Body: {response.text[:200] if response.text else 'empty'}"
            )

        # Extract job ID from Location URL
        # Format:  /org/{orgId}/integrations/{integrationId}/import/{jobId}
        # Or full: https://api.snyk.io/v1/org/{orgId}/integrations/{integrationId}/import/{jobId}
        parts = location.rstrip("/").split("/")

        try:
            # Find the 'import' segment and get the next part as job_id
            import_index = parts.index("import")
            if import_index + 1 < len(parts):
                job_id = parts[import_index + 1]
            else:
                raise ValueError

            # Extract org_id and integration_id from the URL
            org_index = parts.index("org")
            integrations_index = parts.index("integrations")

            if org_index + 1 < len(parts) and integrations_index + 1 < len(parts):
                org_id = parts[org_index + 1]
                integration_id = parts[integrations_index + 1]
            else:
                raise ValueError

        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Could not extract job ID from Location header: {location}. "
                f"Expected format: /org/{{orgId}}/integrations/{{integrationId}}/import/{{jobId}}"
            ) from e

        # Return the job data with routing parameters
        record = {
            "job_id": job_id,
            "org_id": org_id,
            "integration_id": integration_id,
        }

        return RecordQueryResult(record=record)
