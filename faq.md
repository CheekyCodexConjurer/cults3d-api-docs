# FAQ (Cults3D GraphQL)

Quick answers copied from the `#api-help` Discord channel and the official gist. Each entry links to the relevant reference file inside this docset.

### How do I authenticate?
Use HTTP Basic auth: username = your Cults nickname, password = the API key generated at <https://cults3d.com/en/api/keys>. Encode `username:api_key` with Base64 and send `Authorization: Basic <token>`. Alternatives (`Bearer`, `X-Api-Key`) are listed in [architecture.md#authentication](architecture.md#authentication).

### What are the rate limits?
Discord (Mar/2025 and Oct/2025) states roughly 60 requests per 30 seconds and 500 per day. They may change without notice, so always honor the `x-ratelimit-*` headers and back off (1s → 5s → 10s → 30s) after any 429/5xx. Details in [architecture.md#rate-limits--pacing](architecture.md#rate-limits--pacing).

### Can I filter creations by price, date, or AI usage?
Yes. `creationsBatch` supports `onlyFree`, `onlyPriced`, `onlyDiscounted`, `submittedAfter`, `submittedBefore`, and `madeWithAi`. Examples live in [endpoints.md#discovery--filters](endpoints.md#discovery--filters).

### How do I list the models inside my printlists?
March 2025 Discord notes added nested `creationsBatch` access. See [endpoints.md#collections-likes-and-users](endpoints.md#collections-likes-and-users) for the exact query and how to `addCreationToPrintlist`.

### How can I download my purchases?
`ordersBatch { results { lines { downloadUrl } } }` returns the URLs, but you still need to reuse your logged-in browser cookie when fetching the files. Sunny specifically asked for “plenty of waiting time between requests.” See [endpoints.md#orders-sales-and-commerce](endpoints.md#orders-sales-and-commerce).

### Does `salesBatch` show which discount was applied?
Yes. A March 2025 Discord update added `discount { percentage startAt endAt }` to each `Sale`. Example in [endpoints.md#orders-sales-and-commerce](endpoints.md#orders-sales-and-commerce).

### Can I manage meta tags through the API?
As of October 2025 you can read and modify meta tags. Include `metaTags` when calling `createCreation` or `updateCreation`, and query them via `metaTags { code name(locale: EN) }`. See [endpoints.md#reference-data](endpoints.md#reference-data).

### Why do prices dip when I request USD in analytics?
Sunny explained that totals are stored internally in EUR and converted on the fly. Currency swings will therefore appear as dips when charted in USD. Store the EUR values and convert client-side for stable graphs. See [architecture.md#metadata--feature-notes](architecture.md#metadata--feature-notes).

### My uploaded ZIPs show “Unknown” on the dashboard. Why?
That usually happens when the download URL hides the filename (e.g., Google Drive links with query parameters). Host files on URLs that expose the actual name and extension so Cults can preserve them. See [workflows/asset_sync.md](workflows/asset_sync.md).

### Do I need inline `imageUrls`/`fileUrls`?
Optional. You can provide them in `createCreation` or leave the arrays empty and immediately attach assets via `createIllustration`/`createBlueprint`. The Discord community often prefers the latter to keep payloads tiny. See [workflows/creation_workflow.md](workflows/creation_workflow.md).

### Como valido se minha chave ainda funciona?
Siga a checklist em [README.md#api-validation-checklist](README.md#api-validation-checklist): teste `{ __typename }`, execute `categories { id }`, rode uma `createCreation` de rascunho e registre os cabeçalhos `x-ratelimit-*`. O snippet [examples/python_client.md#validation-helper](examples/python_client.md#validation-helper) automatiza esses passos.

### Where should I host the ZIPs and renders used in `fileUrls`/`imageUrls`?
Any HTTPS endpoint that exposes the filename (ending with `.zip`, `.png`, etc.) works. Discord frequently mentions tmpfiles.org (~200 MB per upload) and transfer.sh (até 10 GB). Sempre use links diretos e limite cada campo a 10 URLs. O passo a passo está em [examples/upload-hosting.md](examples/upload-hosting.md).

More questions? Re-read the `#api-help` history or post in the channel—then update these docs so everyone shares the same answers.
