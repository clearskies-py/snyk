"""Reference to SnykGroupServiceAccount model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_service_account import SnykGroupServiceAccount


class SnykGroupServiceAccountReference(ModelClassReference["SnykGroupServiceAccount"]):
    """Reference to SnykGroupServiceAccount model."""

    def get_model_class(self) -> type["SnykGroupServiceAccount"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_service_account

        return snyk_group_service_account.SnykGroupServiceAccount
