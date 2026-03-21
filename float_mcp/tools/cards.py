"""Card tools: create, list, freeze, and manage Float cards."""

from float_mcp.utils.float_client import float_client


def _normalize_card(raw: dict) -> dict:
    """Normalize a raw Float card object to a clean schema."""
    return {
        "id": raw.get("id", ""),
        "name": raw.get("name", raw.get("display_name", "")),
        "limit": raw.get("limit", 0),
        "status": raw.get("status", "UNKNOWN"),
    }


async def get_cards() -> dict:
    """
    List all Float cards.

    Returns:
        {"cards": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/cards", params={"page": 1, "page_size": 1000})

    if "error" in resp:
        return resp

    # Handle both list and paginated response formats
    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    cards = [_normalize_card(c) for c in items if "id" in c]

    return {"cards": cards}


async def get_card_by_id(card_id: str) -> dict:
    """
    Retrieve a single card by ID.

    Args:
        card_id: Card ID

    Returns:
        {"card": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/cards/{card_id}")

    if "error" in resp:
        return resp

    return {"card": _normalize_card(resp)}


async def create_card(name: str, limit: int) -> dict:
    """
    Create a new Float card with a spending limit.

    Float separates card creation from limit setting:
    1. POST /cards to create the card
    2. POST /card-limits to set the spending limit

    Args:
        name: Card display name
        limit: Spending limit in dollars

    Returns:
        {"card": {...}} or {"error": "..."}
    """
    # Step 1: Create the card
    create_resp = await float_client.post("/cards", data={"name": name})

    if "error" in create_resp:
        return create_resp

    card_id = create_resp.get("id", "")
    if not card_id:
        return {"error": "Card created but no ID returned"}

    # Step 2: Set the spending limit
    limit_resp = await float_client.post(
        "/card-limits",
        data={
            "card_id": card_id,
            "amount": {"value": int(limit * 100), "currency": "CAD"},
        },
    )

    if "error" in limit_resp:
        return {
            "error": f"Card created (ID: {card_id}) but limit setting failed: {limit_resp['error']}"
        }

    # Return the created card with limit
    card = _normalize_card(create_resp)
    card["limit"] = limit
    return {"card": card}


async def freeze_card(card_id: str) -> dict:
    """
    Freeze a card to prevent further transactions.

    # TODO: endpoint not confirmed in Float docs
    Attempting PATCH /cards/{card_id} with {"status": "FROZEN"}

    Args:
        card_id: Float card ID

    Returns:
        {"card": {...}} or {"error": "..."}
    """
    resp = await float_client.patch(f"/cards/{card_id}", data={"status": "FROZEN"})

    if "error" in resp:
        return resp

    return {"card": _normalize_card(resp)}


async def update_card_limit(card_id: str, new_limit: int) -> dict:
    """
    Update the spending limit for a card.

    # TODO: verify PATCH /card-limits/{id}
    Card limits API is BETA in Float. Currently using POST /card-limits.

    Args:
        card_id: Float card ID
        new_limit: New spending limit in dollars

    Returns:
        {"card": {...}} or {"error": "..."}
    """
    resp = await float_client.post(
        "/card-limits",
        data={
            "card_id": card_id,
            "amount": {"value": int(new_limit * 100), "currency": "CAD"},
        },
    )

    if "error" in resp:
        return resp

    # Fetch the updated card to return normalized data
    card_resp = await float_client.get(f"/cards/{card_id}")

    if "error" in card_resp:
        return {
            "error": f"Limit updated but card fetch failed: {card_resp['error']}"
        }

    return {"card": _normalize_card(card_resp)}
