"""Request-level tests for relationships on nested Snyk endpoints."""

from __future__ import annotations

from typing import Any

import pytest
from clearskies.authentication import Public
from clearskies.di import Di

from clearskies_snyk.models import (
    SnykContainerImage,
    SnykGroup,
    SnykGroupSsoConnection,
    SnykOrgPolicy,
    SnykProject,
    SnykTarget,
)

GROUP_MEMBERSHIPS = {
    "data": [
        {
            "id": "mem-1",
            "type": "group_membership",
            "relationships": {
                "user": {
                    "data": {
                        "id": "u-1",
                        "type": "user",
                        "attributes": {"email": "a@example.com", "name": "A", "username": "a"},
                    }
                },
                "role": {"data": {"id": "r-1", "type": "group_role", "attributes": {"name": "member"}}},
                "group": {"data": {"id": "g-1", "type": "group", "attributes": {"name": "G"}}},
            },
        }
    ],
    "links": {},
}

GROUP_ORG_MEMBERSHIPS = {
    "data": [
        {
            "id": "om-1",
            "type": "org_membership",
            "relationships": {
                "org": {"data": {"id": "o-1", "type": "org", "attributes": {"name": "Org1"}}},
                "user": {"data": {"id": "u-1", "type": "user", "attributes": {"email": "a@example.com"}}},
                "role": {"data": {"id": "r-2", "type": "org_role", "attributes": {"name": "collaborator"}}},
            },
        }
    ],
    "links": {},
}

EMPTY: dict[str, Any] = {"data": [], "links": {}}


class FakeResponse:
    ok = True
    status_code = 200
    headers: dict[str, str] = {}
    content = b"{}"
    text = "{}"

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    def json(self) -> dict[str, Any]:
        return self._data


class FakeRequests:
    """Records request URLs and returns canned responses by URL fragment."""

    # Guard against endless pagination: fail loudly instead of hanging the test run.
    max_requests = 20

    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        self.responses = responses
        self.urls: list[str] = []

    def request(self, method: str, url: str, **kwargs: Any) -> FakeResponse:
        self.urls.append(url)
        if len(self.urls) > self.max_requests:
            raise AssertionError(f"more than {self.max_requests} requests, pagination is not stopping: {self.urls[:3]}")
        for fragment, data in self.responses.items():
            if fragment in url:
                return FakeResponse(data)
        return FakeResponse(EMPTY)


class FakeInputOutput:
    def get_context_for_callables(self) -> dict[str, Any]:
        return {}


def build_di(requests: FakeRequests) -> Di:
    di = Di()
    di.add_binding("requests", requests)
    di.add_binding("snyk_auth", Public())
    di.add_binding("input_output", FakeInputOutput())
    return di


def test_group_membership_orgs_uses_user_id_filter() -> None:
    requests = FakeRequests({"org_memberships": GROUP_ORG_MEMBERSHIPS, "/memberships": GROUP_MEMBERSHIPS})
    group = build_di(requests).build(SnykGroup, cache=False).model({"id": "g-1"})

    memberships = group.memberships.limit(100).paginate_all()
    assert len(memberships) == 1
    membership = memberships[0]
    assert membership.user_id == "u-1"
    assert membership.email == "a@example.com"
    assert membership.name == "A"
    assert membership.username == "a"

    org_membership = membership.orgs.first()
    assert org_membership.id == "om-1"
    assert org_membership.org_id == "o-1"
    assert org_membership.org["name"] == "Org1"
    assert org_membership.role["name"] == "collaborator"

    assert requests.urls[-1].startswith("https://api.snyk.io/rest/groups/g-1/org_memberships?user_id=u-1&")


@pytest.mark.parametrize(
    "model_class,data,rel_name,expected_path",
    [
        (SnykProject, {"id": "p-1", "org_id": "o-1"}, "history", "v1/org/o-1/project/p-1/history"),
        (SnykProject, {"id": "p-1", "org_id": "o-1"}, "ignores", "v1/org/o-1/project/p-1/ignores"),
        (
            SnykProject,
            {"id": "p-1", "org_id": "o-1"},
            "issues",
            "rest/orgs/o-1/issues?scan_item.id=p-1&scan_item.type=project&",
        ),
        (SnykTarget, {"id": "t-1", "org_id": "o-1"}, "projects", "rest/orgs/o-1/projects?target_id=t-1&"),
        (
            SnykContainerImage,
            {"id": "img-1", "org_id": "o-1"},
            "target_refs",
            "rest/orgs/o-1/container_images/img-1/relationships/image_target_refs?",
        ),
        (
            SnykGroupSsoConnection,
            {"id": "sso-1", "group_id": "g-1"},
            "users",
            "rest/groups/g-1/sso_connections/sso-1/users?",
        ),
        (SnykOrgPolicy, {"id": "pol-1", "org_id": "o-1"}, "events", "rest/orgs/o-1/policies/pol-1/events?"),
    ],
)
def test_nested_relationship_builds_full_url(
    model_class: type, data: dict[str, Any], rel_name: str, expected_path: str
) -> None:
    requests = FakeRequests({})
    parent = build_di(requests).build(model_class, cache=False).model(data)

    getattr(parent, rel_name).paginate_all()

    assert requests.urls, "no request was made"
    assert f"https://api.snyk.io/{expected_path}" in requests.urls[0]


PROJECTS_WITH_TARGET = {
    "data": [
        {
            "id": "p-1",
            "type": "project",
            "attributes": {"name": "repo"},
            "relationships": {
                "organization": {"data": {"id": "o-1", "type": "org"}},
                "target": {"data": {"id": "t-1", "type": "target", "attributes": {"display_name": "repo", "url": "u"}}},
            },
        }
    ],
    "links": {},
}


def test_relationship_data_is_not_used_as_partial_belongs_to_parent() -> None:
    """A relationship named like a BelongsToModel column must not become a pre-loaded parent."""
    requests = FakeRequests({"/projects": PROJECTS_WITH_TARGET})
    project = build_di(requests).build(SnykProject, cache=False).where("org_id=o-1").first()

    raw = project.get_raw_data()
    assert project.target_id == "t-1"
    assert "target" not in raw
    assert raw["relationships"]["target"]["data"]["attributes"]["display_name"] == "repo"


def test_group_membership_type_id_is_filled_from_relationship_type() -> None:
    requests = FakeRequests({"/memberships": GROUP_MEMBERSHIPS})
    group = build_di(requests).build(SnykGroup, cache=False).model({"id": "g-1"})

    membership = group.memberships.first()

    assert membership.group_role_id == "r-1"
    assert membership.role == {"id": "r-1", "type": "group_role", "name": "member"}
