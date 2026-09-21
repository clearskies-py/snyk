"""Reference to SnykOrgAppBot model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from clearskies.model import ModelClassReference

if TYPE_CHECKING:
    from clearskies_snyk.models.snyk_org_app_bot import SnykOrgAppBot


class SnykOrgAppBotReference(ModelClassReference["SnykOrgAppBot"]):
    """Reference to SnykOrgAppBot model."""

    def get_model_class(self) -> type["SnykOrgAppBot"]:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_app_bot

        return snyk_org_app_bot.SnykOrgAppBot
