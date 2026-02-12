# GraphQL Examples

All snippets below work against `https://cults3d.com/graphql` with the proper API key. They originate from the official gist plus Discord announcements. Adjust locales, limits, and slugs to match your account.

## Trending Designs
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

## Latest Submissions After a Date
```graphql
{
  creationsBatch(
    sort: BY_DOWNLOADS
    limit: 3
    submittedAfter: "2025-01-18T13:36:44+01:00"
  ) {
    results {
      name(locale: EN)
      price { value }
      shortUrl
      downloadsCount
      publishedAt
    }
  }
}
```
> Source: Discord msg 1339885721154097172.

## Downloads Between Dates
```graphql
{
  creationsBatch(
    sort: BY_DOWNLOADS
    submittedAfter: "2025-01-01T00:00:00+00:00"
    submittedBefore: "2025-01-31T23:59:59+00:00"
  ) {
    results {
      name(locale: EN)
      downloadsCount
      publishedAt
    }
  }
}
```
> Source: Discord msg 1339885721154097172.

## Printlists & Embedded Designs
```graphql
{
  myself {
    printlistsBatch(limit: 2) {
      total
      results {
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

## Create a Printlist
```graphql
mutation {
  createPrintlist(name: "Sheet Sync", public: true) {
    errors
    printlist { id url }
  }
}
```
> Optional `public: true` creates a public list; omit it for private.
> Source: Discord screenshot (Jan 2026) + Discord screenshot (Jan 22, 2026).

## Update a Printlist
```graphql
mutation {
  updatePrintlist(id: "f00b4r42xGebla", name: "Mine ♥", public: false, locale: EN) {
    errors
    printlist {
      name(locale: EN)
      public
    }
  }
}
```

## Add Design to a Collection
```graphql
mutation {
  addCreationToPrintlist(creationId: "CREATION_ID", printlistId: "PRINTLIST_ID") {
    errors
    printlistItem {
      creation { name(locale: EN) url }
      printlist { name url }
    }
  }
}
```
> Source: Discord msg 1439933950192648252.

## Remove Design From a Collection
```graphql
mutation {
  removeCreationFromPrintlist(creationId: "CREATION_ID", printlistId: "PRINTLIST_ID") {
    errors
  }
}
```
> Source: Discord screenshot (Jan 2026).

## Delete a Printlist
```graphql
mutation {
  destroyPrintlist(id: "PRINTLIST_ID") {
    errors
  }
}
```
> Source: Discord screenshot (Jan 2026).

## Notify Previous Downloaders
```graphql
mutation {
  createChangeNotification(
    creationId: "CREATION_ID"
    text: "Updated the STL to fix supports."
  ) {
    errors
  }
}
```
> Source: Discord screenshot (Jan 20, 2026).

## Price Filters
```graphql
{
  freeOnly: creationsBatch(onlyFree: true, limit: 2) {
    results { name(locale: EN) shortUrl }
  }
  paidOnly: creationsBatch(onlyPriced: true, limit: 2) {
    results { name(locale: EN) shortUrl price { value } }
  }
}
```
> Source: Discord msg 1341723740572221492.

## Metadata & Meta Tags
```graphql
{
  myself {
    creationsBatch(limit: 3) {
      results {
        name(locale: EN)
        metaTags {
          code
          name(locale: EN)
        }
      }
    }
  }
}
```
> Source: Discord msg 1434835512383766588.

## Orders + Download URLs
```graphql
{
  myself {
    ordersBatch(limit: 3) {
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
> Download URLs must be fetched with a logged-in browser session (per Discord guidance). Automations should reuse session cookies or prompt the user.
> Source: Discord msg 1372299248560767106, msg 1389915227767963692.

## Sales With Discounts
```graphql
{
  myself {
    salesBatch(limit: 3) {
      results {
        id
        income { value }
        discount { percentage startAt endAt }
        creation {
          name(locale: EN)
          price { value }
        }
        creationViewsCount
        creationLikesCount
      }
    }
  }
}
```
> Discord Jan/2026: `creationLikesCount` in `salesBatch` is the likes count at the moment of sale and is only populated for new sales.
> Discord Dec/2025: `creationViewsCount` in `salesBatch` is the view count at the moment of sale.
> Source: Discord msg 1348948518307631155 (discount), Dec/2025 screenshot for `creationViewsCount`, Jan/2026 screenshot for `creationLikesCount`.

## Discounted Discoverability
```graphql
{
  creationsBatch(onlyDiscounted: true) {
    results {
      name(locale: EN)
      shortUrl
      price(currency: EUR) { value }
      discount {
        percentage
        originalPrice(currency: EUR) { value }
        startAt
        endAt
      }
    }
  }
}
```
> Source: Gist `Find discounted designs.graphql`.

## Manual Discount Creation
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

## Search
```graphql
{
  creationsSearchBatch(query: "batman", limit: 3) {
    total
    results {
      name(locale: EN)
      shortUrl
    }
  }
}
```
> Source: Gist `Search for a design.graphql`.

## Pagination (Offset)
```graphql
{
  creationsBatch(limit: 50, offset: 100) {
    results {
      name(locale: EN)
      shortUrl
    }
  }
}
```
> Source: Discord msg 1437160159154540574.

## User Snapshot
```graphql
{
  user(nick: "bigovereasy") {
    shortUrl
    bio
    imageUrl
    followersCount
    creationsCount
    creations(limit: 3, sort: BY_LIKES) {
      name(locale: EN)
      shortUrl
      illustrationImageUrl
    }
  }
}
```
> Source: Gist `Show a user.graphql` + Discord msg 1356293103581008093 (followers).

## Personal Likes
```graphql
{
  myself {
    user {
      likedCreations(limit: 10) {
        name(locale: EN)
        url(locale: EN)
      }
    }
  }
}
```
> Source: Gist `Show your likes.graphql`.

## Public Message Board Comments
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
> Source: Discord screenshot (Jan 2026).

## My Designs + Stats (Uncached Views)
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
> Omit `cached: false` if cached view counts are acceptable.
> Source: Gist `Show your own designs and their files.graphql` + Discord msg 1356293103581008093.

## Made-With-AI Filter
```graphql
{
  creationsBatch(madeWithAi: false, limit: 5) {
    results {
      url
      madeWithAi
    }
  }
}
```
> Source: Discord msg 1425527790723137548.

## High-Resolution Images
```graphql
{
  creation(slug: "print-in-place-cute-lucky-bunny") {
    name(locale: EN)
    illustrationImageUrl(version: DEFAULT)
    illustrations {
      imageUrl(version: DEFAULT)
    }
  }
}
```
> Source: Discord msg 1357745337367920790.
