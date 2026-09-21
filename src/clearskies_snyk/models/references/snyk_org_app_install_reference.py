"""Reference to SnykOrgAppInstall model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_app_install import SnykOrgAppInstall


class SnykOrgAppInstallReference(ModelClassReference["SnykOrgAppInstall"]):
    """Reference to SnykOrgAppInstall model."""

    def get_model_class(self) -> type["SnykOrgAppInstall"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_app_install

        return snyk_org_app_install.SnykOrgAppInstall
