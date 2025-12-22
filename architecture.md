# Architecture

## Overview
- **Endpoint** - All traffic goes to `https://cults3d.com/graphql`.
- **Payload** - Send `POST` JSON bodies that include a `query` string and, optionally, a `variables` object. Standard GraphQL rules apply.
- **Transport** - HTTPS only. The API does not require browser automation or cookies for normal calls; cookies are only needed when you later download purchase URLs returned by `ordersBatch`.

Everything documented here is derived from the public gist and the `#api-help` Discord conversations.

## Terminology
- **Creation** - A design (the product page).
- **Blueprint** - A printable file attached to a creation.
- **Illustration** - An image attached to a creation.
Source: Discord msg 1359172678262456520.

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

## Pagination
- Batch endpoints use `limit` + `offset` for pagination.
- Community reports suggest responses may cap around 100 rows; use `offset` to fetch additional pages instead of relying on larger limits.
Source: Discord msg 1435688751140442234 (limit observation), msg 1437160159154540574 (offset: x).

## Money Fields and Units
- The official gist uses `cents` in several money examples, while recent Discord snippets use `value`. This doc standardizes on `value`, but you should confirm the exact field name in GraphiQL for your schema.
- Do not assume formatting. Verify whether the field represents minor units or formatted values before doing currency math.

## Known Ambiguities
- Money field name: `value` vs `cents` varies between gist and Discord examples.
- Search naming: some posts mention `searchCreationsBatch` while the gist and schema use `creationsSearchBatch`.
- Sale-time views: older posts used `creation/viewsCount`, current Discord example uses `creationViewsCount`.
- Always confirm these fields in GraphiQL before shipping changes.

## Schema Verification Checklist
Use GraphiQL to confirm field names before shipping a client.

**Introspection quick check**
```graphql
{
  sale: __type(name: "Sale") { fields { name } }
  creation: __type(name: "Creation") { fields { name } }
  money: __type(name: "MoneyType") { fields { name } }
  price: __type(name: "PriceType") { fields { name } }
}
```

**Smoke query**
```graphql
{
  myself {
    salesBatch(limit: 1) {
      results {
        id
        income(currency: EUR) { value } # or cents
        creationViewsCount
      }
    }
  }
}
```
See `schema/README.md` and `scripts/contract_checks.py` for automated schema checks.

## Validation Workflow
| Step | Operation | Success expectation | Troubleshooting |
| --- | --- | --- | --- |
| Auth probe | `POST { __typename }` | HTTP 200, empty `errors` | If 403/404, check firewall or base URL. |
| Schema query | `categories { id }` | HTTP 200 + data | 401 = wrong Basic header; 5xx = retry with exponential backoff. |
| Mutation dry-run | `createCreation` with empty asset lists | Returns `creation { id url }` or descriptive validation errors | Fix required fields (category/license/meta tags). |
| Logging | Capture `x-ratelimit-*`, `cf-ray`, and timestamps | Headers recorded for support audits | Missing headers? confirm proxies are not stripping them. |

Common failures:
- `HTTP Basic: Access denied` - username/key mismatch (recreate keys or re-encode the header).
- GraphQL `errors` array with validation messages - usually missing `subcategoryIds`, invalid license codes, or locale mismatches.
- Network timeouts - follow Discord advice: retry after 1s/5s/10s/30s and keep the number of concurrent calls low.
More patterns live in `error_catalog.md`.

## Rate Limits & Pacing
From multiple Discord threads (Mar/2025 and Oct/2025):
- Expect throttling at roughly **60 requests per 30 seconds** and **500 requests per day**. These thresholds can change without notice.
- Inspect `x-ratelimit-limit`, `x-ratelimit-remaining`, and `x-ratelimit-reset` headers when present.
- Implement exponential backoff when you hit HTTP 429/5xx: wait 1s -> 5s -> 10s -> 30s before retrying.
- "Give plenty of waiting time between requests" when downloading files, and avoid concurrent floods even if your tooling can handle it.
See `rate_limit_contract.md` for the pacing algorithm.

## Asset Hosting Guidelines
- `imageUrls` and `fileUrls` must point to HTTPS locations that Cults3D's backend can reach publicly (e.g., S3/Cloudflare R2/CDN buckets).
- Google Drive can be used as a host: share the file publicly and use the direct download link (`https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&filename=<filename.ext>` or `https://drive.google.com/uc?export=download&id=<FILE_ID>&filename=<filename.ext>`).
- The singular `createIllustration` / `createBlueprint` mutations accept an optional `position` and replace the deprecated plural variants. Source: Discord msg 1376995917026299984.
- Filenames are preserved as provided; ensure they include meaningful extensions (`.zip`, `.jpg`, `.png`) to avoid appearing as "unknown" in the dashboard (a complaint reported in Discord).
- For large images, request the `DEFAULT` size via `imageUrl(version: DEFAULT)` or `illustrationImageUrl(version: DEFAULT)`. Source: Discord msg 1357745337367920790.
- There is no hard limit on total files per design. `fileUrls` accepts up to 10 files per request, so attach additional files via `createBlueprint`. Cults prefers multiple STL files (clearer previews), but large ZIPs are still supported. For very large designs, a single ZIP can help if the auto-generated bundle fails.
- When attaching many assets, you can call `createIllustration`/`createBlueprint` multiple times. Space those calls by a few seconds if you are not batching to stay under the throttles.
- To update assets without downtime, fetch the current snapshot, create the new files first, then remove the obsolete ones.

## Metadata & Feature Notes
- **Categories/Licenses** - Both have dedicated queries (`categories`, `licenses`) in the gist so you can map friendly names to IDs/codes.
- **Meta tags** - October 2025 Discord announcements introduced full read/write support. Use `metaTags { code name }` to read and pass the `metaTags` argument when creating or updating a design to set them.
- **Filters** - `creationsBatch` and `creationsSearchBatch` now support price toggles (`onlyFree`, `onlyPriced`, `onlyDiscounted`), date windows (`submittedAfter`, `submittedBefore`), and `madeWithAi: false` to exclude AI-assisted uploads.
- **Visibility** - Use the `visibility` field on a creation to distinguish public/secret/deactivated items. Source: Discord msg 1380539355180957859.
- **Commerce data** - `salesBatch` exposes `discount { percentage startAt endAt }` plus `creationViewsCount` (sale-time snapshot, Dec/2025). `ordersBatch` exposes `lines { downloadUrl }`, but fetching those URLs still requires your browser session cookie. `SaleType.vat` was fixed in Feb/2025.
- **Views caching** - `viewsCount(cached: false)` returns uncached values (Discord Apr/2025). Omit the argument if cached values are acceptable.

## Sales Analytics Notes
- Use `creationViewsCount` for conversion at the time of sale; compare with current `viewsCount(cached: false)` only if you need trend deltas.
- For revenue charts, prefer `income(currency: EUR)` and convert client-side to avoid exchange-rate drift.
- Use `payedOutAt` for payout-based reporting and `createdAt` for sale-time reporting.
- Use `Sale.discount` for sale-time discounts; the creation's current discount can differ.

## Observability Tips
- Log the operation name, variables, and HTTP status for every call. This helps you prove respectful usage if the API team asks.
- When building dashboards, keep monetary values in EUR (per Discord guidance) and convert to other currencies client-side to avoid graph "dips" caused by exchange-rate fluctuations.
- Paginate using the `limit`/`offset` pairs provided on batch endpoints; a limit of 20-50 keeps responses light and avoids long-running requests.

## Independence Statement
This documentation is community maintained. It summarizes what the Cults team already shared publicly, but it is **not** official support. Always double-check the latest posts in `#api-help` before launching production automations.
