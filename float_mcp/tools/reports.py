"""Report tools: spending analysis and AI-powered finance insights."""

import statistics
from collections import defaultdict
from datetime import datetime

from float_mcp.tools.transactions import _fetch_transactions


async def summarize_spend() -> dict:
    """
    Summarize total spend and spending by transaction type.

    # TODO: Float API has no native expense category field.
    Grouping by transaction type (CAPTURE, REFUND, etc.).

    Returns:
        {"total_spend": float, "by_type": {...}} or {"error": "..."}
    """
    transactions = await _fetch_transactions(limit=1000)

    if not transactions:
        return {"total_spend": 0.0, "by_type": {}}

    total_spend = sum(t["amount"] for t in transactions)
    by_type = defaultdict(float)

    for t in transactions:
        by_type[t.get("type", "UNKNOWN")] += t["amount"]

    return {
        "total_spend": round(total_spend, 2),
        "by_type": {k: round(v, 2) for k, v in dict(by_type).items()},
    }


async def top_merchants() -> dict:
    """
    Get the top 10 merchants by total spend.

    Returns:
        {"top_merchants": [{"merchant": str, "total_spend": float}, ...]}
    """
    transactions = await _fetch_transactions(limit=1000)

    if not transactions:
        return {"top_merchants": []}

    merchant_totals = defaultdict(float)

    for t in transactions:
        merchant = t.get("merchant", "Unknown")
        merchant_totals[merchant] += t["amount"]

    sorted_merchants = sorted(
        merchant_totals.items(), key=lambda x: x[1], reverse=True
    )[:10]

    return {
        "top_merchants": [
            {"merchant": m, "total_spend": round(s, 2)} for m, s in sorted_merchants
        ]
    }


async def monthly_spend_report() -> dict:
    """
    Get spending broken down by month (YYYY-MM).

    Returns:
        {"monthly_spend": {"2024-01": float, "2024-02": float, ...}}
    """
    transactions = await _fetch_transactions(limit=1000)

    if not transactions:
        return {"monthly_spend": {}}

    monthly = defaultdict(float)

    for t in transactions:
        month = t["date"][:7]  # Extract YYYY-MM
        monthly[month] += t["amount"]

    # Sort by month
    sorted_months = dict(sorted(monthly.items()))

    return {
        "monthly_spend": {k: round(v, 2) for k, v in sorted_months.items()}
    }


async def generate_finance_insights() -> dict:
    """
    Generate AI-powered finance insights using statistical analysis.

    Returns algorithmic intelligence on:
    - Burn rate (daily spend average)
    - Category spikes (>2x monthly average)
    - Weekly trends (week-over-week growth)
    - Recommendations (rule-based)

    Returns:
        {
            "burn_rate_per_day": float,
            "category_spikes": [...],
            "weekly_trend": {...},
            "recommendations": [...]
        }
    """
    transactions = await _fetch_transactions(limit=1000)

    if not transactions:
        return {
            "burn_rate_per_day": 0.0,
            "category_spikes": [],
            "weekly_trend": {},
            "recommendations": ["No transactions to analyze."],
        }

    # 1. BURN RATE
    # Calculate dollars per day
    dates = [datetime.fromisoformat(t["date"]) for t in transactions]
    if dates:
        date_range = (max(dates) - min(dates)).days or 1
        total_spend = sum(t["amount"] for t in transactions)
        burn_rate = total_spend / date_range
    else:
        burn_rate = 0.0

    # 2. CATEGORY SPIKES
    # Group by month and merchant, find spikes (current > 2x historical avg)
    category_monthly = defaultdict(list)

    for t in transactions:
        month = t["date"][:7]
        merchant = t.get("merchant", "Unknown")
        category = f"{merchant}"  # Use merchant as category proxy
        category_monthly[category].append((month, t["amount"]))

    spikes = []
    for category, entries in category_monthly.items():
        # Group by month
        monthly_totals = defaultdict(float)
        for month, amount in entries:
            monthly_totals[month] += amount

        months = sorted(monthly_totals.keys())
        if len(months) < 2:
            continue

        current_month = months[-1]
        current_amount = monthly_totals[current_month]
        historical_amounts = [monthly_totals[m] for m in months[:-1]]
        historical_avg = statistics.mean(historical_amounts)

        if historical_avg > 0 and current_amount > 2 * historical_avg:
            spikes.append({
                "category": category,
                "current_month": current_month,
                "current_spend": round(current_amount, 2),
                "historical_avg": round(historical_avg, 2),
                "multiple": round(current_amount / historical_avg, 2),
            })

    # Sort by multiple (highest spike first)
    spikes = sorted(spikes, key=lambda x: x["multiple"], reverse=True)[:5]

    # 3. WEEKLY TREND
    # Compare last 7 days vs prior 7 days
    sorted_txns = sorted(transactions, key=lambda t: t["date"])
    if len(sorted_txns) > 0:
        last_date = datetime.fromisoformat(sorted_txns[-1]["date"])
        last_7_days = [
            t for t in sorted_txns
            if (last_date - datetime.fromisoformat(t["date"])).days <= 7
        ]
        prior_7_days = [
            t for t in sorted_txns
            if 7 < (last_date - datetime.fromisoformat(t["date"])).days <= 14
        ]

        last_7_spend = sum(t["amount"] for t in last_7_days)
        prior_7_spend = sum(t["amount"] for t in prior_7_days) or 1

        weekly_growth = round((last_7_spend / prior_7_spend - 1) * 100, 1)
        weekly_trend = {
            "last_7_days_spend": round(last_7_spend, 2),
            "prior_7_days_spend": round(prior_7_spend, 2),
            "growth_percent": weekly_growth,
        }
    else:
        weekly_trend = {}

    # 4. RECOMMENDATIONS
    recommendations = []

    if burn_rate > 500:
        recommendations.append(
            f"High daily burn rate: ${burn_rate:.2f}/day. Review large recurring charges."
        )
    elif burn_rate > 200:
        recommendations.append(
            f"Moderate daily burn rate: ${burn_rate:.2f}/day. Monitor for cost optimization opportunities."
        )

    for spike in spikes[:3]:  # Top 3 spikes
        recommendations.append(
            f"Spike detected in {spike['category']}: {spike['multiple']}x historical average in {spike['current_month']}"
        )

    if "weekly_growth" in weekly_trend and weekly_trend["growth_percent"] > 50:
        recommendations.append(
            f"Week-over-week spending increased {weekly_trend['growth_percent']}%. Investigate outliers."
        )

    if not recommendations:
        recommendations.append("Spending patterns appear normal.")

    return {
        "burn_rate_per_day": round(burn_rate, 2),
        "category_spikes": spikes,
        "weekly_trend": weekly_trend,
        "recommendations": recommendations,
    }
