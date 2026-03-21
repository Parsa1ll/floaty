import asyncio
import json

from float_mcp.tools.controls import (
    detect_suspicious_transactions,
    explain_spend_anomalies,
)
from float_mcp.tools.reports import generate_finance_insights
from float_mcp.tools.transactions import get_transactions


async def run_demo():
    """Run the full demo flow."""
    print("\n" + "=" * 70)
    print("🤖 FLOAT AI FINANCE COPILOT — DEMO")
    print("=" * 70)

    # [1] Fetch recent transactions
    print("\n[1/4] Fetching recent transactions...")
    txns_result = await get_transactions(limit=100)

    if "error" in txns_result:
        print(f"❌ Error: {txns_result['error']}")
        return

    transactions = txns_result.get("transactions", [])
    print(f"✅ Loaded {len(transactions)} transactions")

    if not transactions:
        print("⚠️  No transactions found. Skipping analysis.")
        return

    # Show first 3 transactions
    if transactions:
        print("\n   Sample transactions:")
        for i, t in enumerate(transactions[:3], 1):
            print(
                f"   {i}. {t['merchant']:30s} ${t['amount']:>8.2f} ({t['date']})"
            )
        if len(transactions) > 3:
            print(f"   ... and {len(transactions) - 3} more")

    # [2] Detect suspicious activity
    print("\n[2/4] Analyzing for suspicious transactions...")
    suspicious_result = await detect_suspicious_transactions()

    if "error" in suspicious_result:
        print(f"❌ Error: {suspicious_result['error']}")
    else:
        suspicious = suspicious_result.get("suspicious", [])
        count = suspicious_result.get("count", 0)

        if count > 0:
            print(f"🚨 Found {count} suspicious transactions:")
            for s in suspicious[:5]:
                risk_type = s["risk_type"].replace("_", " ").title()
                print(f"   • [{risk_type}] {s['transaction']['merchant']} - ${s['transaction']['amount']:.2f}")
        else:
            print("✅ No suspicious transactions detected")

    # [3] Generate finance insights
    print("\n[3/4] Generating finance insights...")
    insights_result = await generate_finance_insights()

    if "error" in insights_result:
        print(f"❌ Error: {insights_result['error']}")
    else:
        burn_rate = insights_result.get("burn_rate_per_day", 0)
        spikes = insights_result.get("category_spikes", [])
        recommendations = insights_result.get("recommendations", [])

        print(f"   💰 Daily burn rate: ${burn_rate:.2f}")

        if spikes:
            print(f"   📈 Category spikes detected ({len(spikes)}):")
            for spike in spikes[:3]:
                print(
                    f"      • {spike['category']}: {spike['multiple']}x average in {spike['current_month']}"
                )
        else:
            print("   📊 No significant category spikes detected")

        if recommendations:
            print("   💡 Recommendations:")
            for rec in recommendations[:3]:
                print(f"      • {rec}")

    # [4] Explain spend anomalies
    print("\n[4/4] Explaining spend anomalies (with confidence)...")
    anomalies_result = await explain_spend_anomalies()

    if "error" in anomalies_result:
        print(f"❌ Error: {anomalies_result['error']}")
    else:
        anomalies = anomalies_result.get("anomalies", [])
        count = anomalies_result.get("count", 0)

        if count > 0:
            print(f"🔍 Found {count} anomalies:")
            for a in anomalies[:5]:
                confidence = int(a["confidence_score"] * 100)
                print(
                    f"   • [{confidence}% confidence] {a['anomaly']}"
                )
        else:
            print("✅ No anomalies detected")

    print("\n" + "=" * 70)
    print("✨ Demo complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(run_demo())
