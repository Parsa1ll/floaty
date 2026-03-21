"""Reimbursement tools."""

from float_mcp.utils.float_client import float_client


def _normalize_reimbursement(raw: dict) -> dict:
    """Map Float API reimbursement to clean schema."""
    return {
        "id": raw.get("id"),
        "amount": (raw.get("amount", {}).get("value", 0) or 0) / 100,
        "currency": raw.get("amount", {}).get("currency", "CAD"),
        "status": raw.get("status", "UNKNOWN"),
        "submitter_email": raw.get("submitter", {}).get("email") if isinstance(raw.get("submitter"), dict) else raw.get("submitter"),
        "date": raw.get("created_at", ""),
        "memo": raw.get("memo", ""),
        "synced": raw.get("synced", False),
    }


async def get_reimbursements(limit: int = 50) -> dict:
    """
    Retrieve reimbursement reports with pagination.

    Args:
        limit: Maximum number of reimbursements to return

    Returns:
        {"reimbursements": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/reimbursements", params={"page": page, "page_size": page_size}
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
    reimbursements = [_normalize_reimbursement(r) for r in all_items]

    return {"reimbursements": reimbursements}


async def get_reimbursement_by_id(reimbursement_id: str) -> dict:
    """
    Retrieve a single reimbursement report by ID.

    Args:
        reimbursement_id: Reimbursement ID

    Returns:
        {"reimbursement": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/reimbursements/{reimbursement_id}")

    if "error" in resp:
        return resp

    return {"reimbursement": _normalize_reimbursement(resp)}


async def update_reimbursement(reimbursement_id: str, data: dict) -> dict:
    """
    Update a single reimbursement.

    Args:
        reimbursement_id: Reimbursement ID
        data: Fields to update

    Returns:
        {"reimbursement": {...}} or {"error": "..."}
    """
    resp = await float_client.patch(f"/reimbursements/{reimbursement_id}", data=data)

    if "error" in resp:
        return resp

    return {"reimbursement": _normalize_reimbursement(resp)}


async def update_reimbursements(updates: list) -> dict:
    """
    Update multiple reimbursements in bulk.

    Args:
        updates: List of update objects with "id" and other fields

    Returns:
        {"reimbursements": [...]} or {"error": "..."}
    """
    resp = await float_client.patch("/reimbursements", data=updates)

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    reimbursements = [_normalize_reimbursement(r) for r in items if "id" in r]

    return {"reimbursements": reimbursements}


async def mark_reimbursement_synced(reimbursement_id: str) -> dict:
    """
    Mark a reimbursement as synced.

    Args:
        reimbursement_id: Reimbursement ID

    Returns:
        {"reimbursement": {...}} or {"error": "..."}
    """
    resp = await float_client.post(f"/reimbursements/{reimbursement_id}/mark-as-synced")

    if "error" in resp:
        return resp

    return {"reimbursement": _normalize_reimbursement(resp)}
