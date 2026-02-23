# Spec-Driven Backend Testing

This directory contains spec-driven tests that validate the SnykBackend implementation against the OpenAPI specification.

## Overview

The spec-driven testing architecture ensures that:

1. **HTTP requests match the spec** - Headers, methods, URLs, and bodies are validated against OpenAPI spec
2. **Spec changes are detected** - When the Snyk API spec is updated, tests immediately show what needs updating
3. **Complete coverage** - All CRUD operations are tested against all endpoints in the spec
4. **Automatic test generation** - Tests are parametrized using the spec, no manual test creation needed

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 OpenAPI Spec Files                      │
│         (v2-rest-api-spec.json, etc.)                  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│              SpecParser                                 │
│  - Extract endpoints, methods, schemas                  │
│  - Parse request/response definitions                   │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ├──────────────────┐
                   ▼                  ▼
┌──────────────────────────┐  ┌────────────────────────┐
│  SpecTestFixtures        │  │  RequestValidator      │
│  - Generate test data    │  │  - Validate headers    │
│  - Create test cases     │  │  - Validate URLs       │
│  - Mock models           │  │  - Validate bodies     │
└──────────────────────────┘  └────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│           Parametrized Tests                            │
│  - test_snyk_backend_crud.py                           │
│  - test_spec_compatibility.py                          │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. SpecParser ([`tests/validation/spec_parser.py`](tests/validation/spec_parser.py))

Parses the OpenAPI spec and extracts endpoint information:

```python
from tests.validation.spec_parser import SpecParser

parser = SpecParser(Path("api_spec/v2-rest-api-spec.json"))

# Get all endpoints
endpoints = parser.get_all_endpoints()

# Get endpoints by operation
post_endpoints = parser.get_endpoints_for_operation("POST")

# Get required headers
headers = parser.get_required_headers("/orgs", "GET")
```

### 2. RequestValidator ([`tests/validation/request_validator.py`](tests/validation/request_validator.py))

Validates HTTP requests against spec requirements:

```python
from tests.validation.request_validator import RequestValidator

validator = RequestValidator(spec_parser)

# Validate headers
result = validator.validate_headers("/orgs", "GET", headers)
assert result.valid

# Validate complete request
result = validator.validate_request(url, "POST", headers, body)
```

### 3. SpecTestFixtures ([`tests/fixtures/spec_fixtures.py`](tests/fixtures/spec_fixtures.py))

Generates test data from the spec:

```python
from tests.fixtures.spec_fixtures import SpecTestFixtures

fixtures = SpecTestFixtures()

# Generate request data
data = fixtures.generate_request_data(endpoint_info)

# Create mock model
model = fixtures.create_mock_model(endpoint_info)

# Get all create endpoints
create_endpoints = fixtures.get_all_create_endpoints()
```

## Test Files

### [`tests/backends/test_snyk_backend_crud.py`](tests/backends/test_snyk_backend_crud.py)

Parametrized tests for CRUD operations:

- **TestCreateOperations** - Validates POST requests
  - Headers match spec requirements
  - Body uses JSON:API format
  - URL includes version parameter

- **TestUpdateOperations** - Validates PATCH requests
  - Headers match spec requirements
  - Body uses JSON:API format with id
  - URL includes version parameter

- **TestDeleteOperations** - Validates DELETE requests
  - Headers match spec requirements
  - URL includes version parameter

- **TestReadOperations** - Validates GET requests
  - Query parameters include version

- **TestHTTPMethodValidation** - Validates correct HTTP methods used
  - create() uses POST
  - update() uses PATCH
  - delete() uses DELETE

### [`tests/validation/test_spec_compatibility.py`](tests/validation/test_spec_compatibility.py)

Spec change detection and compatibility tests:

- **TestSpecVersionTracking** - Detects when spec changes
  - Computes SHA256 hash of spec file
  - Compares to previous version
  - Fails with detailed message if changed

- **TestEndpointCoverage** - Reports on endpoint coverage
  - Summarizes endpoints by tag
  - Lists HTTP methods
  - Shows spec statistics

- **TestSpecStructure** - Validates spec structure
  - All endpoints have operation IDs
  - POST endpoints have request bodies
  - All endpoints have responses

- **TestBackendCompatibility** - Validates backend config
  - Correct API version format
  - JSON:API headers
  - Correct base URL

## Running Tests

### Run all spec-driven tests

```bash
pytest tests/validation/ tests/backends/test_snyk_backend_crud.py -v
```

### Run only CRUD tests

```bash
pytest tests/backends/test_snyk_backend_crud.py -v
```

### Run only compatibility tests

```bash
pytest tests/validation/test_spec_compatibility.py -v
```

### Run tests for specific operation

```bash
pytest tests/backends/test_snyk_backend_crud.py::TestCreateOperations -v
```

### See spec summary

```bash
pytest tests/validation/test_spec_compatibility.py::TestSpecChangeSummary -v -s
```

## Maintenance Workflow

### When Snyk API Updates

1. **Download new spec files** to [`api_spec/`](../../api_spec/)
2. **Run compatibility tests** to detect changes:
   ```bash
   pytest tests/validation/test_spec_compatibility.py -v
   ```
3. **Review failures** - The spec version test will fail with details
4. **Update implementation**:
   - Update models in [`src/clearskies_snyk/models/`](../../src/clearskies_snyk/models/)
   - Update backends in [`src/clearskies_snyk/backends/`](../../src/clearskies_snyk/backends/)
5. **Run all tests** to verify updates:
   ```bash
   pytest -v
   ```

### Adding New Endpoint

1. **Add model** with `destination_name()` method
2. **Run tests** - They auto-generate from spec
3. **Verify tests pass**
4. No manual test creation needed!

### Debugging Test Failures

1. **Check error message** - Shows exactly what's wrong
2. **Review spec** at the failing endpoint path
3. **Compare to backend implementation**
4. **Update backend hooks** if needed
5. **Re-run tests** to verify fix

## Spec Version Tracking

The file [`tests/fixtures/.spec_version`](tests/fixtures/.spec_version) contains the SHA256 hash of the current spec file. When the spec changes:

1. The hash changes
2. [`test_spec_version_recorded()`](tests/validation/test_spec_compatibility.py:40) fails
3. A detailed message shows what to review
4. After review, run tests again to accept the change

## Benefits

1. **Automatic validation** - Spec changes immediately show what needs updating
2. **Complete coverage** - Every endpoint tested automatically
3. **Clear errors** - Know exactly what's wrong when tests fail
4. **Low maintenance** - Tests generate from spec, not manual creation
5. **Confidence** - Implementation matches API requirements
6. **Documentation** - Tests serve as executable API documentation

## Example Test Output

```
tests/backends/test_snyk_backend_crud.py::TestCreateOperations::test_create_request_headers[POST_orgs]
PASSED - Headers match spec requirements

tests/backends/test_snyk_backend_crud.py::TestUpdateOperations::test_update_request_headers[PATCH_orgs/{org_id}]
FAILED - Missing header: Content-Type: application/vnd.api+json

tests/backends/test_snyk_backend_crud.py::TestCreateOperations::test_create_url_includes_version[POST_groups]
PASSED - Version parameter present in URL
```

## Future Enhancements

1. **Schema validation** - Validate request/response bodies against JSON schemas
2. **Response validation** - Validate backend response parsing
3. **Integration tests** - Test against real Snyk API (with test account)
4. **CI/CD integration** - Automated spec update detection
5. **Coverage reports** - Show which endpoints are tested vs implemented

## References

- [OpenAPI Specification](https://swagger.io/specification/)
- [JSON:API Format](https://jsonapi.org/)
- [Snyk API Documentation](https://docs.snyk.io/snyk-api-info)
- [Implementation Plan](../../plans/spec-driven-backend-testing-plan.md)
- [Architecture Diagrams](../../plans/spec-driven-testing-architecture-diagrams.md)
