"""Reference to SnykOrg model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org import SnykOrg


class SnykOrgReference(ModelClassReference["SnykOrg"]):
    """Reference to SnykOrg model."""

    def get_model_class(self) -> type["SnykOrg"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org

        return snyk_org.SnykOrg
