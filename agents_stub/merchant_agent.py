"""
Merchant Classification Agent (Stub)
TO BE REPLACED with real merchant classification logic
"""

def classify_merchant(merchant: str, location: dict = None) -> dict:
    """
    Classify merchant into category and predict MCC code.
    
    TODO: Replace this stub with real classification logic:
    - Connect to MCC database
    - Use NLP for merchant name parsing
    - Incorporate location for better accuracy
    
    Args:
        merchant: Merchant name string
        location: Optional location dict with city, area, lat, lng
    
    Returns:
        Classification result with MCC, category, confidence, evidence
    """
    
    # Mock classification rules
    merchant_lower = merchant.lower()
    
    # Simple pattern matching (to be replaced with ML model)
    classifications = {
        "dining": {
            "keywords": ["restaurant", "cafe", "coffee", "food", "dining", "eat", 
                        "starbucks", "din tai fung", "mcdonald"],
            "mcc": 5812,
            "category": "Dining"
        },
        "grocery": {
            "keywords": ["fairprice", "cold storage", "sheng siong", "grocery", 
                        "supermarket", "mart"],
            "mcc": 5411,
            "category": "Groceries"
        },
        "transport": {
            "keywords": ["grab", "gojek", "taxi", "mrt", "bus", "comfort"],
            "mcc": 4121,
            "category": "Transport"
        },
        "retail": {
            "keywords": ["shop", "store", "mall", "retail", "fashion", "uniqlo"],
            "mcc": 5311,
            "category": "Shopping"
        }
    }
    
    # Find matching category
    for cat_type, cat_data in classifications.items():
        for keyword in cat_data["keywords"]:
            if keyword in merchant_lower:
                # Boost confidence if location matches known areas
                confidence = 0.85
                if location and location.get("area"):
                    if location["area"].lower() in ["orchard", "cbd", "marina bay"]:
                        confidence = 0.95
                
                return {
                    "predicted_category": cat_data["category"],
                    "predicted_mcc": cat_data["mcc"],
                    "confidence": confidence,
                    "evidence": [
                        f"Matched keyword: '{keyword}'",
                        f"Location: {location.get('area', 'Unknown')}" if location else "No location data"
                    ]
                }
    
    # Default fallback
    return {
        "predicted_category": "General",
        "predicted_mcc": 0000,
        "confidence": 0.5,
        "evidence": ["No specific category matched"]
    }