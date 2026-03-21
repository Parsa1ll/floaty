"""User tools: list users and manage card assignments."""

from float_mcp.utils.float_client import float_client


def _normalize_user(raw: dict) -> dict:
    """Normalize a raw Float user object to a clean schema."""
    return {
        "id": raw.get("id", ""),
        "email": raw.get("email", ""),
        "name": raw.get("name", ""),
        "team": raw.get("team", {}).get("name", ""),
    }


async def list_users() -> dict:
    """
    List all users in the Float organization.

    Returns:
        {"users": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/users", params={"page": 1, "page_size": 1000})

    if "error" in resp:
        return resp

    # Handle both list and paginated response formats
    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    users = [_normalize_user(u) for u in items if "id" in u]

    return {"users": users}


async def get_user_by_id(user_id: str) -> dict:
    """
    Retrieve a single user by ID.

    Args:
        user_id: User ID

    Returns:
        {"user": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/users/{user_id}")

    if "error" in resp:
        return resp

    return {"user": _normalize_user(resp)}


async def assign_card_to_user(card_id: str, user_id: str) -> dict:
    """
    Assign a card to a user.

    # TODO: endpoint not found in Float docs
    Attempting PATCH /cards/{card_id} with {"user_id": user_id}

    Args:
        card_id: Float card ID
        user_id: Float user ID to assign the card to

    Returns:
        {"card": {...}} or {"error": "..."}
    """
    resp = await float_client.patch(f"/cards/{card_id}", data={"user_id": user_id})

    if "error" in resp:
        return resp

    # Return the updated card
    from float_mcp.tools.cards import _normalize_card

    return {"card": _normalize_card(resp)}
