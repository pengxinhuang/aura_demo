"""
Utility functions and main optimization logic
Combines all agents to provide recommendations
"""

from .merchant_agent import classify_merchant
from .scoring_engine import score_best_card

def optimize_one(merchant: str, amount: float, currency: str, 
                 location: dict, user_cards: list, mock_mode: bool = True) -> dict:
    """
    Main optimization function that orchestrates all agents.
    
    TODO: When integrating real agents:
    1. Import real agent modules from /agents/ folder
    2. Replace mock calls with real API/function calls
    3. Add error handling and fallbacks
    4. Implement caching for frequent queries
    
    Args:
        merchant: Merchant name
        amount: Transaction amount
        currency: Currency code
        location: Location data dict
        user_cards: User's credit cards
        mock_mode: If True, use mock data; if False, call real agents
    
    Returns:
        Complete recommendation result following API contract
    """
    
    if mock_mode:
        # Use stub agents
        classification = classify_merchant(merchant, location)
        
        txn = {
            "merchant": merchant,
            "amount": amount,
            "currency": currency,
            "category": classification["predicted_category"],
            "mcc": classification["predicted_mcc"]
        }
        
        scoring = score_best_card(txn, user_cards)
        
        # Format response per API contract
        return {
            "summary": {
                "total_expected_reward": scoring["recommendations"][0]["reward"] if scoring["recommendations"] else 0,
                "unit": currency
            },
            "per_txn": [
                {
                    "id": "t1",
                    "merchant": merchant,
                    "predicted_mcc": classification["predicted_mcc"],
                    "predicted_category": classification["predicted_category"],
                    "best_card": scoring["recommendations"][0]["card"] if scoring["recommendations"] else "None",
                    "expected_reward": scoring["recommendations"][0]["reward"] if scoring["recommendations"] else 0,
                    "confidence": classification["confidence"],
                    "explain": {
                        "matched_rule": scoring["recommendations"][0]["matched_rule"] if scoring["recommendations"] else "",
                        "calc_trace": scoring["recommendations"][0]["calc_trace"] if scoring["recommendations"] else "",
                        "recommendations": scoring["recommendations"],
                        "evidence": classification["evidence"]
                    }
                }
            ]
        }
    else:
        # TODO: Call real agents via API
        # Example:
        # import requests
        # API_BASE = os.getenv("AURA_API_BASE", "http://localhost:8000")
        # 
        # classification = requests.post(
        #     f"{API_BASE}/classify",
        #     json={"merchant": merchant, "location": location}
        # ).json()
        #
        # scoring = requests.post(
        #     f"{API_BASE}/score",
        #     json={"txn": txn, "cards": user_cards}
        # ).json()
        
        raise NotImplementedError("Live mode not yet implemented. Please use mock mode.")