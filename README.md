# Float MCP — AI Finance Copilot

> **Model Context Protocol (MCP) server for Float Financial API**
>
> A production-ready, fully-featured MCP server that exposes Float's complete API surface with AI-powered finance intelligence, fraud detection, and anomaly analysis.

---
## 🎬 Demo
<div align="center">
  <a href="https://www.youtube.com/watch?v=Msyh6SsYRC4">
    <img src="https://www.youtube.com/watch?v=FxuzlSiENwI/maxresdefault.jpg" alt="Floaty Demo Video" width="800"/>
  </a>
  <br/>
  <strong>Click the image above to watch the demo on YouTube</strong>
</div>

## 🎯 Overview

**Float MCP** is a comprehensive Model Context Protocol server that integrates seamlessly with Claude and other MCP clients to enable:

- ✅ **Full Float API Access** — All 68 endpoints wrapped as clean, structured tools
- 🤖 **AI Finance Intelligence** — Burn rate analysis, spend spikes, anomaly detection
- 🛡️ **Fraud Detection** — Statistical outlier detection, new merchant alerts, velocity monitoring
- 📊 **Real-time Insights** — Generate actionable recommendations from financial data
- 🔄 **Production-Ready** — Async/await, retry logic, rate limiting, comprehensive error handling

Perfect for building AI agents that need to **operate on actual financial data** (not just CRUD endpoints).

---

## 🏗️ Architecture

### Project Structure

```
float_mcp/
├── server.py                 # MCP server with 68 registered tools (FastMCP)
├── config.py                 # Configuration (API key, base URL)
├── utils/
│   └── float_client.py       # Async HTTP client (retry, rate-limit handling)
└── tools/                    # Organized by resource type
    ├── accounts.py           # Accounts & account transactions (4 tools)
    ├── bills.py              # Bills, attachments, syncing (7 tools)
    ├── cards.py              # Card management, limits (5 tools)
    ├── transactions.py       # Card transactions, filtering, updates (6 tools)
    ├── reports.py            # Spend summary, insights, trends (4 tools)
    ├── controls.py           # Fraud detection, anomaly analysis (4 tools)
    ├── payments.py           # Payment history (2 tools)
    ├── reimbursements.py     # Reimbursement workflows (5 tools)
    ├── vendors.py            # Vendor CRUD (4 tools)
    ├── users.py              # User management (3 tools)
    ├── accounting.py         # GL codes, tax codes, custom fields (15 tools)
    └── org.py                # Teams, policies, receipts (10 tools)
```

### Design Patterns

1. **FastMCP Framework**
   - Uses Anthropic's FastMCP for streamlined MCP server development
   - All tools registered via `@mcp.tool()` decorators
   - Tools are async functions that wrap the actual implementation

2. **Module Singleton Pattern**
   - `FloatClient` is instantiated once and reused across all tools
   - Persistent HTTP session with connection pooling

3. **Normalizer Functions**
   - Each resource type has `_normalize_*()` to map API responses to clean schemas (19 normalizers)
   - Consistent field naming across tools
   - Cents → dollars conversion for all amounts

4. **Error Propagation**
   - Tools never raise exceptions
   - All functions return `{"error": "message"}` on failure
   - Errors bubble up cleanly to MCP clients

5. **Pagination**
   - Multi-page requests handled internally
   - `limit` parameter controls total results
   - Safe handling of partial/missing data

---

## 🚀 Quick Start

### Installation

```bash
# Clone and enter directory
git clone https://github.com/Parsa1ll/floaty
cd floaty

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
FLOAT_API_KEY=your_api_key_here
FLOAT_BASE_URL=https://api.floatfinancial.com
```

### Test the Installation

```bash
# Run the built-in test block
python -m float_mcp.server --test
```

This will:
1. Test card creation
2. Fetch recent transactions
3. Verify API connectivity

### Use as MCP Server

```bash
# Start the MCP server (listens for stdio via FastMCP)
python -m float_mcp.server
```

Then connect from Claude or other MCP clients to access all 68 tools.

---

## 📚 Available Tools (68)

### Accounts (4 tools)
- `get_accounts` — List all accounts
- `get_account_by_id` — Fetch single account
- `get_account_transactions` — Paginated account transactions
- `get_account_transaction_by_id` — Single account transaction

### Cards (5 tools)
- `get_cards` — List all cards
- `get_card_by_id` — Fetch single card
- `create_card` — Create new card with limit
- `freeze_card` — Disable a card
- `update_card_limit` — Modify spending limit

### Transactions (6 tools)
- `get_transactions` — Fetch paginated transactions
- `get_transaction_by_id` — Single transaction details
- `filter_transactions_by_date` — Date range filtering
- `filter_transactions_by_amount` — Amount range filtering
- `update_transaction` — Modify transaction metadata
- `update_transactions` — Bulk update transactions

### Bills (7 tools)
- `get_bills` — Paginated bills
- `get_bill_by_id` — Single bill
- `update_bill` — Modify bill
- `update_bills` — Bulk update
- `mark_bill_synced` — Mark as synced
- `get_bill_attachments` — Fetch receipts
- `get_bill_attachment_by_id` — Single attachment

### Reimbursements (5 tools)
- `get_reimbursements` — Paginated reimbursements
- `get_reimbursement_by_id` — Single reimbursement
- `update_reimbursement` — Modify status/metadata
- `update_reimbursements` — Bulk update
- `mark_reimbursement_synced` — Mark as synced

### Payments (2 tools)
- `get_payments` — Paginated payments
- `get_payment_by_id` — Single payment

### Vendors (4 tools)
- `get_vendors` — List all vendors
- `get_vendor_by_id` — Fetch single vendor
- `create_vendor` — Add new vendor
- `update_vendor` — Modify vendor details

### Accounting (15 tools)
- **GL Codes:** `get_gl_codes`, `get_gl_code_by_id`, `create_gl_code`
- **Tax Codes:** `get_tax_codes`, `get_tax_code_by_id`, `create_tax_code`, `delete_tax_code`
- **Tax Components:** `get_tax_components`
- **Custom Fields:** `get_custom_fields`, `get_custom_field_by_id`, `create_custom_field`, `delete_custom_field`, `create_custom_field_option`, `delete_custom_field_option`

### Organization (10 tools)
- **Teams:** `get_teams`, `get_team_by_id`
- **Subsidiaries:** `get_subsidiaries`, `get_subsidiary_by_id`
- **Receipts:** `get_receipts`, `get_receipt_by_id`
- **Policies:** `get_approval_policies`, `get_approval_policy_by_id`, `get_submission_policies`, `get_submission_policy_by_id`

### Users (3 tools)
- `list_users` — All users in organization
- `get_user_by_id` — Single user
- `assign_card_to_user` — Assign card ownership

### Reports & Analytics (4 tools)

**Spend Analysis:**
- `summarize_spend` — Total spend + breakdown by type
- `top_merchants` — Top 10 vendors by amount
- `monthly_spend_report` — Month-over-month trends

**AI Finance Intelligence:**
- `generate_finance_insights` — Burn rate, spend spikes, week-over-week growth, recommendations

**Fraud & Anomaly Detection:**
- `detect_suspicious_transactions` — Outliers (3σ), new merchants, high velocity (>5/hour)
- `find_duplicate_transactions` — Same merchant + amount within 24h
- `flag_high_spend` — Transactions above threshold
- `explain_spend_anomalies` — Detailed anomalies with confidence scores (0.0-1.0)

---

## 🤖 AI Finance Intelligence

The core differentiator: **real AI-powered analysis**, not just API wrapping.

### Generate Finance Insights
```python
result = await generate_finance_insights()
```

Returns:
```json
{
  "burn_rate_per_day": 342.50,
  "category_spikes": [
    {
      "category": "AWS",
      "current_month": "2024-03",
      "current_spend": 2400.00,
      "historical_avg": 900.00,
      "multiple": 2.67
    }
  ],
  "weekly_trend": {
    "last_7_days_spend": 1500.00,
    "prior_7_days_spend": 900.00,
    "growth_percent": 66.7
  },
  "recommendations": [
    "High daily burn rate: $342.50/day. Review large recurring charges.",
    "Spike detected in AWS: 2.67x historical average in 2024-03",
    "Week-over-week spending increased 66.7%. Investigate outliers."
  ]
}
```

### Detect Suspicious Transactions
```python
result = await detect_suspicious_transactions()
```

Identifies three risk types:
1. **Large Amount** — Statistical outliers (>3 standard deviations)
2. **New Merchant** — First occurrence in last 30 days (vs. historical)
3. **High Velocity** — >5 transactions/hour from same merchant

### Explain Spend Anomalies
```python
result = await explain_spend_anomalies()
```

Combines detection + confidence scoring:
```json
{
  "anomalies": [
    {
      "anomaly": "Large Amount: AWS - $5000.00",
      "reason": "Amount $5000.00 is 4.2 standard deviations above mean ($800.00)",
      "confidence_score": 0.95,
      "transaction": {...}
    },
    {
      "anomaly": "New Merchant: DoorDash - $25.00",
      "reason": "First occurrence of merchant: DoorDash",
      "confidence_score": 0.60,
      "transaction": {...}
    }
  ],
  "count": 2
}
```

---

## 🔧 Technical Details

### HTTP Client (`FloatClient`)

**Features:**
- Async/await with `httpx`
- **Retry Logic:** 3 attempts with exponential backoff (2^attempt seconds)
- **Rate Limit Handling:** Respects 429 + `Retry-After` header
- **Timeout:** 30s per request
- **Logging:** Structured logs with endpoint, method, status, latency
- **Connection Pooling:** Persistent async client

**Error Handling:**
All errors are caught and returned as `{"error": "message"}`:
- HTTP errors (4xx, 5xx)
- Timeouts
- Connection failures
- Rate limits (auto-retry)

### Data Normalization

All API responses are cleaned and normalized:

**Transactions Example:**
```python
{
  "id": "txn_123",
  "merchant": "AWS Services",      # from vendor.name or description
  "amount": 500.00,                # cents → dollars
  "currency": "CAD",
  "date": "2024-03-15T10:30:00Z",  # ISO 8601
  "type": "CAPTURE",
  "spender": "alice@company.com",
  "team": "Engineering"
}
```

**Amounts:** All amounts stored in cents by Float API are divided by 100 when returned. When sending amounts (e.g., card limits), multiply by 100.

### Pagination

**Multi-page requests:**
```python
# Internally handles pagination
result = await get_transactions(limit=500)  # Fetches up to 500 across multiple pages
```

**Query params:**
- `page` — 1-based page number
- `page_size` — Items per page (max 1000)

**Detection:** Stops when `len(items) < page_size` (reached last page).

---

## 📖 Usage Examples

### Example 1: Check Daily Burn Rate

```python
from float_mcp.tools.reports import generate_finance_insights

insights = await generate_finance_insights()
print(f"Daily burn: ${insights['burn_rate_per_day']}/day")
print(f"Recommendations: {insights['recommendations']}")
```

### Example 2: Find Fraudulent Transactions

```python
from float_mcp.tools.controls import explain_spend_anomalies

anomalies = await explain_spend_anomalies()
high_confidence = [a for a in anomalies['anomalies'] if a['confidence_score'] > 0.8]
for anomaly in high_confidence:
    print(f"{anomaly['anomaly']}: {anomaly['reason']}")
```

### Example 3: Manage Vendor Spend

```python
from float_mcp.tools.vendors import get_vendors, create_vendor
from float_mcp.tools.bills import get_bills

vendors = await get_vendors()
bills = await get_bills(limit=100)

# Find top vendor
vendor_totals = {}
for bill in bills['bills']:
    vendor = bill['vendor_name']
    vendor_totals[vendor] = vendor_totals.get(vendor, 0) + bill['amount']

top_vendor = max(vendor_totals, key=vendor_totals.get)
print(f"Top vendor: {top_vendor} (${vendor_totals[top_vendor]:.2f})")
```

### Example 4: Sync Bills to Accounting

```python
from float_mcp.tools.bills import get_bills, mark_bill_synced

# Get unsynced bills
bills = await get_bills(limit=100)
unsynced = [b for b in bills['bills'] if not b['synced']]

# Mark as synced after processing
for bill in unsynced:
    await mark_bill_synced(bill['id'])
    print(f"Synced bill {bill['id']}")
```

---

## 🧪 Testing

### Run Built-in Test Block
```bash
python -m float_mcp.server --test
```

Tests basic functionality like card creation and transaction fetching.

### Test the MCP Server
```bash
python -m float_mcp.server
```

The server will start listening on stdio. Connect via Claude or any MCP-compatible client to test all 68 tools.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FLOAT_API_KEY` | Float API authentication token | ✅ Yes | — |
| `FLOAT_BASE_URL` | Float API base URL | ❌ No | `https://api.floatfinancial.com` |

### Example .env
```env
FLOAT_API_KEY=sk_test_abc123def456...
FLOAT_BASE_URL=https://api.floatfinancial.com
```

---

## 📦 Dependencies

```
httpx                # Async HTTP client
python-dotenv        # Environment variable loading
mcp[cli]             # Model Context Protocol (with FastMCP)
watchfiles           # File watching for development
```

Install with:
```bash
pip install -r requirements.txt
```

Or from `pyproject.toml`:
```bash
pip install -e .
```

---

## 🎓 Development Notes

### Adding a New Tool

1. **Create normalizer function** in the appropriate tool module:
   ```python
   def _normalize_resource(raw: dict) -> dict:
       return {
           "id": raw.get("id"),
           "name": raw.get("name"),
           # ... map API fields to clean schema
       }
   ```

2. **Implement tool function:**
   ```python
   async def get_resource(resource_id: str) -> dict:
       resp = await float_client.get(f"/resources/{resource_id}")
       if "error" in resp:
           return resp
       return {"resource": _normalize_resource(resp)}
   ```

3. **Register in `server.py` (using FastMCP):**
   ```python
   from float_mcp.tools.resources import get_resource

   @mcp.tool()
   async def get_resource_tool(resource_id: str) -> dict:
       """Fetch a resource by ID."""
       return await get_resource(resource_id)
   ```

   (FastMCP automatically exposes this tool to MCP clients)

### Code Style

- **Async everywhere** — Use `async def` and `await` consistently
- **Error handling** — Never raise; always return `{"error": "message"}`
- **Type hints** — Include return type hints (→ dict)
- **Docstrings** — Brief description + Args + Returns
- **Normalizers** — Map all cents to dollars, standardize field names

### Testing Best Practices

- Use actual Float API with test account
- Test with empty datasets (graceful degradation)
- Verify pagination with >1000 results
- Ensure error responses are propagated cleanly

---

## 📝 API Reference

**Float API Docs:** https://docs.floatfinancial.com/

**MCP Spec:** https://modelcontextprotocol.io/

---

## 🐛 Troubleshooting

### `FLOAT_API_KEY is not set`
→ Create `.env` file with valid API key

### `ModuleNotFoundError: No module named 'mcp'`
→ Run `pip install -r requirements.txt` in activated venv

### Tools return `{"error": "401 Unauthorized"}`
→ Check API key is valid and not expired

### Rate limit errors
→ Client auto-retries; if persistent, reduce request volume

---

## 🤝 Contributing

Contributions welcome! Please follow the development notes above and test thoroughly.

---

## 📞 Support

For issues with the MCP server, file an issue. For Float API questions, see https://docs.floatfinancial.com/
