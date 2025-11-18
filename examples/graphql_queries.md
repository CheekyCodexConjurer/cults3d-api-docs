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
      price { cents }
      shortUrl
      downloadsCount
      publishedAt
    }
  }
}
```

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

## Add Design to a Collection
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

## Price Filters
```graphql
{
  freeOnly: creationsBatch(onlyFree: true, limit: 2) {
    results { name(locale: EN) shortUrl }
  }
  paidOnly: creationsBatch(onlyPriced: true, limit: 2) {
    results { name(locale: EN) shortUrl price { cents } }
  }
}
```

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

## Orders + Download URLs
```graphql
{
  myself {
    ordersBatch(limit: 3) {
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
> Download URLs must be fetched with a logged-in browser session (per Discord guidance). Automations should reuse session cookies or prompt the user.

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
          name
          identifier
          price { value }
        }
      }
    }
  }
}
```

## Discounted Discoverability
```graphql
{
  creationsBatch(onlyDiscounted: true) {
    results {
      name(locale: EN)
      shortUrl
      price(currency: EUR) { cents }
      discount {
        percentage
        originalPrice(currency: EUR) { cents }
        startAt
        endAt
      }
    }
  }
}
```

## Manual Discount Creation
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

## User Snapshot
```graphql
{
  user(nick: "bigovereasy") {
    shortUrl
    bio
    imageUrl
    creationsCount
    creations(limit: 3, sort: BY_LIKES) {
      name(locale: EN)
      shortUrl
      illustrationImageUrl
    }
  }
}
```

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
