"""Vendor management tools."""

from float_mcp.utils.float_client import float_client


def _normalize_vendor(raw: dict) -> dict:
    """Map Float API vendor to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "email": raw.get("email", ""),
        "address": raw.get("address", ""),
        "tax_code_id": raw.get("tax_code_id"),
    }


async def get_vendors() -> dict:
    """
    Retrieve all vendors.

    Returns:
        {"vendors": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/vendors")

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    vendors = [_normalize_vendor(v) for v in items if "id" in v]

    return {"vendors": vendors}


async def get_vendor_by_id(vendor_id: str) -> dict:
    """
    Retrieve a single vendor by ID.

    Args:
        vendor_id: Vendor ID

    Returns:
        {"vendor": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/vendors/{vendor_id}")

    if "error" in resp:
        return resp

    return {"vendor": _normalize_vendor(resp)}


async def create_vendor(name: str, email: str = "", address: str = "", tax_code_id: str = "") -> dict:
    """
    Create a new vendor.

    Args:
        name: Vendor name
        email: Vendor email
        address: Vendor address
        tax_code_id: Tax code ID

    Returns:
        {"vendor": {...}} or {"error": "..."}
    """
    data = {"name": name}
    if email:
        data["email"] = email
    if address:
        data["address"] = address
    if tax_code_id:
        data["tax_code_id"] = tax_code_id

    resp = await float_client.post("/vendors", data=data)

    if "error" in resp:
        return resp

    return {"vendor": _normalize_vendor(resp)}


async def update_vendor(vendor_id: str, data: dict) -> dict:
    """
    Update a vendor.

    Args:
        vendor_id: Vendor ID
        data: Fields to update (e.g., {"name": "...", "email": "..."})

    Returns:
        {"vendor": {...}} or {"error": "..."}
    """
    resp = await float_client.patch(f"/vendors/{vendor_id}", data=data)

    if "error" in resp:
        return resp

    return {"vendor": _normalize_vendor(resp)}
