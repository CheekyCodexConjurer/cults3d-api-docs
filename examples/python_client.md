# Python Client Examples

These snippets use only `requests` and the public GraphQL operations referenced in `endpoints.md`. They assume:
- `pip install requests`
- Environment variables `CULTS_USERNAME` and `CULTS_API_KEY` hold your credentials (or pass them explicitly).

```python
import base64
import os
import requests

API_URL = "https://cults3d.com/graphql"

def run_graphql(query: str, variables: dict | None = None, *, username=None, api_key=None):
    """Helper that executes a GraphQL operation and raises on API errors."""
    username = username or os.environ["CULTS_USERNAME"]
    api_key = api_key or os.environ["CULTS_API_KEY"]
    token = base64.b64encode(f"{username}:{api_key}".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        API_URL,
        json={"query": query, "variables": variables or {}},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(f"Cults3D API error: {payload['errors']}")
    return payload["data"]
```

## Validation Helper
```python
VALIDATION_QUERY = "{ categories { id name(locale: EN) } }"

VALIDATION_CREATE_MUTATION = """
mutation ValidateCreation(
  $name: String!, $description: String!, $category: ID!, $price: Float!, $license: LicenseCodeEnum!
) {
  createCreation(
    name: $name
    description: $description
    imageUrls: []
    fileUrls: []
    locale: EN
    categoryId: $category
    subCategoryIds: []
    downloadPrice: $price
    currency: EUR
    licenseCode: $license
    tagNames: ["validation"]
    metaTags: []
    madeWithAi: false
  ) {
    creation { id url(locale: EN) }
    errors
  }
}
"""

def validate_api():
    """Runs a query + mutation to confirm credentials, schema access, and write paths."""
    print("Schema probe:", run_graphql("{ __typename }"))
    print("Categories sample:", run_graphql(VALIDATION_QUERY))
    payload = {
        # Use safe/test data; remove the created draft manually after validating.
        "name": "API Validation Draft",
        "description": "Temporary entry created to validate access.",
        "category": "Q2F0ZWdvcnkvMjM=",
        "price": 1.0,
        "license": "cults_cu",
    }
    result = run_graphql(VALIDATION_CREATE_MUTATION, payload)
    print("Mutation result:", result["createCreation"])
```

## Create a Design
```python
create_mutation = """
mutation Create(
  $name: String!, $description: String!, $category: ID!, $subCategories: [ID!],
  $price: Float!, $currency: CurrencyEnum!, $license: LicenseCodeEnum!,
  $tags: [String!], $meta: [CreationMetaTagCode!]
) {
  createCreation(
    name: $name
    description: $description
    imageUrls: []
    fileUrls: []
    locale: EN
    categoryId: $category
    subCategoryIds: $subCategories
    downloadPrice: $price
    currency: $currency
    licenseCode: $license
    tagNames: $tags
    metaTags: $meta
    madeWithAi: false
  ) {
    creation { id url(locale: EN) }
    errors
  }
}
"""

data = run_graphql(
    create_mutation,
    variables={
        "name": "Demo Statue",
        "description": "Uploaded via GraphQL",
        "category": "Q2F0ZWdvcnkvMjM=",
        "subCategories": ["Q2F0ZWdvcnkvMzc"],
        "price": 7.0,
        "currency": "EUR",
        "license": "cults_cu",
        "tags": ["robot", "statue"],
        "meta": ["CultsHighlight"],
    },
)
creation_id = data["createCreation"]["creation"]["id"]
print("Creation URL:", data["createCreation"]["creation"]["url"])
```
Attach assets afterward via `createBlueprint` / `createIllustration` once the ZIPs and renders are hosted.

## Update a Price or Metadata Field
```python
update_mutation = """
mutation Update($id: ID!, $price: Float!) {
  updateCreation(id: $id, downloadPrice: $price, currency: EUR) {
    creation { url(locale: EN) }
    errors
  }
}
"""

run_graphql(update_mutation, {"id": creation_id, "price": 8.5})
```
You can include any other mutable field (description, tags, metaTags, madeWithAi, etc.) in the same mutation.

## Attach a Blueprint
```python
add_blueprint = """
mutation Attach($creationId: ID!, $url: String!, $position: Int!) {
  createBlueprint(creationId: $creationId, fileUrl: $url, position: $position) {
    blueprint { id }
    errors
  }
}
"""

run_graphql(
    add_blueprint,
    {"creationId": creation_id, "url": "https://cdn.example.com/demo.zip", "position": 1},
)
```

## Fetch Orders and Download URLs
```python
orders_query = """
{
  myself {
    ordersBatch(limit: 5, offset: 0) {
      results {
        publicId
        createdAt
        price { currency cents }
        lines { downloadUrl }
      }
    }
  }
}
"""

orders = run_graphql(orders_query)["myself"]["ordersBatch"]["results"]
for order in orders:
    print(order["publicId"], "->", [line["downloadUrl"] for line in order["lines"]])
print("Remember: fetching the download URLs themselves still requires your browser cookie.")
```

## List Printlists with Their Creations
```python
printlists_query = """
{
  myself {
    printlistsBatch(limit: 2, offset: 0) {
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
"""

printlists = run_graphql(printlists_query)["myself"]["printlistsBatch"]["results"]
for entry in printlists:
    print(entry["name"], "→", [c["shortUrl"] for c in entry["creationsBatch"]["results"]])
```

## Handling Errors
Wrap calls in `try/except` to catch both HTTP issues and GraphQL validation failures:
```python
try:
    run_graphql(update_mutation, {"id": creation_id, "price": -1})
except Exception as exc:
    print("API rejected the update:", exc)
```

## Tips
- Watch for `x-ratelimit-*` headers in `response.headers` if you need to throttle dynamically.
- Keep asset attachments serialized or batched in tiny groups; Discord confirms the API throttles bursts quickly.
- When experimenting, test read-only queries first to confirm your credentials before attempting mutations.
