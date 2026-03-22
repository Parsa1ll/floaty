"""Bill and bill attachment tools."""

from float_mcp.utils.float_client import float_client


def _normalize_bill(raw: dict) -> dict:
    """Map Float API bill response to clean schema."""
    out = {
        "id": raw.get("id"),
        "amount": (raw.get("amount", {}).get("value", 0) or 0) / 100,
        "currency": raw.get("amount", {}).get("currency", "CAD"),
        "status": raw.get("status", "UNKNOWN"),
        "vendor_name": raw.get("vendor", {}).get("name") if isinstance(raw.get("vendor"), dict) else raw.get("vendor"),
        "date": raw.get("date", ""),
        "memo": raw.get("memo", ""),
        "synced": raw.get("synced", False),
    }
    if raw.get("due_date"):
        out["due_date"] = raw["due_date"]
    return out


def _normalize_bill_attachment(raw: dict) -> dict:
    """Map Float API bill attachment to clean schema."""
    return {
        "id": raw.get("id"),
        "bill_id": raw.get("bill_id"),
        "filename": raw.get("filename", ""),
        "url": raw.get("url", ""),
        "created_at": raw.get("created_at", ""),
    }


async def get_bills(limit: int = 50) -> dict:
    """
    Retrieve bills with pagination.

    Args:
        limit: Maximum number of bills to return

    Returns:
        {"bills": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/bills", params={"page": page, "page_size": page_size}
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
    bills = [_normalize_bill(b) for b in all_items]

    return {"bills": bills}


async def get_bill_by_id(bill_id: str) -> dict:
    """
    Retrieve a single bill by ID.

    Args:
        bill_id: Bill ID

    Returns:
        {"bill": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/bills/{bill_id}")

    if "error" in resp:
        return resp

    return {"bill": _normalize_bill(resp)}


async def update_bill(bill_id: str, data: dict) -> dict:
    """
    Update a single bill.

    Args:
        bill_id: Bill ID
        data: Fields to update (e.g., {"status": "APPROVED", "memo": "..."})

    Returns:
        {"bill": {...}} or {"error": "..."}
    """
    resp = await float_client.patch(f"/bills/{bill_id}", data=data)

    if "error" in resp:
        return resp

    return {"bill": _normalize_bill(resp)}


async def update_bills(updates: list) -> dict:
    """
    Update multiple bills in bulk.

    Args:
        updates: List of update objects with "id" and other fields to update

    Returns:
        {"bills": [...]} or {"error": "..."}
    """
    resp = await float_client.patch("/bills", data=updates)

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    bills = [_normalize_bill(b) for b in items if "id" in b]

    return {"bills": bills}


async def mark_bill_synced(bill_id: str) -> dict:
    """
    Mark a bill as synced.

    Args:
        bill_id: Bill ID

    Returns:
        {"bill": {...}} or {"error": "..."}
    """
    resp = await float_client.post(f"/bills/{bill_id}/mark-as-synced")

    if "error" in resp:
        return resp

    return {"bill": _normalize_bill(resp)}


async def get_bill_attachments(bill_id: str, limit: int = 50) -> dict:
    """
    Retrieve attachments for a specific bill.

    Args:
        bill_id: Bill ID
        limit: Maximum attachments to return

    Returns:
        {"attachments": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            f"/bills/{bill_id}/attachments",
            params={"page": page, "page_size": page_size}
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
    attachments = [_normalize_bill_attachment(a) for a in all_items]

    return {"attachments": attachments}


async def get_bill_attachment_by_id(attachment_id: str) -> dict:
    """
    Retrieve a single bill attachment by ID.

    Args:
        attachment_id: Attachment ID

    Returns:
        {"attachment": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/bill-attachments/{attachment_id}")

    if "error" in resp:
        return resp

    return {"attachment": _normalize_bill_attachment(resp)}
