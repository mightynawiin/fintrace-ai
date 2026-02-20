# backend/app/formatter.py

def format_output(suspicious_accounts, rings, total_accounts, processing_time):
    fraud_rings = []

    for ring in rings:
        members = ring["member_accounts"]
        pattern = ring["pattern_type"]

        # Clean pattern name
        if pattern.startswith("cycle"):
            clean_pattern = "cycle"
        elif pattern.startswith("fan_in"):
            clean_pattern = "fan_in"
        elif pattern.startswith("fan_out"):
            clean_pattern = "fan_out"
        elif pattern == "layered_shell":
            clean_pattern = "layered_shell"
        else:
            clean_pattern = pattern

        # Calculate average risk score
        member_scores = [
            acc["suspicion_score"]
            for acc in suspicious_accounts
            if acc["account_id"] in members
        ]

        avg_score = sum(member_scores) / len(member_scores) if member_scores else 0.0

        # FORCE FLOAT FORMAT
        formatted_avg = float(f"{avg_score:.1f}")

        fraud_rings.append({
            "ring_id": ring["ring_id"],
            "member_accounts": members,
            "pattern_type": clean_pattern,
            "risk_score": formatted_avg
        })

    summary = {
        "total_accounts_analyzed": total_accounts,
        "suspicious_accounts_flagged": len(suspicious_accounts),
        "fraud_rings_detected": len(fraud_rings),
        "processing_time_seconds": round(processing_time, 3)

    }

    return {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": fraud_rings,
        "summary": summary
    }
