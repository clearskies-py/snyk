"""Reference to SnykGroupSsoConnection model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_sso_connection import SnykGroupSsoConnection


class SnykGroupSsoConnectionReference(ModelClassReference["SnykGroupSsoConnection"]):
    """Reference to SnykGroupSsoConnection model."""

    def get_model_class(self) -> type["SnykGroupSsoConnection"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_sso_connection

        return snyk_group_sso_connection.SnykGroupSsoConnection
