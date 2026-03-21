"""Payment tools."""

from float_mcp.utils.float_client import float_client


def _normalize_payment(raw: dict) -> dict:
    """Map Float API payment to clean schema."""
    return {
        "id": raw.get("id"),
        "amount": (raw.get("amount", {}).get("value", 0) or 0) / 100,
        "currency": raw.get("amount", {}).get("currency", "CAD"),
        "status": raw.get("status", "UNKNOWN"),
        "date": raw.get("created_at", ""),
        "description": raw.get("description", ""),
    }


async def get_payments(limit: int = 50) -> dict:
    """
    Retrieve payments with pagination.

    Args:
        limit: Maximum number of payments to return

    Returns:
        {"payments": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/payments", params={"page": page, "page_size": page_size}
        )

        if "error" in resp:
            break

        items = resp.get("items", [])
        if not items:
            break

        all_items.extend(items)
        if len(items) < page_size:
            break

        page += 1

    all_items = all_items[:limit]
    payments = [_normalize_payment(p) for p in all_items]

    return {"payments": payments}


async def get_payment_by_id(payment_id: str) -> dict:
    """
    Retrieve a single payment by ID.

    Args:
        payment_id: Payment ID

    Returns:
        {"payment": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/payments/{payment_id}")

    if "error" in resp:
        return resp

    return {"payment": _normalize_payment(resp)}
