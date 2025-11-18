# Cults3D API Docs

This folder keeps a compact, public reference for the [Cults3D GraphQL API](https://cults3d.com/en/api/keys). Every note below comes straight from two sources:

1. The official GraphQL gist maintained by @sunny – <https://gist.github.com/sunny/07db54478ac030bd277c19cfe734648b>.
2. The `#api-help` Discord channel.

No private SDKs, scraping tricks, or repository-specific helpers are required to use this documentation. Everything assumes you are calling `https://cults3d.com/graphql` directly.

- Host assets using HTTPS links that end with the extension (see `examples/upload-hosting.md`). tmpfiles.org accepts ~200 MB por upload; transfer.sh aceita até 10 GB.
- Respeite as limitações de `fileUrls`/`imageUrls`: máximo 10 links por campo. Se precisar de mais arquivos, combine em ZIPs ou reutilize hosts alternativos.
- Exemplo completo: `examples/create-creation.graphql` reproduz o payload mostrado em `Create a design.graphql`, já com `tagNames` e `metaTags`.

Each markdown file stays under ~180 lines and is written to be LLM-friendly: clear headings, minimal cross-file dependencies, and short paragraphs that can be chunked independently.

## Directory Layout
| Path | Description |
| --- | --- |
| `architecture.md` | Transport basics, authentication modes, rate limits, and hosting guidance. |
| `endpoints.md` | Reference of GraphQL operations grouped by theme (creations, assets, discovery, commerce). |
| `workflows/creation_workflow.md` | Step-by-step outline to publish a new design via API. |
| `workflows/update_workflow.md` | How to refresh metadata or assets on an existing creation. |
| `workflows/asset_sync.md` | Best practices when diffing, batching, and retrying blueprint/illustration mutations. |
| `examples/graphql_queries.md` | Ready-to-run queries/mutations from the gist and Discord updates. |
| `examples/python_client.md` | Minimal Python client showing Basic auth, error handling, and pagination. |
| `examples/create-creation.graphql` | Payload pronto com `fileUrls`/`imageUrls` inline. |
| `examples/upload-hosting.md` | Guia rápido para gerar links diretos (tmpfiles, transfer.sh, etc.). |
| `llm_ingest.md` | Tips to package these docs for copilots/agents without wasting tokens. |
| `faq.md` | Fast answers curated from `#api-help`. |

## Getting Started
1. **Generate an API key** at <https://cults3d.com/en/api/keys>. Keep one key per integration.
2. **Create a HTTP client** (curl, Postman, requests, etc.) that POSTs JSON with `query` + `variables` to `https://cults3d.com/graphql`.
3. **Set the header** `Authorization: Basic <base64(username:api_key)>`. Discord also mentions `Bearer` and `X-Api-Key` headers; see `architecture.md`.
4. **Host assets** (ZIPs, renders) in publicly reachable HTTPS buckets so the API can pull them when you pass `imageUrls` or `fileUrls`.
5. **Respect rate limits** – the Cults team currently enforces ~60 req / 30 s and ~500 req / day and asks everyone to back off exponentially on HTTP 429/5xx.

## API Validation Checklist
1. **Ping the endpoint** – send `{ __typename }` or `architecture.md#requests--responses`’s sample query to confirm TLS + DNS.
2. **Test authentication** – issue `categories { id name(locale: EN) }` with your Basic header; expect HTTP 200 with data, or 401 if the username/key pair is wrong.
3. **Run a dry `createCreation`** – reuse `examples/create-creation.graphql` but keep `imageUrls`/`fileUrls` empty to ensure mutations work without attaching assets yet.
4. **Inspect headers** – log `x-ratelimit-*` plus `cf-ray`/`date` so you can correlate traffic when the API team asks for evidence.
5. **Record responses** – capture success + error bodies and store them with your ops notes; the FAQ section explains recurring failures.
6. **Automate checks** – `examples/python_client.md#validation` contains a small helper that runs the query + mutation pair and prints outcomes for monitoring.

## Coverage
These docs include everything that has been publicly discussed so far:
- Model creation/update mutations, asset attachment, and deletion.
- Discovery helpers: trending lists, search, price/date filters, `madeWithAi` flag, discounted-only views.
- Account data: printlists (with nested creations), likes, orders (with `downloadUrl`), sales (with the applied `discount`), and user snapshots.
- Meta tag read/write support (October 2025 Discord announcement).
- Operational tips from Discord: hosting requirements, Basic auth troubleshooting, and pacing guidance.

See a new snippet in `#api-help`? Add it to the relevant file with the date/source noted so everyone can trace provenance.

## Disclaimer
This is a community-maintained knowledge base. We are not affiliated with Cults3D, and there is no support agreement. Use the API respectfully, follow the platform’s terms, and re-check the Discord channel before automating large workflows.
