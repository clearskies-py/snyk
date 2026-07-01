"""Reference to SnykGroupRoleV1 model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_group_role_v1 import SnykGroupRoleV1


class SnykGroupRoleV1Reference(ModelClassReference["SnykGroupRoleV1"]):
    """Reference to SnykGroupRoleV1 model."""

    def get_model_class(self) -> type["SnykGroupRoleV1"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_group_role_v1

        return snyk_group_role_v1.SnykGroupRoleV1
