"""Reference to SnykGroupAppInstall model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_app_install import SnykGroupAppInstall


class SnykGroupAppInstallReference(ModelClassReference["SnykGroupAppInstall"]):
    """Reference to SnykGroupAppInstall model."""

    def get_model_class(self) -> type["SnykGroupAppInstall"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_app_install

        return snyk_group_app_install.SnykGroupAppInstall
