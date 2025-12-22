import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


API_URL = os.environ.get("CULTS_API_URL", "https://cults3d.com/graphql")


def load_query() -> str:
    query_path = Path(__file__).resolve().parents[1] / "schema" / "introspection.graphql"
    return query_path.read_text(encoding="utf-8")


def build_headers(username: str, api_key: str) -> dict:
    token = base64.b64encode(f"{username}:{api_key}".encode("utf-8")).decode("ascii")
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }


def run_request(query: str, headers: dict) -> dict:
    payload = json.dumps({"query": query, "variables": {}}).encode("utf-8")
    request = urllib.request.Request(API_URL, data=payload, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")
    return json.loads(body)


def main() -> int:
    username = os.environ.get("CULTS_USERNAME")
    api_key = os.environ.get("CULTS_API_KEY")
    if not username or not api_key:
        print("Set CULTS_USERNAME and CULTS_API_KEY before running this script.")
        return 1

    query = load_query()
    headers = build_headers(username, api_key)

    try:
        payload = run_request(query, headers)
    except urllib.error.HTTPError as exc:
        print(f"HTTP error: {exc.code} {exc.reason}")
        return 1
    except urllib.error.URLError as exc:
        print(f"Network error: {exc.reason}")
        return 1

    if payload.get("errors"):
        print("GraphQL errors returned:")
        print(json.dumps(payload["errors"], indent=2))
        return 1

    output_path = Path(__file__).resolve().parents[1] / "schema" / "schema.snapshot.json"
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote schema snapshot to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
