"""Account and account transaction tools."""

from float_mcp.utils.float_client import float_client


def _normalize_account(raw: dict) -> dict:
    """Map Float API account response to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name"),
        "current_balance": (raw.get("current_balance", {}).get("value", 0) or 0) / 100,
        "currency": raw.get("current_balance", {}).get("currency", "CAD"),
        "status": raw.get("status", "UNKNOWN"),
    }


def _normalize_account_transaction(raw: dict) -> dict:
    """Map Float API account transaction to clean schema."""
    return {
        "id": raw.get("id"),
        "description": raw.get("description"),
        "amount": (raw.get("amount", {}).get("value", 0) or 0) / 100,
        "currency": raw.get("amount", {}).get("currency", "CAD"),
        "date": raw.get("created_at", ""),
        "type": raw.get("type", "UNKNOWN"),
    }


async def get_accounts() -> dict:
    """
    Retrieve all accounts with pagination.

    Returns:
        {"accounts": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/accounts", params={"page": 1, "page_size": 1000})

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    accounts = [_normalize_account(a) for a in items if "id" in a]

    return {"accounts": accounts}


async def get_account_by_id(account_id: str) -> dict:
    """
    Retrieve a single account by ID.

    Args:
        account_id: Account ID

    Returns:
        {"account": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/accounts/{account_id}")

    if "error" in resp:
        return resp

    return {"account": _normalize_account(resp)}


async def get_account_transactions(limit: int = 50) -> dict:
    """
    Retrieve account transactions with pagination.

    Args:
        limit: Maximum number of transactions to return

    Returns:
        {"transactions": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/account-transactions", params={"page": page, "page_size": page_size}
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
    transactions = [_normalize_account_transaction(t) for t in all_items]

    return {"transactions": transactions}


async def get_account_transaction_by_id(transaction_id: str) -> dict:
    """
    Retrieve a single account transaction by ID.

    Args:
        transaction_id: Transaction ID

    Returns:
        {"transaction": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/account-transactions/{transaction_id}")

    if "error" in resp:
        return resp

    return {"transaction": _normalize_account_transaction(resp)}
