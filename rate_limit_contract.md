# Rate Limit Contract

This file documents the community-known rate limits and the recommended backoff strategy. Always follow `x-ratelimit-*` headers when present.

## Known Limits (Community Reports)
- Roughly 60 requests per 30 seconds.
- Roughly 500 requests per day.
Source: Discord `#api-help` (Mar/2025, Oct/2025).

## Headers to Log
- `x-ratelimit-limit`
- `x-ratelimit-remaining`
- `x-ratelimit-reset`
- `cf-ray`

## Backoff Policy
Use exponential backoff after 429 or 5xx responses:
1. Wait 1 second.
2. Retry once.
3. If still failing, wait 5 seconds.
4. Retry again.
5. Escalate to 10 seconds, then 30 seconds for persistent failures.

## Download URLs
When processing `ordersBatch` download URLs, pause between requests. Sunny asked for "plenty of waiting time between requests" when automating downloads.
Source: Discord msg 1372299248560767106.

## Example Throttle Logic (Pseudo)
```text
for each request:
  response = send()
  if response.status == 429 or response.status >= 500:
    sleep(backoff_seconds)
    backoff_seconds = min(backoff_seconds * 5, 30)
    retry
  else:
    backoff_seconds = 1
```
