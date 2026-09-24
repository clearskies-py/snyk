"""Reference to SnykSelfAppSession model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_self_app_session import SnykSelfAppSession


class SnykSelfAppSessionReference(ModelClassReference["SnykSelfAppSession"]):
    """Reference to SnykSelfAppSession model."""

    def get_model_class(self) -> type["SnykSelfAppSession"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_self_app_session

        return snyk_self_app_session.SnykSelfAppSession
