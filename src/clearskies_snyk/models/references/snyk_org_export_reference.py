"""Reference to SnykOrgExport model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_export import SnykOrgExport


class SnykOrgExportReference(ModelClassReference["SnykOrgExport"]):
    """Reference to SnykOrgExport model."""

    def get_model_class(self) -> type["SnykOrgExport"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_export

        return snyk_org_export.SnykOrgExport
