# Changelog

This log tracks updates from the official gist and the `#api-help` Discord channel. Keep entries short and include the source and date.

## 2025-12 (Discord #api-help)
- Added `creationViewsCount` on `salesBatch` results to capture the view count at the time of sale. Source: Discord screenshot (Dec 2025, no msg id yet).

## 2025-11-03 (Discord #api-help)
- Meta tags are readable and writable on creations. Source: Discord msg 1434835512383766588.

## 2025-11-17 (Discord #api-help)
- Added `addCreationToPrintlist` to attach creations to collections. Source: Discord msg 1439933950192648252.

## 2025-10-08 (Discord #api-help)
- `madeWithAi: false` filter added to `creationsBatch`. Source: Discord msg 1425527790723137548.

## 2025-07-09 (Discord #api-help)
- No hard limit on total files per design. Prefer multiple STL files; large ZIPs remain supported. Source: Discord msg 1392455056405692508.

## 2025-07-02 (Discord #api-help)
- `ordersBatch` includes `publicId`, `createdAt`, and `price`. Source: Discord msg 1389915227767963692.

## 2025-05-14 (Discord #api-help)
- `ordersBatch` exposes `lines { downloadUrl }`. Source: Discord msg 1372299248560767106.

## 2025-05-27 (Discord #api-help)
- Added singular `createIllustration` and `createBlueprint` mutations with optional `position`, deprecating the plural forms. Source: Discord msg 1376995917026299984.

## 2025-04-04 (Discord #api-help)
- `imageUrl(version: DEFAULT)` returns the largest image variant. Source: Discord msg 1357745337367920790.

## 2025-04-02 (Discord #api-help)
- `viewsCount(cached: false)` returns uncached view counts. Source: Discord msg 1356293103581008093.
- Creator stats example includes `identifier`, `totalSalesAmount`, `visibility`, and `tags`. Source: Discord msg 1356293103581008093.

## 2025-03-04 (Discord #api-help)
- Printlists can expose nested creations via `creationsBatch`. Source: Discord msg 1346469900566401065.

## 2025-03-11 (Discord #api-help)
- `Sale.discount` added for sale-time discount visibility. Source: Discord msg 1348948518307631155.

## 2025-02-19 (Discord #api-help)
- `onlyPriced: true` filter added to `creationsBatch` and `creationsSearchBatch`. Source: Discord msg 1341723740572221492.

## 2025-02-14 (Discord #api-help)
- `submittedAfter` and `submittedBefore` filters added to `creationsBatch`. Source: Discord msg 1339885721154097172.
- `SaleType.vat` fixed to avoid errors. Source: Discord msg 1339886382696628314.

## Baseline (Gist)
- Core mutations and queries: `createCreation`, `updateCreation`, `createDiscount`, `creation`, `user`, `creationsBatch`, `creationsSearchBatch`, `ordersBatch`, `salesBatch`.
- Gist files: `Create a design.graphql`, `Update a creation price.graphql`, `Add a discount.graphql`, `Show a design.graphql`, `Show a user.graphql`, `Search for a design.graphql`, `Find discounted designs.graphql`, `Show your own designs and their files.graphql`, `List your sales.graphql`, `Show categories.graphql`, `List available licenses.graphql`.
