"""
Scoring Engine Agent (Stub)
TO BE REPLACED with real scoring and optimization logic
"""

def score_best_card(txn: dict, user_cards: list) -> dict:
    """
    Score and rank credit cards for a transaction.
    
    TODO: Replace with real scoring logic:
    - Load actual card T&Cs and rules
    - Calculate precise cashback/miles
    - Consider caps and tier bonuses
    - Apply user preferences
    
    Args:
        txn: Transaction dict with merchant, amount, category, etc.
        user_cards: List of user's credit cards
    
    Returns:
        Scoring result with top recommendations and calculations
    """
    
    amount = txn.get("amount", 0)
    category = txn.get("category", "General")
    
    # Mock scoring rules (to be replaced with rule engine)
    MILE_TO_SGD = 0.02
    category_rates = {
        "Dining": {
            "Citi Cash Back+": {"rate": 0.08, "unit": "sgd"},
            "DBS Altitude": {"rate": 3.0, "unit": "mile"},
            "UOB One": {"rate": 0.05, "unit": "sgd"},
            "OCBC 365": {"rate": 0.06, "unit": "sgd"},
            "StanChart Unlimited": {"rate": 0.015, "unit": "sgd"}
        },
        "Groceries": {
            "Citi Cash Back+": {"rate": 0.08, "unit": "sgd"},
            "DBS Altitude": {"rate": 1.2, "unit": "mile"},
            "UOB One": {"rate": 0.10, "unit": "sgd"},
            "OCBC 365": {"rate": 0.03, "unit": "sgd"},
            "StanChart Unlimited": {"rate": 0.015, "unit": "sgd"}
        },
        "Transport": {
            "Citi Cash Back+": {"rate": 0.08, "unit": "sgd"},
            "DBS Altitude": {"rate": 2.0, "unit": "mile"},
            "UOB One": {"rate": 0.03, "unit": "sgd"},
            "OCBC 365": {"rate": 0.03, "unit": "sgd"},
            "StanChart Unlimited": {"rate": 0.03, "unit": "sgd"}
        },
        "General": {
            "Citi Cash Back+": {"rate": 0.015, "unit": "sgd"},
            "DBS Altitude": {"rate": 1.2, "unit": "mile"},
            "UOB One": {"rate": 0.01, "unit": "sgd"},
            "OCBC 365": {"rate": 0.006, "unit": "sgd"},
            "StanChart Unlimited": {"rate": 0.015, "unit": "sgd"}
        }
    }
    
    # Calculate rewards for each card
    recommendations = []
    rates = category_rates.get(category, category_rates["General"])

    for card in user_cards[:5]:  # Limit to user's cards
        card_name = card["display_name"]
        rate_info = rates.get(card_name) or {"rate": 0.01, "unit": "sgd"}
        rate = rate_info["rate"]
        unit = rate_info.get("unit", "sgd")

        if unit == "mile":
            reward_value = amount * rate * MILE_TO_SGD
            calc_trace = (
                f"${amount:.2f} x {rate:.1f} miles x ${MILE_TO_SGD:.2f} = ${reward_value:.2f}"
            )
            matched_rule = f"{category} {rate:.1f} miles per dollar"
        else:
            reward_value = amount * rate
            calc_trace = f"${amount:.2f} x {rate * 100:.1f}% = ${reward_value:.2f}"
            matched_rule = f"{category} {rate * 100:.1f}% cashback"

        # Check monthly cap
        remaining_cap = card["monthly_cap"] - card["used_this_month"]
        if reward_value > remaining_cap:
            reward_value = max(remaining_cap, 0)
            capped = True
        else:
            capped = False

        recommendations.append({
            "card": card_name,
            "bank": card["bank"],
            "reward": round(reward_value, 2),
            "rate": rate,
            "rate_unit": unit,
            "calc_trace": calc_trace,
            "matched_rule": matched_rule + (" (cap reached)" if capped else ""),
            "capped": capped,
            "last4": card.get("last4", "0000"),
            "card_id": card.get("id"),
        })
    
    # Sort by reward amount
    recommendations.sort(key=lambda x: x["reward"], reverse=True)
    
    return {
        "recommendations": recommendations[:3],  # Top 3
        "calculation_method": "category_based_rates"
    }
