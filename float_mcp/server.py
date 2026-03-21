"""MCP server for Float Finance Copilot.

Registers all tools via FastMCP decorators and exposes them to Claude or other MCP clients.
"""

import asyncio
import logging

from mcp.server.fastmcp import FastMCP

# Import all tool functions
from float_mcp.tools.accounts import (
    get_account_by_id,
    get_account_transactions,
    get_account_transaction_by_id,
    get_accounts,
)
from float_mcp.tools.accounting import (
    create_custom_field,
    create_custom_field_option,
    create_gl_code,
    create_tax_code,
    delete_custom_field,
    delete_custom_field_option,
    delete_tax_code,
    get_custom_field_by_id,
    get_custom_fields,
    get_gl_code_by_id,
    get_gl_codes,
    get_tax_code_by_id,
    get_tax_codes,
    get_tax_components,
)
from float_mcp.tools.bills import (
    get_bill_attachments,
    get_bill_attachment_by_id,
    get_bill_by_id,
    get_bills,
    mark_bill_synced,
    update_bill,
    update_bills,
)
from float_mcp.tools.cards import (
    create_card,
    freeze_card,
    get_card_by_id,
    get_cards,
    update_card_limit,
)
from float_mcp.tools.controls import (
    detect_suspicious_transactions,
    explain_spend_anomalies,
    find_duplicate_transactions,
    flag_high_spend,
)
from float_mcp.tools.org import (
    get_approval_policies,
    get_approval_policy_by_id,
    get_receipt_by_id,
    get_receipts,
    get_submission_policies,
    get_submission_policy_by_id,
    get_subsidiaries,
    get_subsidiary_by_id,
    get_team_by_id,
    get_teams,
)
from float_mcp.tools.payments import get_payment_by_id, get_payments
from float_mcp.tools.reimbursements import (
    get_reimbursement_by_id,
    get_reimbursements,
    mark_reimbursement_synced,
    update_reimbursement,
    update_reimbursements,
)
from float_mcp.tools.reports import (
    generate_finance_insights,
    monthly_spend_report,
    summarize_spend,
    top_merchants,
)
from float_mcp.tools.transactions import (
    filter_transactions_by_amount,
    filter_transactions_by_date,
    get_transaction_by_id,
    get_transactions,
    update_transaction,
    update_transactions,
)
from float_mcp.tools.users import (
    assign_card_to_user,
    get_user_by_id,
    list_users,
)
from float_mcp.tools.vendors import (
    create_vendor,
    get_vendor_by_id,
    get_vendors,
    update_vendor,
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("float_mcp.server")

# Create MCP server
mcp = FastMCP("float-copilot")


# ============================================================================
# CARD TOOLS
# ============================================================================


@mcp.tool()
async def create_card_tool(name: str, limit: int) -> dict:
    """Create a new Float card with a spending limit."""
    return await create_card(name, limit)


@mcp.tool()
async def get_cards_tool() -> dict:
    """List all Float cards."""
    return await get_cards()


@mcp.tool()
async def get_card_by_id_tool(card_id: str) -> dict:
    """Retrieve a single card by ID."""
    return await get_card_by_id(card_id)


@mcp.tool()
async def freeze_card_tool(card_id: str) -> dict:
    """Freeze a card to prevent further transactions."""
    return await freeze_card(card_id)


@mcp.tool()
async def update_card_limit_tool(card_id: str, new_limit: int) -> dict:
    """Update the spending limit for a card."""
    return await update_card_limit(card_id, new_limit)


# ============================================================================
# TRANSACTION TOOLS
# ============================================================================


@mcp.tool()
async def get_transactions_tool(limit: int = 50) -> dict:
    """Fetch recent transactions with pagination."""
    return await get_transactions(limit)


@mcp.tool()
async def get_transaction_by_id_tool(transaction_id: str) -> dict:
    """Fetch a single transaction by ID."""
    return await get_transaction_by_id(transaction_id)


@mcp.tool()
async def filter_transactions_by_date_tool(start_date: str, end_date: str) -> dict:
    """Filter transactions by date range (ISO 8601 format)."""
    return await filter_transactions_by_date(start_date, end_date)


@mcp.tool()
async def filter_transactions_by_amount_tool(
    min_amount: float, max_amount: float
) -> dict:
    """Filter transactions by amount range."""
    return await filter_transactions_by_amount(min_amount, max_amount)


@mcp.tool()
async def update_transaction_tool(transaction_id: str, data: dict) -> dict:
    """Update a single card transaction."""
    return await update_transaction(transaction_id, data)


@mcp.tool()
async def update_transactions_tool(updates: list) -> dict:
    """Update multiple card transactions in bulk."""
    return await update_transactions(updates)


# ============================================================================
# REPORT TOOLS
# ============================================================================


@mcp.tool()
async def summarize_spend_tool() -> dict:
    """Get total spend and breakdown by transaction type."""
    return await summarize_spend()


@mcp.tool()
async def top_merchants_tool() -> dict:
    """Get the top 10 merchants by total spend."""
    return await top_merchants()


@mcp.tool()
async def monthly_spend_report_tool() -> dict:
    """Get spending broken down by month."""
    return await monthly_spend_report()


@mcp.tool()
async def generate_finance_insights_tool() -> dict:
    """Generate AI-powered finance insights (burn rate, spikes, trends, recommendations)."""
    return await generate_finance_insights()


# ============================================================================
# CONTROL TOOLS
# ============================================================================


@mcp.tool()
async def flag_high_spend_tool(threshold: float) -> dict:
    """Flag all transactions above a spending threshold."""
    return await flag_high_spend(threshold)


@mcp.tool()
async def find_duplicate_transactions_tool() -> dict:
    """Find potential duplicate transactions (same merchant + amount within 24h)."""
    return await find_duplicate_transactions()


@mcp.tool()
async def detect_suspicious_transactions_tool() -> dict:
    """Detect suspicious transactions (outliers, new merchants, high velocity)."""
    return await detect_suspicious_transactions()


@mcp.tool()
async def explain_spend_anomalies_tool() -> dict:
    """Comprehensive anomaly explanation with confidence scores."""
    return await explain_spend_anomalies()


# ============================================================================
# USER TOOLS
# ============================================================================


@mcp.tool()
async def list_users_tool() -> dict:
    """List all users in the Float organization."""
    return await list_users()


@mcp.tool()
async def get_user_by_id_tool(user_id: str) -> dict:
    """Retrieve a single user by ID."""
    return await get_user_by_id(user_id)


@mcp.tool()
async def assign_card_to_user_tool(card_id: str, user_id: str) -> dict:
    """Assign a card to a user."""
    return await assign_card_to_user(card_id, user_id)


# ============================================================================
# ACCOUNT TOOLS
# ============================================================================


@mcp.tool()
async def get_accounts_tool() -> dict:
    """Retrieve all accounts."""
    return await get_accounts()


@mcp.tool()
async def get_account_by_id_tool(account_id: str) -> dict:
    """Retrieve a single account by ID."""
    return await get_account_by_id(account_id)


@mcp.tool()
async def get_account_transactions_tool(limit: int = 50) -> dict:
    """Retrieve account transactions with pagination."""
    return await get_account_transactions(limit)


@mcp.tool()
async def get_account_transaction_by_id_tool(transaction_id: str) -> dict:
    """Retrieve a single account transaction by ID."""
    return await get_account_transaction_by_id(transaction_id)


# ============================================================================
# BILL TOOLS
# ============================================================================


@mcp.tool()
async def get_bills_tool(limit: int = 50) -> dict:
    """Retrieve bills with pagination."""
    return await get_bills(limit)


@mcp.tool()
async def get_bill_by_id_tool(bill_id: str) -> dict:
    """Retrieve a single bill by ID."""
    return await get_bill_by_id(bill_id)


@mcp.tool()
async def update_bill_tool(bill_id: str, data: dict) -> dict:
    """Update a single bill."""
    return await update_bill(bill_id, data)


@mcp.tool()
async def update_bills_tool(updates: list) -> dict:
    """Update multiple bills in bulk."""
    return await update_bills(updates)


@mcp.tool()
async def mark_bill_synced_tool(bill_id: str) -> dict:
    """Mark a bill as synced."""
    return await mark_bill_synced(bill_id)


@mcp.tool()
async def get_bill_attachments_tool(bill_id: str, limit: int = 50) -> dict:
    """Retrieve attachments for a specific bill."""
    return await get_bill_attachments(bill_id, limit)


@mcp.tool()
async def get_bill_attachment_by_id_tool(attachment_id: str) -> dict:
    """Retrieve a single bill attachment by ID."""
    return await get_bill_attachment_by_id(attachment_id)


# ============================================================================
# REIMBURSEMENT TOOLS
# ============================================================================


@mcp.tool()
async def get_reimbursements_tool(limit: int = 50) -> dict:
    """Retrieve reimbursement reports with pagination."""
    return await get_reimbursements(limit)


@mcp.tool()
async def get_reimbursement_by_id_tool(reimbursement_id: str) -> dict:
    """Retrieve a single reimbursement report by ID."""
    return await get_reimbursement_by_id(reimbursement_id)


@mcp.tool()
async def update_reimbursement_tool(reimbursement_id: str, data: dict) -> dict:
    """Update a single reimbursement."""
    return await update_reimbursement(reimbursement_id, data)


@mcp.tool()
async def update_reimbursements_tool(updates: list) -> dict:
    """Update multiple reimbursements in bulk."""
    return await update_reimbursements(updates)


@mcp.tool()
async def mark_reimbursement_synced_tool(reimbursement_id: str) -> dict:
    """Mark a reimbursement as synced."""
    return await mark_reimbursement_synced(reimbursement_id)


# ============================================================================
# PAYMENT TOOLS
# ============================================================================


@mcp.tool()
async def get_payments_tool(limit: int = 50) -> dict:
    """Retrieve payments with pagination."""
    return await get_payments(limit)


@mcp.tool()
async def get_payment_by_id_tool(payment_id: str) -> dict:
    """Retrieve a single payment by ID."""
    return await get_payment_by_id(payment_id)


# ============================================================================
# VENDOR TOOLS
# ============================================================================


@mcp.tool()
async def get_vendors_tool() -> dict:
    """Retrieve all vendors."""
    return await get_vendors()


@mcp.tool()
async def get_vendor_by_id_tool(vendor_id: str) -> dict:
    """Retrieve a single vendor by ID."""
    return await get_vendor_by_id(vendor_id)


@mcp.tool()
async def create_vendor_tool(name: str, email: str = "", address: str = "", tax_code_id: str = "") -> dict:
    """Create a new vendor."""
    return await create_vendor(name, email, address, tax_code_id)


@mcp.tool()
async def update_vendor_tool(vendor_id: str, data: dict) -> dict:
    """Update a vendor."""
    return await update_vendor(vendor_id, data)


# ============================================================================
# ACCOUNTING TOOLS (GL CODES, TAX CODES, CUSTOM FIELDS)
# ============================================================================


@mcp.tool()
async def get_gl_codes_tool(limit: int = 50) -> dict:
    """Retrieve GL codes with pagination."""
    return await get_gl_codes(limit)


@mcp.tool()
async def get_gl_code_by_id_tool(gl_code_id: str) -> dict:
    """Retrieve a single GL code by ID."""
    return await get_gl_code_by_id(gl_code_id)


@mcp.tool()
async def create_gl_code_tool(name: str, code: str, account_type: str = "") -> dict:
    """Create a new GL code."""
    return await create_gl_code(name, code, account_type)


@mcp.tool()
async def get_tax_codes_tool() -> dict:
    """Retrieve all tax codes."""
    return await get_tax_codes()


@mcp.tool()
async def get_tax_code_by_id_tool(tax_code_id: str) -> dict:
    """Retrieve a single tax code by ID."""
    return await get_tax_code_by_id(tax_code_id)


@mcp.tool()
async def create_tax_code_tool(name: str, rate: float) -> dict:
    """Create a new tax code."""
    return await create_tax_code(name, rate)


@mcp.tool()
async def delete_tax_code_tool(tax_code_id: str) -> dict:
    """Delete a tax code."""
    return await delete_tax_code(tax_code_id)


@mcp.tool()
async def get_tax_components_tool() -> dict:
    """Retrieve all tax components."""
    return await get_tax_components()


@mcp.tool()
async def get_custom_fields_tool(limit: int = 50) -> dict:
    """Retrieve custom fields with pagination."""
    return await get_custom_fields(limit)


@mcp.tool()
async def get_custom_field_by_id_tool(field_id: str) -> dict:
    """Retrieve a single custom field by ID."""
    return await get_custom_field_by_id(field_id)


@mcp.tool()
async def create_custom_field_tool(name: str, field_type: str) -> dict:
    """Create a new custom field."""
    return await create_custom_field(name, field_type)


@mcp.tool()
async def delete_custom_field_tool(field_id: str) -> dict:
    """Delete a custom field."""
    return await delete_custom_field(field_id)


@mcp.tool()
async def create_custom_field_option_tool(field_id: str, value: str) -> dict:
    """Create a custom field option."""
    return await create_custom_field_option(field_id, value)


@mcp.tool()
async def delete_custom_field_option_tool(field_id: str, option_id: str) -> dict:
    """Delete a custom field option."""
    return await delete_custom_field_option(field_id, option_id)


# ============================================================================
# ORG TOOLS (TEAMS, SUBSIDIARIES, RECEIPTS, POLICIES)
# ============================================================================


@mcp.tool()
async def get_teams_tool(limit: int = 50) -> dict:
    """Retrieve teams with pagination."""
    return await get_teams(limit)


@mcp.tool()
async def get_team_by_id_tool(team_id: str) -> dict:
    """Retrieve a single team by ID."""
    return await get_team_by_id(team_id)


@mcp.tool()
async def get_subsidiaries_tool() -> dict:
    """Retrieve all subsidiaries."""
    return await get_subsidiaries()


@mcp.tool()
async def get_subsidiary_by_id_tool(subsidiary_id: str) -> dict:
    """Retrieve a single subsidiary by ID."""
    return await get_subsidiary_by_id(subsidiary_id)


@mcp.tool()
async def get_receipts_tool(limit: int = 50) -> dict:
    """Retrieve receipts with pagination."""
    return await get_receipts(limit)


@mcp.tool()
async def get_receipt_by_id_tool(receipt_id: str) -> dict:
    """Retrieve a single receipt by ID."""
    return await get_receipt_by_id(receipt_id)


@mcp.tool()
async def get_approval_policies_tool(limit: int = 50) -> dict:
    """Retrieve approval policies with pagination."""
    return await get_approval_policies(limit)


@mcp.tool()
async def get_approval_policy_by_id_tool(policy_id: str) -> dict:
    """Retrieve a single approval policy by ID."""
    return await get_approval_policy_by_id(policy_id)


@mcp.tool()
async def get_submission_policies_tool(limit: int = 50) -> dict:
    """Retrieve submission policies with pagination."""
    return await get_submission_policies(limit)


@mcp.tool()
async def get_submission_policy_by_id_tool(policy_id: str) -> dict:
    """Retrieve a single submission policy by ID."""
    return await get_submission_policy_by_id(policy_id)


# ============================================================================
# TEST BLOCK
# ============================================================================


async def _test():
    """Test basic functionality."""
    print("=" * 60)
    print("FLOAT MCP SERVER — TEST BLOCK")
    print("=" * 60)

    print("\n[1/2] Testing create_card...")
    result = await create_card("Test Card", 1000)
    print(f"Result: {result}")

    print("\n[2/2] Testing get_transactions...")
    result = await get_transactions(limit=5)
    print(f"Result: {result}")

    print("\nTest block complete.")


if __name__ == "__main__":
    asyncio.run(_test())
