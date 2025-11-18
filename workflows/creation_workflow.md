# Creation Workflow

This walkthrough explains how to publish a new design through the Cults3D GraphQL API using only the public primitives shared in the gist and on Discord.

## Inputs & Prerequisites
- A Cults3D API key (Basic auth username = Cults nick, password = API key).
- Hosted assets reachable via HTTPS (ZIP blueprints and PNG/JPG renders). Cloudflare R2, S3, or any CDN bucket works as long as it is public.
- Metadata fields from your source of truth: title, description, category, subcategories, tags, meta tag codes, license, price, locale, and currency.
- Optional: date windows or filters you want to reuse later for discovery queries.

## Stage 1 – Prepare Metadata
1. **Collect required fields** from the gist’s `createCreation` mutation: `name`, `description`, `downloadPrice`, `currency`, `locale`, `categoryId`, `subCategoryIds`, `licenseCode`, `tagNames`, `metaTags`, and `madeWithAi`.
2. **Resolve IDs** by calling `categories` and `licenses`. Store the mapping so you can pass the right base64 IDs and license codes.
3. **Normalize tags** (lowercase and strip whitespace) to match what the API expects. Meta tags must use the codes announced on Discord (e.g., `CultsHighlight`, `3DP_TOOLTIP`).
4. **Choose locale/currency** combinations supported by Cults (`EN`, `FR`, `EUR`, `USD`, etc.).

## Stage 2 – Prepare Assets
1. **Blueprint ZIPs** – keep consistent naming so the front-end can display them cleanly. Discord reports “Unknown” for files lacking an extension.
2. **Renders** – plan for multiple camera angles; host PNG/JPG versions at accessible URLs.
3. Decide whether you will provide `imageUrls`/`fileUrls` inline in `createCreation` or attach everything afterward via `createIllustration` and `createBlueprint`.

## Stage 3 – Call `createCreation`
1. Compose the mutation shown in `endpoints.md#creations--metadata`.
2. If you plan to attach assets separately, send empty arrays for `imageUrls` and `fileUrls`.
3. Send the request with your Basic auth header. Log both the request payload (minus secrets) and the HTTP status for traceability.
4. Inspect the response: if the `errors` array is non-empty, abort and fix the metadata. Successful responses return the `creation { id url }`.

## Stage 4 – Attach Assets (optional)
1. Use `createBlueprint` and `createIllustration` mutations for each hosted URL. Positions are integers where `1` is the first slot.
2. If you need to replace assets right away, call `creation(slug: "...")` to fetch the current list, compare it to your desired list, and then:
   - Create new files first.
   - Destroy old entries with `destroyBlueprint` / `destroyIllustration`.
3. Sleep a few seconds between calls (per Discord guidance) or batch operations in groups of ~10 to stay well under throttling thresholds.

## Stage 5 – Verification & Logging
1. Run a follow-up `creation(slug)` query to confirm the final asset order and capture the public URL.
2. Store the creation ID/slug in your system of record so future updates can target it quickly.
3. Monitor rate-limit headers and log them for future tuning.

## Recovery Tips
- If a mutation fails after some assets were uploaded, re-fetch the snapshot; re-running `createIllustration`/`createBlueprint` with the same URLs is idempotent because duplicates can be removed with the `destroy*` helpers.
- Errors like `HTTP Basic: Access denied` usually mean the username/API key pair is wrong. Base64 encode `username:api_key` exactly as shown in `architecture.md`.
- When in doubt, consult the `#api-help` backlog before automating new fields; Discord announcements often introduce new arguments (meta tags, AI filters, printlist helpers) that you may want to adopt immediately.
