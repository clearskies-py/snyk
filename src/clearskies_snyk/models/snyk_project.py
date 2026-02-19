"""Snyk Project model."""

from typing import Self

from clearskies import Model
from clearskies.columns import BelongsToId, BelongsToModel, Boolean, Datetime, Json, Select, String

from clearskies_snyk.backends import SnykBackend
from clearskies_snyk.columns import ProjectTagList
from clearskies_snyk.models.references import snyk_org_reference, snyk_target_reference


class SnykProject(Model):
    """
    Model for Snyk Projects.

    This model represents projects in Snyk. Projects are the primary unit of scanning
    in Snyk and are associated with a target (repository, container image, etc.).

    ```python
    import clearskies
    from clearskies_snyk.models import SnykProject


    def my_handler(snyk_project: SnykProject):
        # Fetch all projects for an organization
        projects = snyk_project.where("org_id=org-id-123")
        for project in projects:
            print(f"Project: {project.name} ({project.status})")

        # Find a specific project
        project = projects.find("id=project-id-456")
        print(project.name)

        # Access parent organization
        print(f"Org: {project.org.name}")

        # Access parent target
        print(f"Target: {project.target.display_name}")
    ```
    """

    id_column_name: str = "id"

    # orgs/{org_id}/projects: query=True, create=False, update=True, delete=True
    # Map API field 'type' to 'project_type' to avoid shadowing builtin
    backend = SnykBackend(
        api_to_model_map={
            "type": "project_type",
        },
        can_create=False,
        resource_type="project",
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/projects"

    """
    The unique identifier for the project.
    """
    id = String()

    """
    The ID of the organization this project belongs to.
    """
    org_id = BelongsToId(
        snyk_org_reference.SnykOrgReference,
        is_searchable=True,
    )

    """
    The parent organization this project belongs to.

    BelongsTo relationship to SnykOrg.
    """
    org = BelongsToModel("org_id")

    """
    The ID of the group this project belongs to.
    """
    group_id = String(is_searchable=True)

    """
    The human-readable name of the project.
    """
    name = String()

    """
    The origin of the project (e.g., github, gitlab, cli).
    """
    origin = String()

    """
    Search parameter: Filter by origins.
    """
    origins = String(is_searchable=True, is_temporary=True)

    """
    The type of the project (e.g., npm, pip, maven).
    Mapped from API field 'type' to avoid shadowing builtin.
    """
    project_type = String()

    """
    Search parameter: Filter by types.
    """
    types = String(is_searchable=True, is_temporary=True)

    """
    Build arguments for the project.
    """
    build_args = Json()

    """
    Timestamp of when the project was created.
    """
    created = Datetime()

    """
    The business criticality of the project.
    """
    business_criticality = Select(
        allowed_values=[
            "critical",
            "high",
            "medium",
            "low",
        ],
    )

    """
    The environment of the project.
    """
    environment = Select(
        allowed_values=[
            "frontend",
            "backend",
            "internal",
            "mobile",
            "saas",
            "onprem",
            "hosted",
            "distributed",
        ],
    )

    """
    The lifecycle stage of the project.
    """
    lifecycle = Select(
        allowed_values=[
            "production",
            "development",
            "sandbox",
        ],
    )

    """
    Whether the project is read-only.
    """
    read_only = Boolean()

    """
    Project settings.
    """
    settings = Json()

    """
    The status of the project.
    """
    status = Select(
        allowed_values=[
            "active",
            "inactive",
        ],
    )

    """
    Tags associated with the project.
    """
    tags = ProjectTagList()

    """
    The target file for the project.
    """
    target_file = String()

    """
    The target reference (branch, tag, etc.).
    """
    target_reference = String()

    """
    The target runtime for the project.
    """
    target_runtime = String()

    """
    The ID of the user who imported the project.
    """
    importer_id = String()

    """
    The ID of the project owner.
    """
    owner_id = String()

    """
    The ID of the target this project belongs to.
    """
    target_id = BelongsToId(
        snyk_target_reference.SnykTargetReference,
    )

    """
    The parent target this project belongs to.

    BelongsTo relationship to SnykTarget.
    """
    target = BelongsToModel("target_id")
