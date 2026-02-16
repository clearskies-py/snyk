"""Snyk Learn Assignment model."""

from typing import Self

from clearskies import Model
from clearskies.columns import Boolean, Datetime, Json, String

from clearskies_snyk.backends import SnykBackend


class SnykLearnAssignment(Model):
    """
    Model for Snyk Learn Assignments.

    This model represents lesson assignments for users in an organization.
    Uses the Snyk v2 REST API endpoint: /orgs/{org_id}/learn/assignments

    ```python
    import clearskies
    from clearskies_snyk.models import SnykLearnAssignment


    def my_handler(snyk_learn_assignment: SnykLearnAssignment):
        # List assignments for an organization
        assignments = snyk_learn_assignment.where("org_id=org-id-123")
        for assignment in assignments:
            print(f"Assignment: {assignment.lesson_title} for {assignment.user_email}")
    ```
    """

    id_column_name: str = "id"

    # Map 'type' to 'assignment_type' to avoid shadowing Python's builtin type
    backend = SnykBackend(
        api_to_model_map={
            "type": "assignment_type",
        }
    )

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "orgs/{org_id}/learn/assignments"

    """
    The unique identifier for the assignment.
    """
    id = String()

    """
    The ID of the organization.
    """
    org_id = String(is_searchable=True)

    """
    The type of resource (lesson_assignment).
    """
    assignment_type = String()

    """
    The ID of the user assigned.
    """
    user_id = String()

    """
    The email of the user assigned.
    """
    user_email = String()

    """
    The ID of the lesson assigned.
    """
    lesson_id = String()

    """
    The title of the lesson.
    """
    lesson_title = String()

    """
    The slug of the lesson.
    """
    lesson_slug = String()

    """
    The due date for the assignment.
    """
    due_date = Datetime()

    """
    The date the assignment was completed.
    """
    completed_date = Datetime()

    """
    The ID of the user who created the assignment.
    """
    assigning_user_id = String()

    """
    The email of the user who created the assignment.
    """
    assigning_user_email = String()

    """
    Whether the assignment is active.
    """
    is_active = Boolean()

    """
    Learning path IDs associated with this assignment.
    """
    learning_path_ids = Json()

    """
    Learning program ID if part of a program.
    """
    learning_program_id = String()

    """
    The date the lesson was created.
    """
    lesson_created_at = Datetime()

    """
    The date the lesson was last updated.
    """
    lesson_updated_at = Datetime()

    """
    The date the assignment was created.
    """
    created_at = Datetime()

    """
    The date the assignment was last updated.
    """
    updated_at = Datetime()
