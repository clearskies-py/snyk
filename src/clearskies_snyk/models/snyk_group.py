"""Snyk Group model."""

from typing import Self

from clearskies import Model
from clearskies.columns import HasMany, HasOne, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import (
    snyk_group_issue_reference,
    snyk_group_membership_reference,
    snyk_group_role_v1_reference,
    snyk_group_service_account_reference,
    snyk_group_settings_reference,
    snyk_group_tag_reference,
    snyk_org_reference,
)


class SnykGroup(Model):
    """
    Model for Snyk Groups.

    This model represents groups in Snyk. Groups are the top-level container
    that can contain multiple organizations.

    ```python
    from clearskies_snyk.models import SnykGroup

    # Fetch all groups
    groups = SnykGroup()
    for group in groups:
        print(f"Group: {group.name}")

    # Find a specific group
    group = groups.find("id=group-id-123")
    print(group.name)

    # Access related organizations
    for org in group.orgs:
        print(f"  Org: {org.name}")

    # Access group memberships
    for membership in group.memberships:
        print(f"  Member: {membership.name}")
    ```
    """

    id_column_name: str = "id"

    # groups: query=True, create=False, update=False, delete=False
    backend = SnykBackend(can_create=False, can_update=False, can_delete=False)

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups"

    """
    The unique identifier for the group.
    """
    id = String()

    """
    The human-readable name of the group.
    """
    name = String()

    """
    Related organizations for this group.

    HasMany relationship to SnykOrg.
    """
    orgs = HasMany(
        snyk_org_reference.SnykOrgReference,
        foreign_column_name="group_id",
    )

    """
    Group memberships.

    HasMany relationship to SnykGroupMembership.
    """
    memberships = HasMany(
        snyk_group_membership_reference.SnykGroupMembershipReference,
        foreign_column_name="group_id",
    )

    """
    Group service accounts.

    HasMany relationship to SnykGroupServiceAccount.
    """
    service_accounts = HasMany(
        snyk_group_service_account_reference.SnykGroupServiceAccountReference,
        foreign_column_name="group_id",
    )

    """
    Group issues.

    HasMany relationship to SnykGroupIssue.
    """
    issues = HasMany(
        snyk_group_issue_reference.SnykGroupIssueReference,
        foreign_column_name="group_id",
    )

    # V1 API relationships (these use the Snyk v1 API)

    """
    Group settings (v1 API).

    HasOne relationship to SnykGroupSettings.
    """
    settings = HasOne(
        snyk_group_settings_reference.SnykGroupSettingsReference,
        foreign_column_name="group_id",
    )

    """
    Tags in this group (v1 API).

    HasMany relationship to SnykGroupTag.
    """
    tags = HasMany(
        snyk_group_tag_reference.SnykGroupTagReference,
        foreign_column_name="group_id",
    )

    """
    Roles available in this group (v1 API).

    HasMany relationship to SnykGroupRoleV1.
    """
    roles = HasMany(
        snyk_group_role_v1_reference.SnykGroupRoleV1Reference,
        foreign_column_name="group_id",
    )
