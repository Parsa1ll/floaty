"""Accounting tools: GL codes, tax codes, custom fields."""

from float_mcp.utils.float_client import float_client


# ============================================================================
# GL CODES
# ============================================================================


def _normalize_gl_code(raw: dict) -> dict:
    """Map Float API GL code to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "code": raw.get("code", ""),
        "account_type": raw.get("account_type"),
    }


async def get_gl_codes(limit: int = 50) -> dict:
    """
    Retrieve GL codes with pagination.

    Args:
        limit: Maximum number of GL codes to return

    Returns:
        {"gl_codes": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/gl-codes", params={"page": page, "page_size": page_size}
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
    gl_codes = [_normalize_gl_code(g) for g in all_items]

    return {"gl_codes": gl_codes}


async def get_gl_code_by_id(gl_code_id: str) -> dict:
    """
    Retrieve a single GL code by ID.

    Args:
        gl_code_id: GL code ID

    Returns:
        {"gl_code": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/gl-codes/{gl_code_id}")

    if "error" in resp:
        return resp

    return {"gl_code": _normalize_gl_code(resp)}


async def create_gl_code(name: str, code: str, account_type: str = "") -> dict:
    """
    Create a new GL code.

    Args:
        name: GL code name
        code: GL code value
        account_type: Account type

    Returns:
        {"gl_code": {...}} or {"error": "..."}
    """
    data = {"name": name, "code": code}
    if account_type:
        data["account_type"] = account_type

    resp = await float_client.post("/gl-codes", data=data)

    if "error" in resp:
        return resp

    return {"gl_code": _normalize_gl_code(resp)}


# ============================================================================
# TAX CODES
# ============================================================================


def _normalize_tax_code(raw: dict) -> dict:
    """Map Float API tax code to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "rate": raw.get("rate", 0.0),
    }


async def get_tax_codes() -> dict:
    """
    Retrieve all tax codes.

    Returns:
        {"tax_codes": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/tax-codes")

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    tax_codes = [_normalize_tax_code(t) for t in items if "id" in t]

    return {"tax_codes": tax_codes}


async def get_tax_code_by_id(tax_code_id: str) -> dict:
    """
    Retrieve a single tax code by ID.

    Args:
        tax_code_id: Tax code ID

    Returns:
        {"tax_code": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/tax-codes/{tax_code_id}")

    if "error" in resp:
        return resp

    return {"tax_code": _normalize_tax_code(resp)}


async def create_tax_code(name: str, rate: float) -> dict:
    """
    Create a new tax code.

    Args:
        name: Tax code name
        rate: Tax rate (e.g., 0.05 for 5%)

    Returns:
        {"tax_code": {...}} or {"error": "..."}
    """
    resp = await float_client.post("/tax-codes", data={"name": name, "rate": rate})

    if "error" in resp:
        return resp

    return {"tax_code": _normalize_tax_code(resp)}


async def delete_tax_code(tax_code_id: str) -> dict:
    """
    Delete a tax code.

    Args:
        tax_code_id: Tax code ID

    Returns:
        {"success": True} or {"error": "..."}
    """
    # DELETE doesn't exist as a public method, use PATCH with delete flag or POST to delete endpoint
    # Using a placeholder endpoint pattern
    resp = await float_client.post(f"/tax-codes/{tax_code_id}/delete")

    if "error" in resp:
        return resp

    return {"success": True}


# ============================================================================
# TAX COMPONENTS
# ============================================================================


def _normalize_tax_component(raw: dict) -> dict:
    """Map Float API tax component to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "rate": raw.get("rate", 0.0),
    }


async def get_tax_components() -> dict:
    """
    Retrieve all tax components.

    Returns:
        {"tax_components": [...]} or {"error": "..."}
    """
    resp = await float_client.get("/tax-components")

    if "error" in resp:
        return resp

    items = resp.get("items", resp) if isinstance(resp.get("items"), list) else [resp]
    tax_components = [_normalize_tax_component(t) for t in items if "id" in t]

    return {"tax_components": tax_components}


# ============================================================================
# CUSTOM FIELDS
# ============================================================================


def _normalize_custom_field(raw: dict) -> dict:
    """Map Float API custom field to clean schema."""
    return {
        "id": raw.get("id"),
        "name": raw.get("name", ""),
        "field_type": raw.get("field_type", raw.get("type")),
        "options": raw.get("options", []),
    }


async def get_custom_fields(limit: int = 50) -> dict:
    """
    Retrieve custom fields with pagination.

    Args:
        limit: Maximum number of fields to return

    Returns:
        {"custom_fields": [...]} or {"error": "..."}
    """
    all_items = []
    page = 1
    page_size = min(limit, 1000)

    while len(all_items) < limit:
        resp = await float_client.get(
            "/custom-fields", params={"page": page, "page_size": page_size}
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
    custom_fields = [_normalize_custom_field(c) for c in all_items]

    return {"custom_fields": custom_fields}


async def get_custom_field_by_id(field_id: str) -> dict:
    """
    Retrieve a single custom field by ID.

    Args:
        field_id: Custom field ID

    Returns:
        {"custom_field": {...}} or {"error": "..."}
    """
    resp = await float_client.get(f"/custom-fields/{field_id}")

    if "error" in resp:
        return resp

    return {"custom_field": _normalize_custom_field(resp)}


async def create_custom_field(name: str, field_type: str) -> dict:
    """
    Create a new custom field.

    Args:
        name: Field name
        field_type: Field type (e.g., "text", "number", "select")

    Returns:
        {"custom_field": {...}} or {"error": "..."}
    """
    resp = await float_client.post(
        "/custom-fields", data={"name": name, "field_type": field_type}
    )

    if "error" in resp:
        return resp

    return {"custom_field": _normalize_custom_field(resp)}


async def delete_custom_field(field_id: str) -> dict:
    """
    Delete a custom field.

    Args:
        field_id: Custom field ID

    Returns:
        {"success": True} or {"error": "..."}
    """
    resp = await float_client.post(f"/custom-fields/{field_id}/delete")

    if "error" in resp:
        return resp

    return {"success": True}


async def create_custom_field_option(field_id: str, value: str) -> dict:
    """
    Create a custom field option.

    Args:
        field_id: Custom field ID
        value: Option value

    Returns:
        {"option": {...}} or {"error": "..."}
    """
    resp = await float_client.post(
        f"/custom-fields/{field_id}/options", data={"value": value}
    )

    if "error" in resp:
        return resp

    return {"option": resp}


async def delete_custom_field_option(field_id: str, option_id: str) -> dict:
    """
    Delete a custom field option.

    Args:
        field_id: Custom field ID
        option_id: Option ID

    Returns:
        {"success": True} or {"error": "..."}
    """
    resp = await float_client.post(
        f"/custom-fields/{field_id}/options/{option_id}/delete"
    )

    if "error" in resp:
        return resp

    return {"success": True}
