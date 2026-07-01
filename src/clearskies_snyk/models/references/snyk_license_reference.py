"""Reference to SnykLicense model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.v1.snyk_license import SnykLicense


class SnykLicenseReference(ModelClassReference["SnykLicense"]):
    """Reference to SnykLicense model."""

    def get_model_class(self) -> type["SnykLicense"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models.v1 import snyk_license

        return snyk_license.SnykLicense
