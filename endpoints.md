# Endpoints & GraphQL Operations

All requests call `https://cults3d.com/graphql` with a JSON body such as:

```json
{
  "query": "query Example { categories { id name(locale: EN) } }",
  "variables": {}
}
```

## Summary Table
| Operation | Type | Purpose | Source |
| --- | --- | --- | --- |
| `createCreation` | Mutation | Publish a new design (metadata + inline `fileUrls` / `imageUrls`). | Gist `Create a design.graphql` |
| `updateCreation` | Mutation | Modify any mutable field or adjust price only. | Gist `Update a creation price.graphql` |
| `createBlueprint` / `createIllustration` | Mutation | Attach a hosted ZIP/PNG to a creation. | Discord (`#api-help`) |
| `destroyBlueprint` / `destroyIllustration` | Mutation | Remove obsolete files or renders. | Discord |
| `creation(slug)` | Query | Fetch ID, URL, and asset lists. | Gist `Show a design.graphql` |
| `creationsBatch`, `creationsSearchBatch` | Query | Discovery with sort, paging, price/date filters, and `madeWithAi`. | Gist + Discord |
| `printlistsBatch`, `createPrintlist`, `destroyPrintlist`, `addCreationToPrintlist`, `removeCreationFromPrintlist` | Query/Mutation | Manage collections, including creation add/remove and deletion. | Discord |
| `myself.commentsBatch` | Query | Read public message board comments. | Discord |
| `ordersBatch`, `salesBatch` | Query | Pull purchases, download URLs, sale income, discounts, and sale-time view/like snapshots. | Gist + Discord |
| `categories`, `licenses`, `user`, `myself` | Query | Reference data, user profile, likes, dashboard stats. | Gist |
| `createDiscount` | Mutation | Schedule a promotion for a creation. | Gist `Add a discount.graphql` |

Sections below expand on each group with ready-to-use snippets.

## Creations & Metadata
**Create a design** (gist)
```graphql
mutation {
  createCreation(
    name: "Cults Logo"
    description: "A Cults logo, to test the API"
    imageUrls: ["https://wtf.sunfox.org/3d/cults-logo.jpg"]
    fileUrls: ["https://wtf.sunfox.org/3d/cults-logo.stl"]
    locale: EN
    categoryId: "Q2F0ZWdvcnkvMjM="
    subCategoryIds: ["Q2F0ZWdvcnkvMzc"]
    downloadPrice: 42.5
    currency: EUR
    licenseCode: "cults_cu"
    tagNames: ["Miniature", "Sci-Fi"]
    metaTags: ["3DP_TOOLTIP"]
    madeWithAi: false
  ) {
    creation { id url(locale: EN) }
    errors
  }
}
```
> Host each URL on public HTTPS. See `examples/upload-hosting.md` for direct Google Drive links and keep each field to 10 links. `fileUrls` accepts up to 10 files per request; attach more files later via `createBlueprint`.
> Source: Gist `Create a design.graphql`; meta tags (Discord msg 1434835512383766588); `madeWithAi` (Discord msg 1425527790723137548).

**Update a creation** (gist + Discord meta-tag announcement)
```graphql
mutation {
  updateCreation(
    id: "CREATION_ID"
    name: "New Title"
    description: "Updated description"
    downloadPrice: 7.0
    currency: EUR
    licenseCode: "cults_cu_nd"
    tagNames: ["resin", "tabletop"]
    metaTags: ["CultsHighlight"]
    madeWithAi: false
  ) {
    creation { id url(locale: EN) }
    errors
  }
}
```
For price-only edits, pass just `id`, `downloadPrice`, and `currency`.
> Source: Gist `Update a creation price.graphql`; meta tags (Discord msg 1434835512383766588); `madeWithAi` (Discord msg 1425527790723137548).

**Snapshot an existing creation**
```graphql
query ($slug: String!, $locale: LocaleEnum!) {
  creation(slug: $slug) {
    id
    url(locale: $locale)
    blueprints { id fileUrl position }
    illustrations { id imageUrl position }
  }
}
```
Use this before updating assets so you can compare desired vs existing files.

## Asset Mutations
Discord replaced the legacy plural mutations with singular ones that accept optional `position`. Source: Discord msg 1376995917026299984.
```graphql
mutation {
  createBlueprint(
    creationId: "CREATION_ID"
    fileUrl: "https://cdn.example.com/model.zip"
    position: 1
  ) {
    blueprint { id }
    errors
  }
}

mutation {
  destroyBlueprint(id: "BLUEPRINT_ID") {
    errors
  }
}

mutation {
  createIllustration(
    creationId: "CREATION_ID"
    imageUrl: "https://cdn.example.com/render.png"
    position: 1
  ) {
    illustration { id }
    errors
  }
}

mutation {
  destroyIllustration(id: "ILLUSTRATION_ID") {
    errors
  }
}
```
Send calls sequentially (or in small batches) with a pause between them to honor rate limits.

## Discovery & Filters
- **Trending / likes** (Discord answer to "how do I fetch most liked models?")
  ```graphql
  {
    creationsBatch(sort: BY_LIKES, limit: 3) {
      results {
        name(locale: EN)
        shortUrl
        likesCount
        downloadsCount
      }
    }
  }
  ```
  > Source: Discord msg 1341078782638821440.
- **Downloads within a date window**
  ```graphql
  {
    creationsBatch(
      sort: BY_DOWNLOADS
      submittedAfter: "2025-01-01T00:00:00+00:00"
      submittedBefore: "2025-01-31T23:59:59+00:00"
    ) {
      results { name(locale: EN) shortUrl downloadsCount }
    }
  }
  ```
  > Source: Discord msg 1339885721154097172.
- **Price filters** - `creationsBatch(onlyFree: true)` for free models, `creationsBatch(onlyPriced: true)` for paid ones, or `onlyDiscounted: true` to see active promotions.
  > Source: Discord msg 1341723740572221492.
- **Search** - gist `Search for a design.graphql`:
  ```graphql
  {
    creationsSearchBatch(query: "batman", limit: 3) {
      total
      results { name(locale: EN) shortUrl }
    }
  }
  ```
  > Discord posts sometimes refer to `searchCreationsBatch`. The gist and schema use `creationsSearchBatch`; verify the actual field name in GraphiQL and use that.
  > Source: Gist `Search for a design.graphql`.
- **Made with AI flag** - Discord (Oct/2025) added `madeWithAi: false`:
  ```graphql
  {
    creationsBatch(madeWithAi: false) {
      results {
        url
        madeWithAi
      }
    }
  }
  ```
  > Source: Discord msg 1425527790723137548.
- **Discount insight** - The `discount` object (percentage + original price + date window) is exposed both in `creationsBatch` (for discovery) and `salesBatch` (see below).
  > Source: Discord msg 1348948518307631155.
- **Pagination** - use `limit` + `offset` and advance the offset for the next page.
  > Source: Discord msg 1437160159154540574.

## Collections, Likes, and Users
**Printlists with embedded creations** (Discord March/2025)
```graphql
{
  myself {
    printlistsBatch(limit: 2, offset: 0) {
      total
      results {
        id
        url
        name
        public
        creationsBatch(limit: 2) {
          total
          results { shortUrl }
        }
      }
    }
  }
}
```
> Source: Discord msg 1346469900566401065.

**Create a printlist** (Discord Jan/2026)
```graphql
mutation {
  createPrintlist(name: "A test") {
    errors
    printlist { id url }
  }
}
```
> Source: Discord screenshot (Jan 2026).

**Add a design to a collection** (Discord November/2025)
```graphql
mutation {
  addCreationToPrintlist(creationId: "CREATION_ID", printlistId: "PRINTLIST_ID") {
    errors
    printlistItem {
      creation { name url }
      printlist { name url }
    }
  }
}
```
> Source: Discord msg 1439933950192648252.

**Remove a design from a collection** (Discord Jan/2026)
```graphql
mutation {
  removeCreationFromPrintlist(creationId: "CREATION_ID", printlistId: "PRINTLIST_ID") {
    errors
  }
}
```
> Source: Discord screenshot (Jan 2026).

**Delete a printlist** (Discord Jan/2026)
```graphql
mutation {
  destroyPrintlist(id: "PRINTLIST_ID") {
    errors
  }
}
```
> Source: Discord screenshot (Jan 2026).

**Show a user** (gist)  
`user(nick: "bigovereasy") { shortUrl bio imageUrl followersCount creationsCount creations(limit: 3, sort: BY_LIKES) { name(locale: EN) shortUrl illustrationImageUrl } }`
> Source: Gist `Show a user.graphql`.

**Likes** (gist)  
`myself { user { likedCreations(limit: 10, offset: 0) { name(locale: EN) url(locale: EN) } } }`
> Source: Gist `Show your likes.graphql`.

**Public message board comments** (Discord Jan/2026)
```graphql
{
  myself {
    commentsBatch {
      total
      results {
        publishedAt
        creator { nick }
        text
      }
    }
  }
}
```
> Args were not shown in the Discord snippet; check GraphiQL for `limit` / `offset` if needed.
> Source: Discord screenshot (Jan 2026).

**My designs with stats + files** (gist + Discord Apr/2025)
```graphql
{
  myself {
    user { nick imageUrl followersCount }
    creationsBatch(limit: 10, offset: 0) {
      total
      results {
        identifier
        name(locale: EN)
        url(locale: EN)
        illustrationImageUrl
        downloadsCount
        viewsCount(cached: false)
        totalSalesAmount(currency: USD) { value }
        visibility
        tags(locale: EN)
        blueprints { fileUrl imageUrl }
      }
    }
  }
}
```
> Use `viewsCount(cached: false)` for the freshest numbers. Omit the argument if you prefer cached values.
> Source: Gist `Show your own designs and their files.graphql` + Discord msg 1356293103581008093.

## Orders, Sales, and Commerce
**Orders with download URLs** (Discord May/2025)
```graphql
{
  myself {
    ordersBatch(limit: 20, offset: 0) {
      results {
        publicId
        createdAt
        price { currency value }
        lines { downloadUrl }
      }
    }
  }
}
```
> The URLs returned inside `downloadUrl` still require your logged-in browser cookie to fetch. Sunny explicitly asked everyone to "give plenty of waiting time between requests" when automating downloads.
> Source: Discord msg 1372299248560767106, msg 1389915227767963692.

**Sales with applied discount + view/like snapshots** (Discord March/2025; views snapshot Dec/2025; likes snapshot Jan/2026)
```graphql
{
  myself {
    salesBatch(limit: 3, offset: 0) {
      total
      results {
        id
        creation { name(locale: EN) }
        user { nick }
        income(currency: EUR) { value }
        creationViewsCount
        creationLikesCount
        createdAt
        payedOutAt
        discount {
          percentage
          startAt
          endAt
        }
      }
    }
  }
}
```
> `creationViewsCount` is a snapshot from the sale time (Dec/2025), not a live counter.
> `creationLikesCount` is a sale-time likes snapshot (Jan/2026) and only populated for sales after that date.
> SaleType also exposes `vat` (fixed Feb/2025) if you need tax details.
> Source: Discord msg 1348948518307631155 (discount), msg 1339886382696628314 (vat), Dec/2025 screenshot for `creationViewsCount`, Jan/2026 screenshot for `creationLikesCount`.

**Create a discount** (gist)
```graphql
mutation {
  createDiscount(
    creationId: "Q3JlYXRpb24vMjIwMjQzMA"
    discountPercentage: 50
    discountEndAt: "2024-09-01T16:59:12+02:00"
  ) {
    discount {
      creation { name(locale: EN) price { value } }
      originalPrice { value }
      percentage
    }
    errors
  }
}
```
> Source: Gist `Add a discount.graphql`.

## Reference Data
- **Categories** - `categories { id name(locale: EN) children { id name(locale: EN) } }`
- **Licenses** - `licenses { code name(locale: EN) url(locale: EN) availableOnFreeDesigns availableOnPricedDesigns }`
- **Meta tags** - Discord (Nov/2025) confirmed you can now read/write them:
  ```graphql
  {
    myself {
      creationsBatch(limit: 3) {
        results {
          metaTags {
            code
            name(locale: EN)
          }
        }
      }
    }
  }
  ```
  Pass `metaTags: ["featured", "highlight"]` in `createCreation` or `updateCreation` to set them.
  > Source: Discord msg 1434835512383766588.

## Images
**Largest image variant** (Discord Apr/2025)
```graphql
{
  creation(slug: "print-in-place-cute-lucky-bunny") {
    illustrationImageUrl(version: DEFAULT)
    illustrations {
      imageUrl(version: DEFAULT)
    }
  }
}
```
> Source: Discord msg 1357745337367920790.

## Notes & Best Practices
- Always check the `errors` array returned by each mutation; failed validations surface here even when HTTP status is 200.
- Keep `limit` and `offset` conservative (around 50 rows) to avoid timeouts; community reports suggest results may cap around 100 rows anyway. Source: Discord msg 1435688751140442234.
- When mixing multiple queries, alias them to keep responses easy to parse.
- Cite the gist or Discord date when you add new operations so future readers know where they originated.
