"""Snyk Target model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Datetime, HasMany, Json, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.models.references import snyk_org_reference, snyk_project_reference


class SnykTarget(Model):
    """
    Model for Snyk Targets.

    This model represents targets in Snyk. Targets are the source of projects
    (e.g., a repository, container image, or other scannable resource).

    ```python
    from clearskies_snyk.models import SnykTarget

    # Fetch all targets for an organization
    targets = SnykTarget().where("org_id=org-id-123")
    for target in targets:
        print(f"Target: {target.display_name}")

    # Find a specific target
    target = targets.find("id=target-id-456")
    print(target.display_name)

    # Access parent organization
    print(f"Org: {target.org.name}")

    # Access related projects
    for project in target.projects:
        print(f"  Project: {project.name}")
    ```
    """

    id_column_name: str = "id"

    backend = SnykBackend()

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/targets"

    """
    The unique identifier for the target.
    """
    id = String()

    """
    The ID of the organization this target belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        readable_parent_columns=["id", "name", "slug"],
        is_searchable=True,
    )

    """
    The parent organization this target belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The display name of the target.
    """
    display_name = String()

    """
    The URL of the target (if applicable).
    """
    url = String()

    """
    Whether the target is private.
    """
    is_private = String()

    """
    The origin of the target (e.g., github, gitlab).
    """
    origin = String()

    """
    Timestamp of when the target was created.
    """
    created_at = Datetime()

    """
    Additional target attributes.
    """
    attributes = Json()

    """
    Related projects for this target.

    HasMany relationship to SnykProject.
    """
    projects = HasMany(
        snyk_project_reference.SnykProjectReference,
        foreign_column_name="target_id",
    )
