"""Reference to SnykCloudEnvironment model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_cloud_environment import SnykCloudEnvironment


class SnykCloudEnvironmentReference(ModelClassReference["SnykCloudEnvironment"]):
    """Reference to SnykCloudEnvironment model."""

    def get_model_class(self) -> type["SnykCloudEnvironment"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_cloud_environment

        return snyk_cloud_environment.SnykCloudEnvironment
