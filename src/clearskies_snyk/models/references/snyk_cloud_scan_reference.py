"""Reference to SnykCloudScan model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_cloud_scan import SnykCloudScan


class SnykCloudScanReference(ModelClassReference["SnykCloudScan"]):
    """Reference to SnykCloudScan model."""

    def get_model_class(self) -> type["SnykCloudScan"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_cloud_scan

        return snyk_cloud_scan.SnykCloudScan
