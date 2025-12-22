# Asset Synchronization

When the Cults API introduced the singular `createBlueprint` / `createIllustration` mutations, the Discord channel recommended a predictable process for keeping assets in sync. The checklist below keeps things API-friendly and reproducible.

## 1. Collect Desired Assets
- Build the full ordered list of URLs you expect to see on the creation.
- Store additional metadata locally (e.g., captions or camera angles) so you can track which file is which without relying on Cults IDs.

## 2. Fetch the Current Snapshot
Use `creation(slug)` to capture:
- Blueprint IDs, URLs, and positions.
- Illustration IDs, URLs, and positions.

Keep this snapshot handy; every sync operation references it to avoid redundant traffic.

## 3. Diff Desired vs Existing State
- If both lists match exactly (including order), skip the sync and log that nothing changed.
- Otherwise compute:
  - **Creates** - URLs that do not yet exist.
  - **Deletes** - IDs that are no longer needed.
  - **Moves** - when URLs are the same but positions change (treat as update by deleting and recreating, since no dedicated move mutation exists).

## 4. Apply Mutations
1. **Create first** - Add all new URLs via `createBlueprint` / `createIllustration`, supplying the correct `position`. Pause briefly (~5 s) between calls to respect the ~60 req / 30 s throttle noted on Discord.
2. **Delete later** - Once the new assets are live, issue `destroyBlueprint(id: ...)` or `destroyIllustration(id: ...)` for the obsolete IDs.
3. **Batching** - If you have more than a few assets, send them in small groups (<=10) to keep payloads readable and to simplify retries.
4. **Retry strategy** - On HTTP 429/5xx or GraphQL errors, obey the backoff suggested by the Cults team (1s -> 5s -> 10s -> 30s) before retrying the same mutation.

## 5. Verification
- Re-run `creation(slug)` after the mutations finish.
- Confirm that the positions and URLs line up exactly with your desired state.
- Persist the new IDs for future updates.

## Logging & Safety Tips
- Always log which URLs you attempted to add/remove along with the response status. This helps prove respectful usage if the Cults team audits access.
- When hosting assets on services like Google Drive, ensure the links return a direct download (Discord users observed "Unknown" filenames when query parameters hid the real name).
- Never run destructive operations (delete) in parallel with uploads; stagger them to keep the listing stable for buyers.

## Recovery
- If a run fails halfway, recompute the diff using the most recent snapshot. Because every operation is idempotent, replays simply skip existing files and remove leftovers.
- For persistent failures involving a single URL, double-check that the asset is publicly reachable and does not require cookies.
- Keep an eye on the Discord announcements; that is where singular mutations, meta tag support, and other behavior changes are first communicated.
