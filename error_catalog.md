# Error Catalog

Known error patterns from the Cults3D GraphQL API, with likely causes and mitigation steps.

## HTTP / Transport
| Symptom | Likely cause | Fix | Source |
| --- | --- | --- | --- |
| `HTTP Basic: Access denied` | Bad Basic auth header or wrong API key | Re-encode `username:api_key`, rotate key if needed | Common |
| 401/403 responses | Missing or invalid auth | Verify headers and key status | Common |
| 429 Too Many Requests | Rate limit exceeded | Back off (1s -> 5s -> 10s -> 30s), reduce concurrency | Discord (rate limit guidance) |
| 5xx responses | Server transient error | Retry with backoff, log `cf-ray` | Common |

## GraphQL Validation
| Symptom | Likely cause | Fix | Source |
| --- | --- | --- | --- |
| `errors` array with validation messages | Missing required fields, invalid enums | Check mutation arguments against GraphiQL | Common |
| `Price must be greater than or equal to 0.5` when updating visibility | Known update bug (price validation triggered) | Include a valid price or retry after fix | Discord msg 1359185536522125454, msg 1359208692473401555 |

## Assets & Images
| Symptom | Likely cause | Fix | Source |
| --- | --- | --- | --- |
| ZIP shows "Unknown" in dashboard | URL hides filename or extension | Use direct links with filename in URL | Discord msg 1440065320273313954 |
| Image URLs are null | Querying the wrong field or missing images | Request `illustrationImageUrl` / `illustrations { imageUrl }` | Discord msg 1439120162417803264 |
| Images are low resolution | Default image size | Use `imageUrl(version: DEFAULT)` | Discord msg 1357745337367920790 |

## Commerce
| Symptom | Likely cause | Fix | Source |
| --- | --- | --- | --- |
| `downloadUrl` returns 403 in browser | Missing session cookie | Reuse logged-in browser cookie | Discord msg 1372299248560767106 |
