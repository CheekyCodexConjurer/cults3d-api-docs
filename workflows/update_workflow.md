# Update Workflow

Use this guide when you need to refresh an existing creation’s metadata, assets, or both via the public GraphQL API.

## Inputs
- The public URL (slug) or internal ID of the creation you want to modify.
- Any new metadata values (title, description, tags, meta tag codes, license, price).
- Updated ZIPs or renders hosted at HTTPS locations if assets must change.

## Stage 1 – Decide the Scope
1. Separate updates into three buckets:
   - **Metadata** – fields handled by `updateCreation`.
   - **Blueprints** – `.zip` assets created via `createBlueprint`.
   - **Illustrations** – renders handled by `createIllustration`.
2. If nothing changed, stop; the Cults team asks everyone to avoid redundant API calls.

## Stage 2 – Fetch the Current Snapshot
1. Use the `creation(slug: "...")` query to retrieve:
   - `id` – required for `updateCreation` and asset mutations.
   - `blueprints { id fileUrl position }` and `illustrations { id imageUrl position }` – needed to diff assets.
2. Persist the snapshot so you can detect partial updates if the workflow is retried.

## Stage 3 – Update Metadata (optional)
1. Build the `updateCreation` mutation with only the fields you wish to change (Cults accepts sparse payloads).
2. Include `metaTags` if you plan to add/remove highlights—Discord confirmed this argument now works for both create and update flows.
3. Send the mutation, inspect the `errors` array, and log the returned URL (the slug may change if the title changes).

## Stage 4 – Refresh Assets (optional)
1. Compare the desired list of URLs to the snapshot:
   - **Same order + same URLs** → skip.
   - **New files** → call `createBlueprint`/`createIllustration` with the `creationId`.
   - **Removed files** → call `destroyBlueprint`/`destroyIllustration` with the obsolete IDs.
2. Recommended order per Discord guidance:
   - Create new assets first so the listing never falls to zero renders/files.
   - Delete extras afterward.
3. Add a short pause (≈5 seconds) between calls or process them in small batches to respect the ~60 requests / 30 seconds limit.

## Stage 5 – Validation
1. Run another `creation(slug)` query to confirm the final state.
2. Update your internal tracker with the latest slug, ID, and asset URLs so future jobs start with fresh data.
3. Monitor the `x-ratelimit-*` headers to ensure you stay well below the daily quotas.

## Recovery Notes
- All mutations are repeatable: if a request times out, check the snapshot before retrying so you do not accidentally duplicate assets.
- If you need to download proofs (orders, sales, etc.) while debugging, insert generous waits between requests; the Discord channel repeatedly warns against hammering the API.
- When adding entirely new fields announced on Discord (e.g., meta tags, AI filters), update both this workflow and your automation scripts simultaneously so they stay in sync.
