import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


API_URL = os.environ.get("CULTS_API_URL", "https://cults3d.com/graphql")

ROOT_QUERY = """
{
  __schema {
    queryType { name fields { name args { name } type { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } }
    mutationType { name fields { name args { name } type { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } }
  }
}
"""

TYPE_QUERY = """
query ($name: String!) {
  __type(name: $name) {
    name
    fields {
      name
      args { name }
      type { kind name ofType { kind name ofType { kind name ofType { kind name } } } }
    }
  }
}
"""


def build_headers(username: str, api_key: str) -> dict:
    token = base64.b64encode(f"{username}:{api_key}".encode("utf-8")).decode("ascii")
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }


def run_graphql(query: str, variables: dict | None, headers: dict) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    request = urllib.request.Request(API_URL, data=payload, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")
    result = json.loads(body)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]


def unwrap_type(type_info: dict | None) -> str | None:
    while type_info:
        name = type_info.get("name")
        if name:
            return name
        type_info = type_info.get("ofType")
    return None


def collect_fields(type_info: dict | None) -> dict:
    if not type_info or not type_info.get("fields"):
        return {}
    return {field["name"]: field for field in type_info["fields"]}


def main() -> int:
    username = os.environ.get("CULTS_USERNAME")
    api_key = os.environ.get("CULTS_API_KEY")
    strict = os.environ.get("STRICT", "0") == "1"

    if not username or not api_key:
        print("Set CULTS_USERNAME and CULTS_API_KEY before running this script.")
        return 1

    headers = build_headers(username, api_key)
    errors = []
    warnings = []

    try:
        root_data = run_graphql(ROOT_QUERY, None, headers)
    except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError) as exc:
        print(f"Root query failed: {exc}")
        return 1

    query_fields = {f["name"]: f for f in root_data["__schema"]["queryType"]["fields"]}
    mutation_fields = {f["name"]: f for f in root_data["__schema"]["mutationType"]["fields"]}

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def warn(condition: bool, message: str) -> None:
        if not condition:
            warnings.append(message)

    # Core queries
    for field in [
        "creation",
        "creationsBatch",
        "creationsSearchBatch",
        "ordersBatch",
        "salesBatch",
        "printlistsBatch",
        "user",
        "myself",
        "categories",
        "licenses",
    ]:
        require(field in query_fields, f"Missing query field: {field}")

    # Core mutations
    for field in [
        "createCreation",
        "updateCreation",
        "createBlueprint",
        "destroyBlueprint",
        "createIllustration",
        "destroyIllustration",
        "createDiscount",
    ]:
        require(field in mutation_fields, f"Missing mutation field: {field}")

    for field in ["addCreationToPrintlist", "updatePrintlist"]:
        warn(field in mutation_fields, f"Missing mutation field: {field}")

    update_printlist_args = {arg["name"] for arg in mutation_fields.get("updatePrintlist", {}).get("args", [])}
    for arg in ["id", "name", "public", "locale"]:
        warn(arg in update_printlist_args, f"updatePrintlist missing arg: {arg}")

    # Query args for creationsBatch
    creations_batch_args = {arg["name"] for arg in query_fields.get("creationsBatch", {}).get("args", [])}
    for arg in ["limit", "offset", "onlyFree", "onlyPriced", "onlyDiscounted"]:
        require(arg in creations_batch_args, f"creationsBatch missing arg: {arg}")
    for arg in ["submittedAfter", "submittedBefore", "madeWithAi"]:
        warn(arg in creations_batch_args, f"creationsBatch missing recent arg: {arg}")

    # Query args for creationsSearchBatch
    search_args = {arg["name"] for arg in query_fields.get("creationsSearchBatch", {}).get("args", [])}
    for arg in ["query", "limit", "offset"]:
        require(arg in search_args, f"creationsSearchBatch missing arg: {arg}")

    def get_type(name: str) -> dict | None:
        try:
            data = run_graphql(TYPE_QUERY, {"name": name}, headers)
        except RuntimeError:
            return None
        return data.get("__type")

    creation_fields = collect_fields(get_type("Creation"))
    sale_fields = collect_fields(get_type("Sale"))
    order_fields = collect_fields(get_type("Order"))
    user_fields = collect_fields(get_type("User"))
    printlist_fields = collect_fields(get_type("Printlist"))

    # Core creation fields
    for field in ["name", "url", "shortUrl", "price", "downloadsCount", "likesCount", "tags"]:
        require(field in creation_fields, f"Creation missing field: {field}")

    # Recent creation fields
    for field in ["identifier", "visibility", "totalSalesAmount", "metaTags", "madeWithAi"]:
        warn(field in creation_fields, f"Creation missing recent field: {field}")

    views_field = creation_fields.get("viewsCount")
    if views_field:
        view_args = {arg["name"] for arg in views_field.get("args", [])}
        warn("cached" in view_args, "Creation.viewsCount missing arg: cached")
    else:
        require(False, "Creation missing field: viewsCount")

    illustration_field = creation_fields.get("illustrationImageUrl")
    if illustration_field:
        illustration_args = {arg["name"] for arg in illustration_field.get("args", [])}
        warn("version" in illustration_args, "Creation.illustrationImageUrl missing arg: version")
    else:
        warn(False, "Creation missing field: illustrationImageUrl")

    # Sale fields
    for field in ["id", "createdAt", "payedOutAt", "income"]:
        require(field in sale_fields, f"Sale missing field: {field}")
    for field in ["discount", "creationViewsCount", "creationLikesCount"]:
        warn(field in sale_fields, f"Sale missing recent field: {field}")

    # SaleType.vat (optional)
    sale_type_fields = collect_fields(get_type("SaleType"))
    if sale_type_fields:
        warn("vat" in sale_type_fields, "SaleType missing field: vat")
    else:
        warn("vat" in sale_fields, "SaleType not found; check Sale.vat instead")

    # Order fields
    for field in ["lines"]:
        require(field in order_fields, f"Order missing field: {field}")
    for field in ["publicId", "createdAt", "price"]:
        warn(field in order_fields, f"Order missing recent field: {field}")

    # OrderLine downloadUrl
    order_lines = order_fields.get("lines")
    if order_lines:
        line_type = unwrap_type(order_lines.get("type"))
        if line_type:
            line_fields = collect_fields(get_type(line_type))
            warn("downloadUrl" in line_fields, f"{line_type} missing field: downloadUrl")
        else:
            warn(False, "Order.lines type could not be resolved")

    # User fields
    for field in ["nick", "shortUrl", "imageUrl", "creationsCount"]:
        require(field in user_fields, f"User missing field: {field}")
    warn("followersCount" in user_fields, "User missing recent field: followersCount")

    # Printlist fields
    for field in ["name", "public"]:
        require(field in printlist_fields, f"Printlist missing field: {field}")
    warn("creationsBatch" in printlist_fields, "Printlist missing recent field: creationsBatch")
    warn("position" in printlist_fields, "Printlist missing field: position")

    # Recent screenshot-backed additions (warning-level, introspection-only)

    # myself -> bundlesBatch + state arg (screenshots 2026-07-13, 2026-07-16 12:55)
    myself_field = query_fields.get("myself")
    myself_type = unwrap_type(myself_field.get("type")) if myself_field else None
    if myself_type:
        myself_type_info = get_type(myself_type)
        if myself_type_info is None:
            warn(False, f"{myself_type} type could not be resolved")
        else:
            myself_fields = collect_fields(myself_type_info)
            bundles_field = myself_fields.get("bundlesBatch")
            if bundles_field:
                bundles_args = {arg["name"] for arg in bundles_field.get("args", [])}
                warn("state" in bundles_args, f"{myself_type}.bundlesBatch missing arg: state")
            else:
                warn(False, f"{myself_type} missing field: bundlesBatch")
    else:
        warn(False, "Could not resolve the type of myself")

    # updateBundle + shown args (screenshot 2026-07-16 13:10)
    update_bundle = mutation_fields.get("updateBundle")
    warn(update_bundle is not None, "Missing mutation field: updateBundle")
    if update_bundle:
        update_bundle_args = {arg["name"] for arg in update_bundle.get("args", [])}
        for arg in ["id", "name", "description", "discountPercentage", "state"]:
            warn(arg in update_bundle_args, f"updateBundle missing arg: {arg}")

    # categories.safe (screenshot 2026-05-18)
    categories_args = {arg["name"] for arg in query_fields.get("categories", {}).get("args", [])}
    warn("safe" in categories_args, "categories missing arg: safe")

    # Creation.illustrations element fields (screenshot message date inferred as 2026-08-04)
    illustrations_field = creation_fields.get("illustrations")
    if illustrations_field:
        illustration_type = unwrap_type(illustrations_field.get("type"))
        if illustration_type:
            illustration_type_info = get_type(illustration_type)
            if illustration_type_info is None:
                warn(False, f"{illustration_type} type could not be resolved")
            else:
                illustration_fields = collect_fields(illustration_type_info)
                for field in ["id", "imageUrl"]:
                    warn(field in illustration_fields, f"{illustration_type} missing field: {field}")
        else:
            warn(False, "Creation.illustrations element type could not be resolved")
    else:
        warn(False, "Creation missing field: illustrations")

    # Creation.license.spdxId (screenshot 2026-07-30); resolve the nested type dynamically.
    license_field = creation_fields.get("license")
    if license_field:
        license_type = unwrap_type(license_field.get("type"))
        if license_type:
            license_type_info = get_type(license_type)
            if license_type_info is None:
                warn(False, f"{license_type} type could not be resolved")
            else:
                license_fields = collect_fields(license_type_info)
                warn("spdxId" in license_fields, f"{license_type} missing field: spdxId")
        else:
            warn(False, "Creation.license type could not be resolved")
    else:
        warn(False, "Creation missing field: license")

    if errors:
        print("Errors:")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("Warnings:")
        for item in warnings:
            print(f"- {item}")

    if errors:
        return 1
    if warnings and strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
