"""Reference to SnykOrgApp model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_app import SnykOrgApp


class SnykOrgAppReference(ModelClassReference["SnykOrgApp"]):
    """Reference to SnykOrgApp model."""

    def get_model_class(self) -> type["SnykOrgApp"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_app

        return snyk_org_app.SnykOrgApp
