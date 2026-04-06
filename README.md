# Email Finder - Python Library

[![PyPI version](https://img.shields.io/pypi/v/email-finder.svg)](https://pypi.org/project/email-finder/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/EnrowAPI/email-finder-python)](https://github.com/EnrowAPI/email-finder-python)
[![Last commit](https://img.shields.io/github/last-commit/EnrowAPI/email-finder-python)](https://github.com/EnrowAPI/email-finder-python/commits)

Find verified professional email addresses from a name and company. Integrate email discovery into your sales pipeline, CRM sync, or lead generation workflow.

Powered by [Enrow](https://enrow.io) — works on catch-all domains, only charged when an email is found.

## Installation

```bash
pip install email-finder
```

Requires Python 3.8+. Only dependency: `httpx`.

## Simple Usage

```python
from enrow_email_finder import find_email, get_email_result

search = find_email(
    api_key="your_api_key",
    full_name="Tim Cook",
    company_domain="apple.com",
)

result = get_email_result("your_api_key", search["id"])

print(result["email"])          # tcook@apple.com
print(result["qualification"])  # valid
```

`find_email` returns a search ID. The search runs asynchronously — call `get_email_result` to retrieve the result once it's ready. You can also pass a `webhook` URL to get notified automatically.

## Search by company name

If you don't have the domain, you can search by company name instead. The `country_code` parameter helps narrow down results when company names are ambiguous.

```python
search = find_email(
    api_key="your_api_key",
    full_name="Tim Cook",
    company_name="Apple Inc.",
    country_code="US",
)
```

## Bulk search

```python
from enrow_email_finder import find_emails, get_email_results

batch = find_emails(
    api_key="your_api_key",
    searches=[
        {"full_name": "Tim Cook", "company_domain": "apple.com"},
        {"full_name": "Satya Nadella", "company_domain": "microsoft.com"},
        {"full_name": "Jensen Huang", "company_name": "NVIDIA"},
    ],
)

# batch["batchId"], batch["total"], batch["status"]

results = get_email_results("your_api_key", batch["batchId"])
# results["results"] — list of email result dicts
```

Up to 5,000 searches per batch. Pass a `webhook` URL to get notified when the batch completes.

## Error handling

```python
try:
    find_email(api_key="bad_key", full_name="Test", company_domain="test.com")
except Exception as e:
    # str(e) contains the API error description
    # Common errors:
    # - "Invalid or missing API key" (401)
    # - "Your credit balance is insufficient." (402)
    # - "Rate limit exceeded" (429)
    print(e)
```

## Getting an API key

Register at [app.enrow.io](https://app.enrow.io) to get your API key. You get **50 free credits** (= 50 emails) with no credit card required.

Paid plans start at **$17/mo** for 1,000 emails up to **$497/mo** for 100,000 emails. See [pricing](https://enrow.io/pricing).

## Documentation

- [Enrow API documentation](https://docs.enrow.io)
- [Full Enrow SDK](https://github.com/EnrowAPI/enrow-python) — includes email verifier, phone finder, reverse email lookup, and more

## License

MIT — see [LICENSE](LICENSE) for details.
