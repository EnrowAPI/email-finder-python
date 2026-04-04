"""Find professional email addresses from a name and company. Powered by Enrow."""

from typing import Any, Dict, List, Optional

import httpx

__all__ = ["find_email", "get_email_result", "find_emails", "get_email_results"]

BASE_URL = "https://api.enrow.io"


def _request(api_key: str, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    url = f"{BASE_URL}{path}"

    with httpx.Client() as client:
        response = client.request(method, url, headers=headers, json=body)

    data = response.json()
    if not response.is_success:
        raise Exception(data.get("message", f"API error {response.status_code}"))
    return data


def find_email(
    api_key: str,
    full_name: str,
    company_domain: Optional[str] = None,
    company_name: Optional[str] = None,
    custom: Optional[Dict[str, Any]] = None,
    country_code: Optional[str] = None,
    retrieve_gender: Optional[bool] = None,
    webhook: Optional[str] = None,
) -> Dict[str, Any]:
    """Start a single email search. Returns a dict with an 'id' to poll for results."""
    body: Dict[str, Any] = {"fullname": full_name}
    if company_domain:
        body["company_domain"] = company_domain
    if company_name:
        body["company_name"] = company_name
    if custom is not None:
        body["custom"] = custom
    if country_code or webhook or retrieve_gender is not None:
        settings: Dict[str, Any] = {}
        if country_code:
            settings["country_code"] = country_code
        if retrieve_gender is not None:
            settings["retrieve_gender"] = retrieve_gender
        if webhook:
            settings["webhook"] = webhook
        body["settings"] = settings
    return _request(api_key, "POST", "/email/find/single", body)


def get_email_result(api_key: str, id: str) -> Dict[str, Any]:
    """Retrieve the result of a single email search by its ID."""
    return _request(api_key, "GET", f"/email/find/single?id={id}")


def find_emails(
    api_key: str,
    searches: List[Dict[str, Any]],
    country_code: Optional[str] = None,
    retrieve_gender: Optional[bool] = None,
    webhook: Optional[str] = None,
) -> Dict[str, Any]:
    """Start a bulk email search. Returns a dict with a 'batchId' to poll for results."""
    body: Dict[str, Any] = {
        "searches": [
            {
                "fullname": s["full_name"],
                **( {"company_domain": s["company_domain"]} if s.get("company_domain") else {}),
                **( {"company_name": s["company_name"]} if s.get("company_name") else {}),
                **( {"custom": s["custom"]} if s.get("custom") else {}),
            }
            for s in searches
        ],
    }
    if country_code or webhook or retrieve_gender is not None:
        settings: Dict[str, Any] = {}
        if country_code:
            settings["country_code"] = country_code
        if retrieve_gender is not None:
            settings["retrieve_gender"] = retrieve_gender
        if webhook:
            settings["webhook"] = webhook
        body["settings"] = settings
    return _request(api_key, "POST", "/email/find/bulk", body)


def get_email_results(api_key: str, id: str) -> Dict[str, Any]:
    """Retrieve the results of a bulk email search by its batch ID."""
    return _request(api_key, "GET", f"/email/find/bulk?id={id}")
