"""MCP server for Float Finance Copilot.

Registers all tools via FastMCP decorators and exposes them to Claude or other MCP clients.
"""

import asyncio
import logging

from mcp.server.fastmcp import FastMCP

# Import all tool functions
from float_mcp.tools.cards import (
    create_card,
    freeze_card,
    get_cards,
    update_card_limit,
)
from float_mcp.tools.controls import (
    detect_suspicious_transactions,
    explain_spend_anomalies,
    find_duplicate_transactions,
    flag_high_spend,
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
)
from float_mcp.tools.users import assign_card_to_user, list_users

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
async def assign_card_to_user_tool(card_id: str, user_id: str) -> dict:
    """Assign a card to a user."""
    return await assign_card_to_user(card_id, user_id)


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
