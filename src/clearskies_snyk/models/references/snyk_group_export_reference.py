"""Reference to SnykGroupExport model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_group_export import SnykGroupExport


class SnykGroupExportReference(ModelClassReference["SnykGroupExport"]):
    """Reference to SnykGroupExport model."""

    def get_model_class(self) -> type["SnykGroupExport"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_group_export

        return snyk_group_export.SnykGroupExport
