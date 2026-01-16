# Field Matrix

Quick reference for common fields used by coding agents. Verify field names in GraphiQL if the schema changes.

## Schema Verification (GraphiQL)
```graphql
{
  sale: __type(name: "Sale") { fields { name } }
  creation: __type(name: "Creation") { fields { name } }
  money: __type(name: "MoneyType") { fields { name } }
  price: __type(name: "PriceType") { fields { name } }
}
```

## Sales Analytics Notes
- Use `creationViewsCount` for sale-time conversion calculations.
- Use `creationLikesCount` for sale-time popularity; older sales may not include it.
- Use `viewsCount(cached: false)` if you need fresh view counts for current trends.
- Prefer `income(currency: EUR)` for consistent reporting, and convert client-side if needed.
- Use `createdAt` for sale-time reporting and `payedOutAt` for payout reporting.

## Sale (salesBatch results)
| Field | Notes | Source |
| --- | --- | --- |
| `id` | Sale id | Gist |
| `createdAt` | Sale timestamp | Gist |
| `payedOutAt` | Payout timestamp | Gist |
| `income(currency: EUR) { value }` | Money field, currency argument | Gist (uses `cents`) + Discord msg 1356293103581008093 |
| `discount { percentage startAt endAt }` | Sale-time discount | Discord msg 1348948518307631155 |
| `creation { name(locale: EN) }` | Creation summary | Gist |
| `creationViewsCount` | Sale-time views snapshot | Discord screenshot (Dec 2025) |
| `creationLikesCount` | Sale-time likes snapshot (only for sales after Jan 2026) | Discord screenshot (Jan 2026) |
| `user { nick }` | Buyer summary | Gist |
| `vat` | On `SaleType`, fixed Feb/2025 | Discord msg 1339886382696628314 |

## Order (ordersBatch results)
| Field | Notes | Source |
| --- | --- | --- |
| `publicId` | Public order id | Discord msg 1389915227767963692 |
| `createdAt` | Order timestamp | Discord msg 1389915227767963692 |
| `price { currency value }` | Money field, currency argument | Gist (uses `cents`) + Discord msg 1389915227767963692 |
| `lines { downloadUrl }` | Requires browser session cookie to fetch | Discord msg 1372299248560767106 |

## Creation (creation / creationsBatch results)
| Field | Notes | Source |
| --- | --- | --- |
| `identifier` | Internal identifier | Discord msg 1356293103581008093 |
| `name(locale: EN)` | Localized name | Gist |
| `url(locale: EN)` | Localized URL | Gist |
| `shortUrl` | Short link | Gist |
| `illustrationImageUrl` | Cover image | Gist |
| `illustrationImageUrl(version: DEFAULT)` | Large image variant | Discord msg 1357745337367920790 |
| `price(currency: EUR) { value }` | Money field, currency argument | Gist (uses `cents`) |
| `viewsCount(cached: false)` | Uncached view count | Discord msg 1356293103581008093 |
| `downloadsCount` | Downloads | Gist |
| `likesCount` | Likes | Gist |
| `madeWithAi` | AI flag | Discord msg 1425527790723137548 |
| `metaTags { code name(locale: EN) }` | Meta tag support | Discord msg 1434835512383766588 |
| `tags(locale: EN)` | Tags list | Gist |
| `visibility` | Visibility state | Discord msg 1380539355180957859 |
| `totalSalesAmount(currency: USD) { value }` | Earnings | Discord msg 1356293103581008093 |
| `publishedAt` | Publish timestamp | Gist |
| `discount { percentage originalPrice startAt endAt }` | Current discount | Gist |
| `blueprints { fileUrl imageUrl }` | Files list | Gist |
| `illustrations { imageUrl position }` | Images list | Gist |

## User (user / myself.user)
| Field | Notes | Source |
| --- | --- | --- |
| `nick` | Username | Gist |
| `shortUrl` | Profile short URL | Gist |
| `bio` | Profile bio | Gist |
| `imageUrl` | Avatar URL | Gist |
| `followersCount` | Followers | Discord msg 1356293103581008093 |
| `creationsCount` | Creation count | Gist |
| `likedCreations(limit, offset)` | Likes list | Gist |

## Printlist (printlistsBatch results)
| Field | Notes | Source |
| --- | --- | --- |
| `id` | Printlist id | Discord msg 1346469900566401065 |
| `url` | Printlist URL | Discord msg 1346469900566401065 |
| `name` | Printlist name | Discord msg 1346469900566401065 |
| `public` | Visibility flag | Discord msg 1346469900566401065 |
| `position` | Ordering on profile | Gist |
| `creationsBatch(limit, offset)` | Nested creations | Discord msg 1346469900566401065 |

## Comment (commentsBatch results)
| Field | Notes | Source |
| --- | --- | --- |
| `publishedAt` | Comment timestamp | Discord screenshot (Jan 2026) |
| `creator { nick }` | Author summary | Discord screenshot (Jan 2026) |
| `text` | Comment body | Discord screenshot (Jan 2026) |
