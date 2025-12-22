# Schema Capture

This folder stores the GraphQL schema snapshot and the introspection query used to capture it. Use these artifacts when you need to verify field names or detect drift.

## Prerequisites
- Set `CULTS_USERNAME` and `CULTS_API_KEY` in your environment.
- Optional: set `CULTS_API_URL` (defaults to `https://cults3d.com/graphql`).

## Capture the Schema
```powershell
python scripts/fetch_schema.py
```
This writes `schema/schema.snapshot.json`. If you do not want to commit the snapshot, keep it in `.gitignore`.

## Run Contract Checks
```powershell
python scripts/contract_checks.py
```
The script validates the presence of key fields used in this docset. Update `stability_matrix.md` if a field is missing.

## Troubleshooting
- `HTTP Basic: Access denied` usually means the username or key is wrong.
- If introspection fails, retry with a fresh key and confirm Basic auth encoding.
