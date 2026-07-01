"""
Context-based integration tests for SnykBackend.

These tests validate the backend using proper clearskies Context and DI,
following the pattern from clearskies' test_api_backend.py.
"""

import unittest
from unittest.mock import MagicMock

import clearskies

from clearskies_snyk.models import SnykOrg, SnykTarget


class SnykBackendContextTest(unittest.TestCase):
    """Integration tests using clearskies Context."""

    def test_list_targets_with_routing_params(self):
        """Test listing targets with org_id routing parameter using Callable."""

        def list_targets(snyk_targets: SnykTarget):
            # Query with routing parameter
            targets = snyk_targets.where("org_id=org-123").limit(2)
            # Iterate to get results (don't use list() as it calls count())
            return [t for t in targets]

        # Mock response from Snyk API
        requests = MagicMock()
        response = MagicMock()
        response.ok = True
        response.status_code = 200
        response.headers = {}
        response.json = MagicMock(
            return_value={
                "data": [
                    {
                        "id": "target-1",
                        "type": "target",
                        "attributes": {
                            "display_name": "repo-1",
                            "origin": "github",
                        },
                    },
                    {
                        "id": "target-2",
                        "type": "target",
                        "attributes": {
                            "display_name": "repo-2",
                            "origin": "gitlab",
                        },
                    },
                ],
                "links": {},
            }
        )
        requests.request = MagicMock(return_value=response)

        # Create context with proper DI
        context = clearskies.contexts.Context(
            clearskies.endpoints.Callable(
                list_targets,
                model_class=SnykTarget,
                readable_column_names=["id", "display_name", "origin"],
            ),
            classes=[SnykTarget],
            bindings={
                "snyk_auth": clearskies.authentication.Public(),
                "requests": requests,
            },
        )

        status_code, result, headers = context()

        # Verify response
        assert status_code == 200
        assert len(result["data"]) == 2
        assert result["data"][0]["id"] == "target-1"
        assert result["data"][0]["display_name"] == "repo-1"
        assert result["data"][1]["id"] == "target-2"

        # Verify request was made correctly
        requests.request.assert_called_once()
        call_args = requests.request.call_args
        # The first positional arg is the method (GET), second is URL
        # Or check kwargs for url
        if len(call_args[0]) >= 2:
            url = call_args[0][1]
        elif "url" in call_args.kwargs:
            url = call_args.kwargs["url"]
        else:
            url = str(call_args[0][0])

        # URL must include org_id routing parameter
        assert "orgs/org-123/targets" in url
        assert "version=" in url

    def test_get_single_target(self):
        """Test fetching a single target by ID with routing params."""

        def get_target(snyk_targets: SnykTarget):
            return snyk_targets.where("org_id=org-456").find("id=target-abc")

        requests = MagicMock()
        response = MagicMock()
        response.ok = True
        response.status_code = 200
        response.headers = {}
        response.json = MagicMock(
            return_value={
                "data": {
                    "id": "target-abc",
                    "type": "target",
                    "attributes": {
                        "display_name": "my-app",
                        "origin": "github",
                    },
                }
            }
        )
        requests.request = MagicMock(return_value=response)

        context = clearskies.contexts.Context(
            clearskies.endpoints.Callable(
                get_target,
                model_class=SnykTarget,
                readable_column_names=["id", "display_name", "origin", "org_id"],
            ),
            classes=[SnykTarget],
            bindings={
                "snyk_auth": clearskies.authentication.Public(),
                "requests": requests,
            },
        )

        status_code, result, headers = context()

        assert status_code == 200
        assert result["data"]["id"] == "target-abc"
        assert result["data"]["display_name"] == "my-app"
        # Routing parameter should be included in result
        assert result["data"]["org_id"] == "org-456"

    def test_delete_with_routing_params(self):
        """
        Test delete operation with routing parameters.

        This is the critical test for the bug fix - ensuring that delete
        operations work correctly when the model instance was fetched
        via a query with routing parameters.
        """

        def delete_target(snyk_targets: SnykTarget):
            # Query with routing parameter
            target = snyk_targets.where("org_id=org-789").find("id=target-xyz")
            # Delete should include org_id in URL
            target.delete()
            return {"deleted": True}

        requests = MagicMock()

        # Mock GET response for finding the target
        get_response = MagicMock()
        get_response.ok = True
        get_response.status_code = 200
        get_response.headers = {}
        get_response.json = MagicMock(
            return_value={
                "data": {
                    "id": "target-xyz",
                    "type": "target",
                    "attributes": {
                        "display_name": "old-repo",
                    },
                }
            }
        )

        # Mock DELETE response
        delete_response = MagicMock()
        delete_response.ok = True
        delete_response.status_code = 204
        delete_response.content = b""

        # Return GET first, then DELETE
        requests.request = MagicMock(side_effect=[get_response, delete_response])

        context = clearskies.contexts.Context(
            clearskies.endpoints.Callable(delete_target),
            classes=[SnykTarget],
            bindings={
                "snyk_auth": clearskies.authentication.Public(),
                "requests": requests,
            },
        )

        status_code, result, headers = context()

        assert status_code == 200
        assert result["data"]["deleted"] is True

        # Verify two requests were made
        assert requests.request.call_count == 2

        # Verify DELETE request included org_id in URL
        delete_call = requests.request.call_args_list[1]
        # Args are (method, url, ...) or check kwargs
        if len(delete_call[0]) >= 2:
            delete_method = delete_call[0][0]
            delete_url = delete_call[0][1]
        else:
            delete_method = delete_call.kwargs.get("method")
            delete_url = delete_call.kwargs.get("url")

        assert delete_method == "DELETE"
        # CRITICAL: delete URL must include org-789
        assert "orgs/org-789/targets/target-xyz" in delete_url
        assert "version=" in delete_url

    def test_list_orgs(self):
        """Test listing organizations (no routing params needed)."""

        def list_orgs(snyk_orgs: SnykOrg):
            orgs = snyk_orgs.limit(10)
            return [o for o in orgs]  # Iterate instead of list()

        requests = MagicMock()
        response = MagicMock()
        response.ok = True
        response.status_code = 200
        response.headers = {}
        response.json = MagicMock(
            return_value={
                "data": [
                    {
                        "id": "org-1",
                        "type": "org",
                        "attributes": {
                            "name": "My Company",
                            "slug": "my-company",
                        },
                    }
                ],
                "links": {},
            }
        )
        requests.request = MagicMock(return_value=response)

        context = clearskies.contexts.Context(
            clearskies.endpoints.Callable(
                list_orgs,
                model_class=SnykOrg,
                readable_column_names=["id", "name", "slug"],
            ),
            classes=[SnykOrg],
            bindings={
                "snyk_auth": clearskies.authentication.Public(),
                "requests": requests,
            },
        )

        status_code, result, headers = context()

        assert status_code == 200
        assert len(result["data"]) == 1
        assert result["data"][0]["name"] == "My Company"

        # Verify URL
        requests.request.assert_called_once()
        call_args = requests.request.call_args
        if len(call_args[0]) >= 2:
            url = call_args[0][1]
        elif "url" in call_args.kwargs:
            url = call_args.kwargs["url"]
        else:
            url = str(call_args[0][0])

        assert "orgs" in url
        assert "version=" in url


if __name__ == "__main__":
    unittest.main()
