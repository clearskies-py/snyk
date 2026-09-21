"""Reference to SnykGroupSsoConnectionUser model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_sso_connection_user import SnykGroupSsoConnectionUser


class SnykGroupSsoConnectionUserReference(ModelClassReference["SnykGroupSsoConnectionUser"]):
    """Reference to SnykGroupSsoConnectionUser model."""

    def get_model_class(self) -> type["SnykGroupSsoConnectionUser"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_sso_connection_user

        return snyk_group_sso_connection_user.SnykGroupSsoConnectionUser
