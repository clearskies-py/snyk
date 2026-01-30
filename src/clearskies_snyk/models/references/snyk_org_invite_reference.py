"""Reference to SnykOrgInvite model."""


class SnykOrgInviteReference:
    """Reference to SnykOrgInvite model."""

    def get_model_class(self) -> type:
        """Return the model class this reference points to."""
        from clearskies_snyk.models import snyk_org_invite

        return snyk_org_invite.SnykOrgInvite
