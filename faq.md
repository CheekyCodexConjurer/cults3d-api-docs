# FAQ (Cults3D GraphQL)

Quick answers copied from the `#api-help` Discord channel and the official gist. Each entry links to the relevant reference file inside this docset.

### How do I authenticate?
Use HTTP Basic auth: username = your Cults nickname, password = the API key generated at <https://cults3d.com/en/api/keys>. Encode `username:api_key` with Base64 and send `Authorization: Basic <token>`. Alternatives (`Bearer`, `X-Api-Key`) are listed in [architecture.md#authentication](architecture.md#authentication).

### What do "creation", "blueprint", and "illustration" mean?
A creation is the design itself, a blueprint is a printable file attached to it, and an illustration is an image attached to it. See [architecture.md#terminology](architecture.md#terminology) for a full definition.
Source: Discord msg 1359172678262456520.

### What are the rate limits?
Discord (Mar/2025 and Oct/2025) states roughly 60 requests per 30 seconds and 500 per day. They may change without notice, so always honor the `x-ratelimit-*` headers and back off (1s -> 5s -> 10s -> 30s) after any 429/5xx. Details in [architecture.md#rate-limits--pacing](architecture.md#rate-limits--pacing).

### Can I filter creations by price, date, or AI usage?
Yes. `creationsBatch` supports `onlyFree`, `onlyPriced`, `onlyDiscounted`, `submittedAfter`, `submittedBefore`, and `madeWithAi`. Examples live in [endpoints.md#discovery--filters](endpoints.md#discovery--filters).
Source: Discord msg 1339885721154097172, msg 1341723740572221492, msg 1425527790723137548.

### Where can I see the full list of `creationsBatch` filters?
Open <https://cults3d.com/graphiql>, click the book icon, and search for `ApplicationQuery.creationsBatch`. The schema lists every available filter.

### How do I list the models inside my printlists?
March 2025 Discord notes added nested `creationsBatch` access. See [endpoints.md#collections-likes-and-users](endpoints.md#collections-likes-and-users) for the exact query and how to `addCreationToPrintlist`.
Source: Discord msg 1346469900566401065, msg 1439933950192648252.

### How can I download my purchases?
`ordersBatch { results { lines { downloadUrl } } }` returns the URLs, but you still need to reuse your logged-in browser cookie when fetching the files. Sunny specifically asked for "plenty of waiting time between requests." See [endpoints.md#orders-sales-and-commerce](endpoints.md#orders-sales-and-commerce).
Source: Discord msg 1372299248560767106.

### Does `salesBatch` show which discount was applied?
Yes. A March 2025 Discord update added `discount { percentage startAt endAt }` to each `Sale`. Example in [endpoints.md#orders-sales-and-commerce](endpoints.md#orders-sales-and-commerce).
Source: Discord msg 1348948518307631155.

### Can I see how many views a design had when it sold?
Yes. A Dec/2025 Discord update added a sale-time view snapshot to `salesBatch`. Include `creationViewsCount` in the results. Example in [endpoints.md#orders-sales-and-commerce](endpoints.md#orders-sales-and-commerce).
Source: Discord screenshot (Dec 2025).

### Can I see how many likes a design had when it sold?
Yes. A Jan/2026 Discord update added a sale-time likes snapshot to `salesBatch`. Include `creationLikesCount` in the results; it is only populated for new sales. Example in [endpoints.md#orders-sales-and-commerce](endpoints.md#orders-sales-and-commerce).
Source: Discord screenshot (Jan 2026).

### How do I get uncached view counts?
Use `viewsCount(cached: false)` when querying `creationsBatch`. Omit the argument if cached values are acceptable. See [endpoints.md#collections-likes-and-users](endpoints.md#collections-likes-and-users).
Source: Discord msg 1356293103581008093.

### Can I manage meta tags through the API?
As of October 2025 you can read and modify meta tags. Include `metaTags` when calling `createCreation` or `updateCreation`, and query them via `metaTags { code name(locale: EN) }`. See [endpoints.md#reference-data](endpoints.md#reference-data).
Source: Discord msg 1434835512383766588.

### Why do prices dip when I request USD in analytics?
Sunny explained that totals are stored internally in EUR and converted on the fly. Currency swings will therefore appear as dips when charted in USD. Store the EUR values and convert client-side for stable graphs. See [architecture.md#metadata--feature-notes](architecture.md#metadata--feature-notes).

### My uploaded ZIPs show "Unknown" on the dashboard. Why?
That usually happens when the download URL hides the filename (e.g., Google Drive links with query parameters). Host files on URLs that expose the actual name and extension so Cults can preserve them. See [workflows/asset_sync.md](workflows/asset_sync.md).
Source: Discord msg 1440065320273313954.

### Why are image URLs null or low resolution?
If you are querying `imageUrl` fields and getting nulls, verify you are requesting the correct image field (`illustrationImageUrl` or `illustrations { imageUrl }`). For full resolution, pass `version: DEFAULT`. If the issue persists, share the exact query in `#api-help` so the team can reproduce it.
Source: Discord msg 1357745337367920790, msg 1439120162417803264.

### Do I need inline `imageUrls`/`fileUrls`?
Optional. You can provide them in `createCreation` or leave the arrays empty and immediately attach assets via `createIllustration`/`createBlueprint`. The Discord community often prefers the latter to keep payloads tiny. See [workflows/creation_workflow.md](workflows/creation_workflow.md).

### Is there a limit to how many files a design can have?
There is no hard limit on total files per design. `imageUrls` and `fileUrls` still cap at 10 URLs each, so add more files via `createBlueprint`/`createIllustration`. See [architecture.md#asset-hosting-guidelines](architecture.md#asset-hosting-guidelines).
Source: Discord msg 1392455056405692508.

### How do I paginate beyond 100 results?
Use the `limit`/`offset` pair on batch endpoints. If a response seems capped at 100 rows, advance the `offset` and request the next page.
Source: Discord msg 1435688751140442234, msg 1437160159154540574.

### How do I validate that my key still works?
Follow the checklist in [README.md#api-validation-checklist](README.md#api-validation-checklist): run `{ __typename }`, execute `categories { id }`, send a dry-run `createCreation`, and log the `x-ratelimit-*` headers. The snippet [examples/python_client.md#validation-helper](examples/python_client.md#validation-helper) automates these steps.

### Where should I host the ZIPs and renders used in `fileUrls`/`imageUrls`?
Google Drive can host ZIPs and renders as long as the direct link exposes the filename extension. Any HTTPS endpoint works; keep each field to 10 URLs. See [examples/upload-hosting.md](examples/upload-hosting.md) for direct download links.

More questions? Re-read the `#api-help` history or post in the channel-then update these docs so everyone shares the same answers.
