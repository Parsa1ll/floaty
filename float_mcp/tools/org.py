"""Organization tools: teams, subsidiaries, receipts, policies."""

from float_mcp.utils.float_client import float_client


# ============================================================================
# TEAMS
# ============================================================================


def _normalize_team(raw: dict) -> dict:
    """Map Float API team to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "description": raw.get("description", ""),
    }


async def get_teams(limit: int = 50) -> dict:
    """
    Retrieve teams with pagination.

    Args:
        limit: Maximum number of teams to return

    Returns:
        {"teams": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/teams", params={"page": page, "page_size": page_size}
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
    teams = [_normalize_team(t) for t in all_items]

    return {"teams": teams}


async def get_team_by_id(team_id: str) -> dict:
    """
    Retrieve a single team by ID.

    Args:
        team_id: Team ID

    Returns:
        {"team": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/teams/{team_id}")

    if "error" in resp:
        return resp

    return {"team": _normalize_team(resp)}


# ============================================================================
# SUBSIDIARIES
# ============================================================================


def _normalize_subsidiary(raw: dict) -> dict:
    """Map Float API subsidiary to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "country": raw.get("country", ""),
        "currency": raw.get("currency", "CAD"),
    }


async def get_subsidiaries() -> dict:
    """
    Retrieve all subsidiaries.

    Returns:
        {"subsidiaries": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/subsidiaries")

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    subsidiaries = [_normalize_subsidiary(s) for s in items if "id" in s]

    return {"subsidiaries": subsidiaries}


async def get_subsidiary_by_id(subsidiary_id: str) -> dict:
    """
    Retrieve a single subsidiary by ID.

    Args:
        subsidiary_id: Subsidiary ID

    Returns:
        {"subsidiary": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/subsidiaries/{subsidiary_id}")

    if "error" in resp:
        return resp

    return {"subsidiary": _normalize_subsidiary(resp)}


# ============================================================================
# RECEIPTS
# ============================================================================


def _normalize_receipt(raw: dict) -> dict:
    """Map Float API receipt to clean schema."""
    return {
        "id": raw.get("id"),
        "filename": raw.get("filename", ""),
        "url": raw.get("url", ""),
        "created_at": raw.get("created_at", ""),
        "file_size": raw.get("file_size", 0),
    }


async def get_receipts(limit: int = 50) -> dict:
    """
    Retrieve receipts with pagination.

    Args:
        limit: Maximum number of receipts to return

    Returns:
        {"receipts": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/receipts", params={"page": page, "page_size": page_size}
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
    receipts = [_normalize_receipt(r) for r in all_items]

    return {"receipts": receipts}


async def get_receipt_by_id(receipt_id: str) -> dict:
    """
    Retrieve a single receipt by ID.

    Args:
        receipt_id: Receipt ID

    Returns:
        {"receipt": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/receipts/{receipt_id}")

    if "error" in resp:
        return resp

    return {"receipt": _normalize_receipt(resp)}


# ============================================================================
# APPROVAL POLICIES
# ============================================================================


def _normalize_approval_policy(raw: dict) -> dict:
    """Map Float API approval policy to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "description": raw.get("description", ""),
        "is_active": raw.get("is_active", True),
    }


async def get_approval_policies(limit: int = 50) -> dict:
    """
    Retrieve approval policies with pagination.

    Args:
        limit: Maximum number of policies to return

    Returns:
        {"approval_policies": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/approval-policies", params={"page": page, "page_size": page_size}
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
    policies = [_normalize_approval_policy(p) for p in all_items]

    return {"approval_policies": policies}


async def get_approval_policy_by_id(policy_id: str) -> dict:
    """
    Retrieve a single approval policy by ID.

    Args:
        policy_id: Policy ID

    Returns:
        {"approval_policy": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/approval-policies/{policy_id}")

    if "error" in resp:
        return resp

    return {"approval_policy": _normalize_approval_policy(resp)}


# ============================================================================
# SUBMISSION POLICIES
# ============================================================================


def _normalize_submission_policy(raw: dict) -> dict:
    """Map Float API submission policy to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "description": raw.get("description", ""),
        "is_active": raw.get("is_active", True),
    }


async def get_submission_policies(limit: int = 50) -> dict:
    """
    Retrieve submission policies with pagination.

    Args:
        limit: Maximum number of policies to return

    Returns:
        {"submission_policies": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/submission-policies", params={"page": page, "page_size": page_size}
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
    policies = [_normalize_submission_policy(p) for p in all_items]

    return {"submission_policies": policies}


async def get_submission_policy_by_id(policy_id: str) -> dict:
    """
    Retrieve a single submission policy by ID.

    Args:
        policy_id: Policy ID

    Returns:
        {"submission_policy": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/submission-policies/{policy_id}")

    if "error" in resp:
        return resp

    return {"submission_policy": _normalize_submission_policy(resp)}
