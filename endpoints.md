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
| `printlistsBatch`, `addCreationToPrintlist` | Query/Mutation | Manage collections and embed their creations. | Discord |
| `ordersBatch`, `salesBatch` | Query | Pull purchases, download URLs, and sale income (with applied discount). | Gist + Discord |
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
> Hospede cada URL em HTTPS público. Veja `examples/upload-hosting.md` para hosts sugeridos e limite de 10 links por campo.

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
Discord replaced the legacy plural mutations with singular ones:
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
- **Trending / likes** (Discord answer to “how do I fetch most liked models?”)
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
- **Price filters** – `creationsBatch(onlyFree: true)` for free models, `creationsBatch(onlyPriced: true)` for paid ones, or `onlyDiscounted: true` to see active promotions.
- **Search** – gist `Search for a design.graphql`:
  ```graphql
  {
    creationsSearchBatch(query: "batman", limit: 3) {
      total
      results { name(locale: EN) shortUrl }
    }
  }
  ```
- **Made with AI flag** – Discord (Oct/2025) added `madeWithAi: false`:
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
- **Discount insight** – The `discount` object (percentage + original price + date window) is exposed both in `creationsBatch` (for discovery) and `salesBatch` (see below).

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

**Show a user** (gist)  
`user(nick: "bigovereasy") { shortUrl bio imageUrl creationsCount creations(limit: 3, sort: BY_LIKES) { name(locale: EN) shortUrl illustrationImageUrl } }`

**Likes** (gist)  
`myself { user { likedCreations(limit: 10, offset: 0) { name(locale: EN) url(locale: EN) } } }`

## Orders, Sales, and Commerce
**Orders with download URLs** (Discord May/2025)
```graphql
{
  myself {
    ordersBatch(limit: 20, offset: 0) {
      results {
        publicId
        createdAt
        price { currency cents }
        lines { downloadUrl }
      }
    }
  }
}
```
> The URLs returned inside `downloadUrl` still require your logged-in browser cookie to fetch. Sunny explicitly asked everyone to “give plenty of waiting time between requests” when automating downloads.

**Sales with applied discount** (Discord March/2025 update)
```graphql
{
  myself {
    salesBatch(limit: 3, offset: 0) {
      total
      results {
        id
        creation { name(locale: EN) }
        user { nick }
        income(currency: EUR) { cents }
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

**Create a discount** (gist)
```graphql
mutation {
  createDiscount(
    creationId: "Q3JlYXRpb24vMjIwMjQzMA"
    discountPercentage: 50
    discountEndAt: "2024-09-01T16:59:12+02:00"
  ) {
    discount {
      creation { name price { cents } }
      originalPrice { cents }
      percentage
    }
    errors
  }
}
```

## Reference Data
- **Categories** – `categories { id name(locale: EN) children { id name(locale: EN) } }`
- **Licenses** – `licenses { code name(locale: EN) url(locale: EN) availableOnFreeDesigns availableOnPricedDesigns }`
- **Meta tags** – Discord (Nov/2025) confirmed you can now read/write them:
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

## Notes & Best Practices
- Always check the `errors` array returned by each mutation; failed validations surface here even when HTTP status is 200.
- Keep `limit` and `offset` conservative (≤50 rows) to avoid timeouts.
- When mixing multiple queries, alias them to keep responses easy to parse.
- Cite the gist or Discord date when you add new operations so future readers know where they originated.
