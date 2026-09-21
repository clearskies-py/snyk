"""Reference to SnykCloudResource model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_cloud_resource import SnykCloudResource


class SnykCloudResourceReference(ModelClassReference["SnykCloudResource"]):
    """Reference to SnykCloudResource model."""

    def get_model_class(self) -> type["SnykCloudResource"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_cloud_resource

        return snyk_cloud_resource.SnykCloudResource
