"""Snyk Org Policy model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference


class SnykOrgPolicy(Model):
    """
    Model for Snyk Organization Policies.

    This model represents policies at the organization level in Snyk.
    Org policies are used for Code Consistent Ignores.

    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/policies

    ```python
    from clearskies_snyk.models import SnykOrgPolicy

    # Fetch all policies for an organization
    policies = SnykOrgPolicy().where("org_id=org-id-123")
    for policy in policies:
        print(f"Policy: {policy.name} ({policy.action_type})")

    # Access the parent organization
    print(f"Org: {policy.org.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/policies"

    """
    The unique identifier for the policy.
    """
    id = String()

    """
    The ID of the organization this policy belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this policy belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The name of the policy.
    """
    name = String()

    """
    The type of action for the policy.
    """
    action_type = Select(
        allowed_values=[
            "ignore",
        ],
    )

    """
    The action configuration for the policy.
    """
    action = Json()

    """
    The conditions group defining when the policy applies.
    """
    conditions_group = Json()

    """
    The review status of the policy.
    """
    review = Select(
        allowed_values=[
            "pending",
            "approved",
            "rejected",
            "not-required",
        ],
    )

    """
    Timestamp of when the policy was created.
    """
    created_at = Datetime()

    """
    Timestamp of when the policy was last updated.
    """
    updated_at = Datetime()

    """
    Information about who created the policy.
    """
    created_by = Json()
