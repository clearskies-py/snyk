"""Snyk Group Policy model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_group_reference


class SnykGroupPolicy(Model):
    """
    Model for Snyk Group Policies.

    This model represents policies at the group level in Snyk.
    Group policies can be used to define rules for ignoring, annotating,
    or overriding severity of security issues.

    Uses the Snyk v2 REST API endpoint: /groups/{group_id}/policies

    ```python
    import clearskies
    from clearskies_snyk.models import SnykGroupPolicy


    def my_handler(snyk_group_policy: SnykGroupPolicy):
        # Fetch all policies for a group
        policies = snyk_group_policy.where("group_id=group-id-123")
        for policy in policies:
            print(f"Policy: {policy.name} ({policy.action_type})")

        # Access the parent group
        print(f"Group: {policy.group.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/{group_id}/policies"

    """
    The unique identifier for the policy.
    """
    id = String()

    """
    The ID of the group this policy belongs to.
    """
    group_id = BelongsToId(
        snyk_group_reference.SnykGroupReference,
        is_searchable=True,
    )

    """
    The parent group this policy belongs to.

    BelongsTo relationship to SnykGroup.
    """
    group = BelongsToModel("group_id")

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
            "annotation",
            "severity-override",
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
