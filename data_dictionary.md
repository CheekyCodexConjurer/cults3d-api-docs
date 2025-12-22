# Data Dictionary

This file defines the core objects and fields used in the Cults3D GraphQL API. Use GraphiQL to confirm field names in your schema and see `field_matrix.md` for a compact checklist.

## Conventions
- **Locale** - Most human-readable fields accept `locale: EN`.
- **Currency** - Money fields accept `currency: EUR` or `USD`. The gist uses `cents`; Discord examples use `value`.
- **Pagination** - Batch endpoints use `limit` and `offset`.
- **IDs** - IDs are opaque base64 strings (e.g., `Q2F0ZWdvcnkvMjM=`).

## Root Queries (ApplicationQuery)
| Field | Purpose | Key arguments | Source |
| --- | --- | --- | --- |
| `creation(slug)` | Fetch a single design and its metadata | `slug` | Gist `Show a design.graphql` |
| `creationsBatch` | List designs with filters | `limit`, `offset`, `sort`, `onlyFree`, `onlyPriced`, `onlyDiscounted`, `submittedAfter`, `submittedBefore`, `madeWithAi` | Gist + Discord msg 1339885721154097172, 1341723740572221492, 1425527790723137548 |
| `creationsSearchBatch` | Search designs by query | `query`, `limit`, `offset` | Gist `Search for a design.graphql` |
| `printlistsBatch` | List user collections | `limit`, `offset` | Discord msg 1346469900566401065 |
| `ordersBatch` | List purchases and download URLs | `limit`, `offset` | Discord msg 1372299248560767106, 1389915227767963692 |
| `salesBatch` | List sales events | `limit`, `offset` | Gist `List your sales.graphql` |
| `user(nick)` | Public user profile | `nick` | Gist `Show a user.graphql` |
| `myself` | Current user scope | none | Gist |
| `categories` | Category tree | none | Gist `Show categories.graphql` |
| `licenses` | License catalog | none | Gist `List available licenses.graphql` |

## Mutations (ApplicationMutation)
| Field | Purpose | Key arguments | Source |
| --- | --- | --- | --- |
| `createCreation` | Publish a design | `name`, `description`, `categoryId`, `subCategoryIds`, `downloadPrice`, `currency`, `licenseCode`, `imageUrls`, `fileUrls`, `tagNames`, `metaTags`, `madeWithAi` | Gist `Create a design.graphql` + Discord msg 1434835512383766588, 1425527790723137548 |
| `updateCreation` | Update metadata or price | `id`, `downloadPrice`, `currency`, `name`, `description`, `tagNames`, `metaTags`, `madeWithAi` | Gist `Update a creation price.graphql` + Discord msg 1434835512383766588, 1425527790723137548 |
| `createBlueprint` | Attach a printable file | `creationId`, `fileUrl`, `position` | Discord msg 1376995917026299984 |
| `destroyBlueprint` | Remove a printable file | `id` | Discord msg 1376995917026299984 |
| `createIllustration` | Attach an image | `creationId`, `imageUrl`, `position` | Discord msg 1376995917026299984 |
| `destroyIllustration` | Remove an image | `id` | Discord msg 1376995917026299984 |
| `createDiscount` | Schedule a discount | `creationId`, `discountPercentage`, `discountEndAt` | Gist `Add a discount.graphql` |
| `addCreationToPrintlist` | Add a creation to a collection | `creationId`, `printlistId` | Discord msg 1439933950192648252 |

## Creation
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `identifier` | Internal identifier string | Useful for analytics exports | Discord msg 1356293103581008093 |
| `name(locale)` | Localized name | Use `locale: EN` for English | Gist |
| `url(locale)` | Localized URL | Use `locale: EN` for English | Gist |
| `shortUrl` | Short link | Often used in UIs | Gist |
| `publishedAt` | Publish timestamp | ISO-8601 | Gist |
| `price(currency)` | Price object | Money type; `value` vs `cents` | Gist |
| `discount` | Current discount | `percentage`, `startAt`, `endAt`, `originalPrice` | Gist `Find discounted designs.graphql` |
| `downloadsCount` | Download count | Integer | Gist |
| `likesCount` | Like count | Integer | Gist |
| `viewsCount(cached)` | View count | `cached: false` for fresh | Discord msg 1356293103581008093 |
| `creationViewsCount` | Sale-time views | Only in `salesBatch` results | Discord screenshot (Dec 2025) |
| `madeWithAi` | AI usage flag | Filterable in `creationsBatch` | Discord msg 1425527790723137548 |
| `metaTags` | Meta tag list | Read/write via mutations | Discord msg 1434835512383766588 |
| `tags(locale)` | Tag list | Localized | Gist |
| `visibility` | Visibility state | Use for deactivated/secret | Discord msg 1380539355180957859 |
| `totalSalesAmount(currency)` | Sales total | Money type | Discord msg 1356293103581008093 |
| `illustrationImageUrl` | Cover image | Use `version: DEFAULT` for large | Discord msg 1357745337367920790 |
| `illustrations` | Image list | `imageUrl`, `position` | Gist |
| `blueprints` | File list | `fileUrl`, `imageUrl` | Gist |

## Sale
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `id` | Sale ID | Opaque string | Gist |
| `createdAt` | Sale timestamp | ISO-8601 | Gist |
| `payedOutAt` | Payout timestamp | ISO-8601 | Gist |
| `income(currency)` | Money object | `value` vs `cents` | Gist + Discord msg 1356293103581008093 |
| `discount` | Sale-time discount | `percentage`, `startAt`, `endAt` | Discord msg 1348948518307631155 |
| `creationViewsCount` | Views at sale time | Snapshot | Discord screenshot (Dec 2025) |
| `user` | Buyer info | `nick` | Gist |

## SaleType
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `vat` | VAT amount | Fixed to avoid errors | Discord msg 1339886382696628314 |

## Order
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `publicId` | Public order id | String | Discord msg 1389915227767963692 |
| `createdAt` | Order timestamp | ISO-8601 | Discord msg 1389915227767963692 |
| `price` | Money object | `value` vs `cents` | Discord msg 1389915227767963692 |
| `lines` | Purchased items | See `OrderLine` | Discord msg 1372299248560767106 |

## OrderLine
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `downloadUrl` | Download URL | Requires browser cookie | Discord msg 1372299248560767106 |

## User
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `nick` | Username | Unique handle | Gist |
| `shortUrl` | Profile short URL | Short link | Gist |
| `bio` | Profile bio | Text | Gist |
| `imageUrl` | Avatar URL | Image | Gist |
| `followersCount` | Followers | Integer | Discord msg 1356293103581008093 |
| `creationsCount` | Number of creations | Integer | Gist |
| `likedCreations` | Liked designs | Use `limit` + `offset` | Gist |

## Printlist
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `id` | Printlist id | Opaque string | Discord msg 1346469900566401065 |
| `url` | Printlist URL | Short link | Discord msg 1346469900566401065 |
| `name` | Printlist name | Text | Discord msg 1346469900566401065 |
| `public` | Visibility flag | Boolean | Discord msg 1346469900566401065 |
| `position` | Ordering on profile | Integer | Gist `List my printlists.graphql` |
| `creationsBatch` | Nested creations | Use `limit` + `offset` | Discord msg 1346469900566401065 |

## Category
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `id` | Category id | Base64 | Gist |
| `name(locale)` | Localized name | Use `locale: EN` | Gist |
| `children` | Subcategories | Nested categories | Gist |

## License
| Field | Meaning | Notes | Source |
| --- | --- | --- | --- |
| `code` | License code | Pass to `licenseCode` | Gist |
| `name(locale)` | Localized name | Use `locale: EN` | Gist |
| `url(locale)` | License URL | Use `locale: EN` | Gist |
| `availableOnFreeDesigns` | Eligibility | Boolean | Gist |
| `availableOnPricedDesigns` | Eligibility | Boolean | Gist |

## Money / Price Types
| Type | Field | Notes |
| --- | --- | --- |
| `MoneyType` | `value` or `cents` | Confirm name in GraphiQL |
| `MoneyType` | `currency` | Enum (EUR, USD, etc.) |
| `PriceType` | `value` or `cents` | Confirm name in GraphiQL |
| `PriceType` | `currency` | Enum (EUR, USD, etc.) |
