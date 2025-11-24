# Architecture

## Overview
- **Endpoint** – All traffic goes to `https://cults3d.com/graphql`.
- **Payload** – Send `POST` JSON bodies that include a `query` string and, optionally, a `variables` object. Standard GraphQL rules apply.
- **Transport** – HTTPS only. The API does not require browser automation or cookies for normal calls; cookies are only needed when you later download purchase URLs returned by `ordersBatch`.

Everything documented here is derived from the public gist and the `#api-help` Discord conversations.

## Authentication
| Mode | Header | Notes |
| --- | --- | --- |
| Basic (recommended) | `Authorization: Basic <base64(username:api_key)>` | Discord support confirmed that the username is your Cults handle and the password is the API key generated at <https://cults3d.com/en/api/keys>. |
| Bearer | `Authorization: Bearer <api_key>` | Mentioned by the Cults team as a future-friendly alternative. |
| X-Api-Key | `X-Api-Key: <api_key>` | Provided for setups that prefer a custom header. |

**Basic auth example**  
```
username  = demo
api_key   = 1234
base64    = demo:1234 -> ZGVtbzoxMjM0
header    = Authorization: Basic ZGVtbzoxMjM0
```

Generate one API key per automation so you can rotate secrets independently. The Discord logs also mention that key names will help you trace which integration uses which secret.

## Requests & Responses
- GraphQL queries follow the schema in the gist. Mutations such as `createCreation`, `updateCreation`, `createBlueprint`, etc., all accept JSON-friendly scalar values.
- Include `locale`, `currency`, and similar enums whenever the gist requires them (`EN`, `EUR`, etc.).
- Every response may contain an `errors` array. Always check it before trusting the `data` portion.
- Some endpoints (orders downloads, certain chart data) reference authenticated browser URLs. Cults staff recommends reusing your logged-in browser cookie when fetching those files and spacing those downloads to avoid throttling.

### Validation Workflow
| Step | Operation | Success expectation | Troubleshooting |
| --- | --- | --- | --- |
| Auth probe | `POST { __typename }` | HTTP 200, empty `errors` | If 403/404, check firewall or base URL. |
| Schema query | `categories { id }` | HTTP 200 + data | 401 = wrong Basic header; 5xx = retry with exponential backoff. |
| Mutation dry-run | `createCreation` with empty asset lists | Returns `creation { id url }` or descriptive validation errors | Fix required fields (category/license/meta tags). |
| Logging | Capture `x-ratelimit-*`, `cf-ray`, and timestamps | Headers recorded for support audits | Missing headers? confirm proxies are not stripping them. |

Common failures:
- `HTTP Basic: Access denied` – username/key mismatch (recreate keys or re-encode the header).
- GraphQL `errors` array with validation messages – usually missing `subcategoryIds`, invalid license codes, or locale mismatches.
- Network timeouts – follow Discord advice: retry after 1s/5s/10s/30s and keep the number of concurrent calls low.

## Rate Limits & Pacing
From multiple Discord threads (Mar/2025 and Oct/2025):
- Expect throttling at roughly **60 requests per 30 seconds** and **500 requests per day**. These thresholds can change without notice.
- Inspect `x-ratelimit-limit`, `x-ratelimit-remaining`, and `x-ratelimit-reset` headers when present.
- Implement exponential backoff when you hit HTTP 429/5xx: wait 1s → 5s → 10s → 30s before retrying.
- “Give plenty of waiting time between requests” when downloading files, and avoid concurrent floods even if your tooling can handle it.

## Asset Hosting Guidelines
- `imageUrls` and `fileUrls` must point to HTTPS locations that Cults3D's backend can reach publicly (e.g., S3/Cloudflare R2/CDN buckets).
- Google Drive pode servir como host: compartilhe o arquivo como p�blico e use o link direto de download (`https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&filename=<nome.extensao>` ou `https://drive.google.com/uc?export=download&id=<FILE_ID>&filename=<nome.extensao>`).
- Filenames are preserved as provided; ensure they include meaningful extensions (`.zip`, `.jpg`, `.png`) to avoid appearing as "unknown" in the dashboard (a complaint reported in Discord).
- When attaching many assets, you can call `createIllustration`/`createBlueprint` multiple times. Space those calls by a few seconds if you are not batching to stay under the throttles.
- To update assets without downtime, fetch the current snapshot, create the new files first, then remove the obsolete ones.

## Metadata & Feature Notes
- **Categories/Licenses** – Both have dedicated queries (`categories`, `licenses`) in the gist so you can map friendly names to IDs/codes.
- **Meta tags** – October 2025 Discord announcements introduced full read/write support. Use `metaTags { code name }` to read and pass the `metaTags` argument when creating or updating a design to set them.
- **Filters** – `creationsBatch` and `creationsSearchBatch` now support price toggles (`onlyFree`, `onlyPriced`, `onlyDiscounted`), date windows (`submittedAfter`, `submittedBefore`), and `madeWithAi: false` to exclude AI-assisted uploads.
- **Commerce data** – `salesBatch` exposes a `discount { percentage startAt endAt }` object so you can see which promotion affected a sale. `ordersBatch` exposes `lines { downloadUrl }`, but fetching those URLs still requires your browser session cookie.

## Observability Tips
- Log the operation name, variables, and HTTP status for every call. This helps you prove respectful usage if the API team asks.
- When building dashboards, keep monetary values in EUR (per Discord guidance) and convert to other currencies client-side to avoid graph “dips” caused by exchange-rate fluctuations.
- Paginate using the `limit`/`offset` pairs provided on batch endpoints; a limit of 20–50 keeps responses light and avoids long-running requests.

## Independence Statement
This documentation is community maintained. It summarizes what the Cults team already shared publicly, but it is **not** official support. Always double-check the latest posts in `#api-help` before launching production automations.
