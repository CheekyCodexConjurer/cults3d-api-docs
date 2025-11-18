# LLM Ingest Guide

## Why this exists
These docs are designed to be fed into copilots such as Codex/GPT. Each file stays compact (<10 KB) and contains explicit prerequisites to avoid wasting context tokens.

## Preparing an Archive
From the root of this documentation folder:
```powershell
$Dest = ".\\cults-api-docs.zip"
if (Test-Path $Dest) { Remove-Item $Dest }
Compress-Archive -Path '.\\*.md','.\workflows','.\examples' -DestinationPath $Dest
```
- The resulting `cults-api-docs.zip` is the “baixável” bundle requested for LLM loading.
- Verify that no credentials or spreadsheet IDs ended up inside the archive before sharing.

## Feeding a Model
1. **Chunk order** – start with `README.md`, followed by `architecture.md`, then the workflow that matches your question (creation/update/asset) and, finally, `endpoints.md` or `examples/*.md`.
2. **Prompt framing** – when asking coding copilots for help, include the relevant path plus section heading (e.g., “See `workflows/creation_workflow.md`, section ‘GraphQL stage’”) so the model can jump directly to the right chunk.
3. **Context discipline** – avoid pasting entire files if only a subsection is needed. The docs are structured so most sections fit into <1,000 tokens.
4. **Versioning** – mention the doc revision date or git commit SHA so other contributors can trace back what the LLM learned.

## Safeguards
- Strip API keys, cookies, or Drive links before uploading the bundle to any third-party model hosting service.
- The docs already reiterate that we have no professional relationship with Cults. Preserve that disclaimer when redistributing snippets.
- When generating further summaries, prefer referential instructions (“consult `endpoints.md#commerce-orders`”) over copying raw mutations to minimize data drift.
