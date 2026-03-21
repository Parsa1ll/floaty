"""Transaction tools: fetch, filter, and normalize Float card transactions."""

from typing import Optional

from float_mcp.utils.float_client import float_client


def _normalize_transaction(raw: dict) -> dict:
    """
    Normalize a raw Float transaction to a clean schema.
    Float stores amounts in smallest currency units (cents), with ISO 8601 dates.
    """
    total = raw.get("total", {})
    vendor = raw.get("vendor", {})

    return {
        "id": raw.get("id", ""),
        "merchant": vendor.get("name", raw.get("description", "")),
        "amount": total.get("value", 0) / 100,  # Convert cents to dollars
        "currency": total.get("currency", ""),
        "date": raw.get("created_at", ""),
        "type": raw.get("type", ""),  # CAPTURE, REFUND, etc.
        "spender": raw.get("spender", {}).get("email", ""),
        "team": raw.get("team", {}).get("name", ""),
    }


async def _fetch_transactions(limit: int = 1000) -> list[dict]:
    """
    Internal helper: fetch up to `limit` transactions with pagination.
    Returns a list of normalized transactions. On error, returns empty list.
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/card-transactions", params={"page": page, "page_size": page_size}
        )

        if "error" in resp:
            # Log error but return what we have so far
            break

        items = resp.get("items", [])
        all_items.extend(items)

        # If we got fewer items than requested, we've hit the last page
        if len(items) < page_size:
            break

        page += 1

    normalized = [_normalize_transaction(t) for t in all_items[:limit]]
    return normalized


async def get_transactions(limit: int = 50) -> dict:
    """
    Fetch recent transactions with pagination.

    Args:
        limit: Max number of transactions to return (default 50)

    Returns:
        {"transactions": [...]} or {"error": "..."}
    """
    transactions = await _fetch_transactions(limit)
    return {"transactions": transactions}


async def get_transaction_by_id(transaction_id: str) -> dict:
    """
    Fetch a single transaction by ID.

    Args:
        transaction_id: Float transaction ID

    Returns:
        {"transaction": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/card-transactions/{transaction_id}")

    if "error" in resp:
        return resp

    return {"transaction": _normalize_transaction(resp)}


async def filter_transactions_by_date(start_date: str, end_date: str) -> dict:
    """
    Filter transactions by date range (ISO 8601 format, e.g. "2024-01-01").

    Args:
        start_date: Start date (ISO 8601)
        end_date: End date (ISO 8601)

    Returns:
        {"transactions": [...]} or {"error": "..."}
    """
    all_transactions = await _fetch_transactions(limit=1000)
    filtered = [
        t
        for t in all_transactions
        if start_date <= t["date"][:10] <= end_date
    ]
    return {"transactions": filtered}


async def filter_transactions_by_amount(
    min_amount: float, max_amount: float
) -> dict:
    """
    Filter transactions by amount range.

    Args:
        min_amount: Minimum transaction amount
        max_amount: Maximum transaction amount

    Returns:
        {"transactions": [...]} or {"error": "..."}
    """
    all_transactions = await _fetch_transactions(limit=1000)
    filtered = [t for t in all_transactions if min_amount <= t["amount"] <= max_amount]
    return {"transactions": filtered}


async def update_transaction(transaction_id: str, data: dict) -> dict:
    """
    Update a single card transaction.

    Args:
        transaction_id: Transaction ID
        data: Fields to update

    Returns:
        {"transaction": {...}} or {"error": "..."}
    """
    resp = await float_client.patch(f"/card-transactions/{transaction_id}", data=data)

    if "error" in resp:
        return resp

    return {"transaction": _normalize_transaction(resp)}


async def update_transactions(updates: list) -> dict:
    """
    Update multiple card transactions in bulk.

    Args:
        updates: List of update objects with "id" and other fields to update

    Returns:
        {"transactions": [...]} or {"error": "..."}
    """
    resp = await float_client.patch("/card-transactions", data=updates)

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    transactions = [_normalize_transaction(t) for t in items if "id" in t]

    return {"transactions": transactions}
