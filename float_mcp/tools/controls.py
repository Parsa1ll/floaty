"""Control tools: fraud detection, anomaly detection, and spend controls."""

import statistics
from collections import defaultdict
from datetime import datetime, timedelta

from float_mcp.tools.transactions import _fetch_transactions


async def flag_high_spend(threshold: float) -> dict:
    """
    Flag all transactions above a spending threshold.

    Args:
        threshold: Dollar amount threshold

    Returns:
        {"flagged_transactions": [...], "threshold": float, "count": int}
    """
    transactions = await _fetch_transactions(limit=1000)

    flagged = [t for t in transactions if t["amount"] >= threshold]

    return {
        "flagged_transactions": flagged,
        "threshold": threshold,
        "count": len(flagged),
    }


async def find_duplicate_transactions() -> dict:
    """
    Find potential duplicate transactions (same merchant + amount within 24h).

    Returns:
        {
            "duplicates": [
                {
                    "transaction_1": {...},
                    "transaction_2": {...},
                    "reason": "..."
                }
            ],
            "count": int
        }
    """
    transactions = await _fetch_transactions(limit=1000)

    if len(transactions) < 2:
        return {"duplicates": [], "count": 0}

    # Group by (merchant, amount)
    groups = defaultdict(list)
    for t in transactions:
        key = (t["merchant"], round(t["amount"], 2))
        groups[key].append(t)

    duplicates = []

    for (merchant, amount), txns in groups.items():
        if len(txns) < 2:
            continue

        # Check all pairs within this group
        for i in range(len(txns)):
            for j in range(i + 1, len(txns)):
                t1, t2 = txns[i], txns[j]

                # Parse dates
                try:
                    date1 = datetime.fromisoformat(t1["date"])
                    date2 = datetime.fromisoformat(t2["date"])
                except (ValueError, KeyError):
                    continue

                # Check if within 24 hours
                delta = abs(date1 - date2)
                if delta <= timedelta(hours=24):
                    duplicates.append({
                        "transaction_1": t1,
                        "transaction_2": t2,
                        "reason": f"Same merchant ({merchant}) and amount (${amount}) within 24h",
                        "time_diff_minutes": int(delta.total_seconds() / 60),
                    })

    return {"duplicates": duplicates, "count": len(duplicates)}


async def detect_suspicious_transactions() -> dict:
    """
    Detect suspicious transactions using three algorithms:
    1. Statistical outliers (>3 std devs above mean)
    2. New/unseen merchants
    3. High velocity (>5 transactions/hour from same merchant)

    Returns:
        {
            "suspicious": [
                {
                    "transaction": {...},
                    "risk_type": "large_amount" | "new_merchant" | "high_velocity",
                    "reason": "..."
                }
            ],
            "count": int
        }
    """
    transactions = await _fetch_transactions(limit=1000)

    if not transactions:
        return {"suspicious": [], "count": 0}

    suspicious_set = set()  # Track by transaction ID to avoid duplicates
    suspicious_list = []

    # 1. STATISTICAL OUTLIERS (3 std devs above mean)
    amounts = [t["amount"] for t in transactions if t["amount"] > 0]

    if len(amounts) >= 2:
        try:
            mean = statistics.mean(amounts)
            stdev = statistics.stdev(amounts)
            threshold = mean + 3 * stdev

            for t in transactions:
                if t["amount"] > threshold and t["id"] not in suspicious_set:
                    z_score = (t["amount"] - mean) / stdev if stdev > 0 else 0
                    suspicious_set.add(t["id"])
                    suspicious_list.append({
                        "transaction": t,
                        "risk_type": "large_amount",
                        "reason": f"Amount ${t['amount']:.2f} is {z_score:.1f} standard deviations above mean (${mean:.2f})",
                    })
        except (ValueError, ZeroDivisionError):
            pass

    # 2. NEW MERCHANT DETECTION
    # Split into historical (days -90 to -30) and recent (last 30 days)
    try:
        sorted_txns = sorted(transactions, key=lambda t: t["date"])
        if sorted_txns:
            now = datetime.fromisoformat(sorted_txns[-1]["date"])
            historical_merchants = {
                t["merchant"]
                for t in sorted_txns
                if (now - datetime.fromisoformat(t["date"])).days > 30
            }
            recent_txns = [
                t
                for t in sorted_txns
                if (now - datetime.fromisoformat(t["date"])).days <= 30
            ]

            for t in recent_txns:
                if (
                    t["merchant"] not in historical_merchants
                    and t["merchant"]
                    and t["id"] not in suspicious_set
                ):
                    suspicious_set.add(t["id"])
                    suspicious_list.append({
                        "transaction": t,
                        "risk_type": "new_merchant",
                        "reason": f"First occurrence of merchant: {t['merchant']}",
                    })
    except (ValueError, AttributeError):
        pass

    # 3. HIGH VELOCITY (>5 transactions/hour from same merchant)
    merchant_txns = defaultdict(list)
    for t in transactions:
        merchant_txns[t["merchant"]].append(t)

    for merchant, txns in merchant_txns.items():
        if len(txns) < 2:
            continue

        # Sort by date
        try:
            sorted_merchant_txns = sorted(txns, key=lambda t: t["date"])
        except (ValueError, KeyError):
            continue

        # Two-pointer sliding 1-hour window
        for i, txn_i in enumerate(sorted_merchant_txns):
            try:
                date_i = datetime.fromisoformat(txn_i["date"])
            except (ValueError, KeyError):
                continue

            window_start = date_i
            window_end = date_i + timedelta(hours=1)
            window = [
                t
                for t in sorted_merchant_txns
                if window_start
                <= datetime.fromisoformat(t["date"])
                <= window_end
            ]

            if len(window) > 5 and txn_i["id"] not in suspicious_set:
                suspicious_set.add(txn_i["id"])
                suspicious_list.append({
                    "transaction": txn_i,
                    "risk_type": "high_velocity",
                    "reason": f"{len(window)} transactions from {merchant} in 1-hour window",
                })

    return {"suspicious": suspicious_list, "count": len(suspicious_list)}


async def explain_spend_anomalies() -> dict:
    """
    Comprehensive anomaly explanation with confidence scores.

    Calls detect_suspicious_transactions, find_duplicate_transactions,
    and generates confidence scores for each anomaly.

    Confidence scoring:
    - Large amount: min(1.0, (z_score - 3) / 3)
    - New merchant: 0.6 + 0.2 if amount > mean else 0
    - High velocity: min(1.0, 0.5 + count / 10)
    - Duplicate: 0.9

    Returns:
        {
            "anomalies": [
                {
                    "anomaly": "...",
                    "reason": "...",
                    "confidence_score": float (0.0-1.0),
                    "transaction": {...}
                }
            ],
            "count": int
        }
    """
    # Fetch anomalies from all detectors
    suspicious = await detect_suspicious_transactions()
    duplicates = await find_duplicate_transactions()

    anomalies = []

    # Process suspicious transactions with confidence scores
    transactions = await _fetch_transactions(limit=1000)
    amounts = [t["amount"] for t in transactions if t["amount"] > 0]

    for item in suspicious.get("suspicious", []):
        t = item["transaction"]
        risk_type = item["risk_type"]
        reason = item["reason"]

        confidence = 0.0

        if risk_type == "large_amount":
            # Confidence based on z-score
            try:
                mean = statistics.mean(amounts)
                stdev = statistics.stdev(amounts)
                if stdev > 0:
                    z_score = (t["amount"] - mean) / stdev
                    confidence = min(1.0, max(0.0, (z_score - 3) / 3))
            except (ValueError, ZeroDivisionError):
                confidence = 0.7

        elif risk_type == "new_merchant":
            # Base confidence 0.6, boost if amount is also high
            confidence = 0.6
            try:
                mean = statistics.mean(amounts)
                if t["amount"] > mean:
                    confidence = min(1.0, confidence + 0.2)
            except (ValueError, IndexError):
                pass

        elif risk_type == "high_velocity":
            # Confidence scales with transaction count in window
            # Extract count from reason string
            try:
                count = int(reason.split()[0])
                confidence = min(1.0, 0.5 + (count / 10))
            except (ValueError, IndexError):
                confidence = 0.7

        anomalies.append({
            "anomaly": f"{risk_type.replace('_', ' ').title()}: {t['merchant']} - ${t['amount']:.2f}",
            "reason": reason,
            "confidence_score": round(confidence, 2),
            "transaction": t,
        })

    # Process duplicates
    for dup in duplicates.get("duplicates", []):
        anomalies.append({
            "anomaly": f"Duplicate transaction: {dup['transaction_1']['merchant']} - ${dup['transaction_1']['amount']:.2f}",
            "reason": dup["reason"],
            "confidence_score": 0.9,
            "transaction": dup["transaction_1"],
        })

    # Sort by confidence descending
    anomalies = sorted(
        anomalies, key=lambda x: x["confidence_score"], reverse=True
    )

    return {"anomalies": anomalies, "count": len(anomalies)}
