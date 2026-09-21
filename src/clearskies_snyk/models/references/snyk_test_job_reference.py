"""Reference to SnykTestJob model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_test_job import SnykTestJob


class SnykTestJobReference(ModelClassReference["SnykTestJob"]):
    """Reference to SnykTestJob model."""

    def get_model_class(self) -> type["SnykTestJob"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_test_job

        return snyk_test_job.SnykTestJob
