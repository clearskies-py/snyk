"""Reference to SnykGroupUser model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_user import SnykGroupUser


class SnykGroupUserReference(ModelClassReference["SnykGroupUser"]):
    """Reference to SnykGroupUser model."""

    def get_model_class(self) -> type["SnykGroupUser"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_user

        return snyk_group_user.SnykGroupUser
