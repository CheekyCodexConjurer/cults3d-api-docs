# Stability Matrix

Use this matrix to decide which fields need verification before you ship a client. "Stable" = in the gist and unchanged for a long time. "Recent" = announced in Discord and may drift. "Volatile" = ambiguous in sources or known to vary (like money field names).

## Legend
- **Stable** - Documented in the official gist.
- **Recent** - Announced in Discord (2025-2026).
- **Volatile** - Conflicting sources or known schema ambiguity.

## Field Stability
| Field / Feature | Object | Stability | Source | Verification |
| --- | --- | --- | --- | --- |
| `createCreation` | Mutation | Stable | Gist | Run a dry mutation in GraphiQL |
| `updateCreation` | Mutation | Stable | Gist | Run a price-only update |
| `creationsBatch` | Query | Stable | Gist | `__schema` query args |
| `creationsSearchBatch` | Query | Stable | Gist | `__schema` query args |
| `ordersBatch` | Query | Stable | Gist | Query a small batch |
| `salesBatch` | Query | Stable | Gist | Query a small batch |
| `createDiscount` | Mutation | Stable | Gist | Dry mutation in GraphiQL |
| `value` vs `cents` | Money fields | Volatile | Gist + Discord | Check `MoneyType` in GraphiQL |
| `submittedAfter` / `submittedBefore` | `creationsBatch` args | Recent | Discord msg 1339885721154097172 | `__schema` query args |
| `onlyPriced` | `creationsBatch` args | Recent | Discord msg 1341723740572221492 | `__schema` query args |
| `madeWithAi` | Creation field + filter | Recent | Discord msg 1425527790723137548 | `__schema` query args + Creation fields |
| `metaTags` | Creation field + mutation arg | Recent | Discord msg 1434835512383766588 | `__type(name: "Creation")` |
| `viewsCount(cached: false)` | Creation field arg | Recent | Discord msg 1356293103581008093 | `__type(name: "Creation")` |
| `creationViewsCount` | Sale field | Recent | Discord screenshot (Dec 2025) | `__type(name: "Sale")` |
| `creationLikesCount` | Sale field | Recent | Discord screenshot (Jan 2026) | `__type(name: "Sale")` |
| `discount` | Sale field | Recent | Discord msg 1348948518307631155 | `__type(name: "Sale")` |
| `publicId` / `createdAt` / `price` | Order fields | Recent | Discord msg 1389915227767963692 | `__type(name: "Order")` |
| `lines.downloadUrl` | OrderLine field | Recent | Discord msg 1372299248560767106 | Resolve `Order.lines` type |
| `imageUrl(version: DEFAULT)` | Illustration image | Recent | Discord msg 1357745337367920790 | `__type(name: "Illustration")` |
| `createBlueprint` / `createIllustration` (singular + `position`) | Mutations | Recent | Discord msg 1376995917026299984 | `__schema` mutation args |
| `addCreationToPrintlist` | Mutation | Recent | Discord msg 1439933950192648252 | `__schema` mutation args |
| `visibility` | Creation field | Recent | Discord msg 1380539355180957859 | `__type(name: "Creation")` |
| `SaleType.vat` | Sale type | Recent | Discord msg 1339886382696628314 | `__type(name: "SaleType")` |

## Verification Routine
1. Run the introspection query in `schema/introspection.graphql` or execute `python scripts/contract_checks.py`.
2. If any **Volatile** field is missing, update `field_matrix.md` and alert in `changelog.md`.
3. If any **Recent** field is missing, confirm in `#api-help` and document the drift.
