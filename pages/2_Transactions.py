"""
Transaction Page - Core functionality
Input transaction -> Get recommendations -> Use card
"""

import time
from datetime import datetime

import streamlit as st

from agents_stub.utils import optimize_one


st.set_page_config(page_title="AURA - Transactions", page_icon="🛍️", layout="wide")

st.title("🛍️ New Transaction")
st.caption("Get personalized card recommendations")


if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False
if "current_recommendation" not in st.session_state:
    st.session_state.current_recommendation = None
if "show_apple_pay" not in st.session_state:
    st.session_state.show_apple_pay = False
if "selected_card" not in st.session_state:
    st.session_state.selected_card = None
if "latest_txn_data" not in st.session_state:
    st.session_state.latest_txn_data = None
if "last_transaction_input" not in st.session_state:
    st.session_state.last_transaction_input = {}


with st.form("transaction_form"):
    st.markdown("### Transaction Details")

    col1, col2 = st.columns(2)

    with col1:
        merchant = st.text_input(
            "Merchant Name",
            placeholder="e.g., Din Tai Fung, Starbucks",
            help="Enter the merchant or store name",
        )

        amount = st.number_input(
            "Amount",
            min_value=0.01,
            value=25.50,
            step=0.01,
            help="Transaction amount",
        )

    with col2:
        currency = st.selectbox(
            "Currency",
            ["SGD", "USD", "EUR", "JPY", "CNY"],
            index=0,
        )

        st.markdown("**Location**")
        location_mode = st.radio(
            "Location method",
            ["Use current location", "Enter manually"],
            horizontal=True,
            label_visibility="collapsed",
        )

    location_data = {}
    if location_mode == "Use current location":
        st.info("Using location: Orchard, Singapore")
        location_data = {"city": "Singapore", "area": "Orchard", "lat": 1.3048, "lng": 103.8318}
    else:
        loc_col1, loc_col2 = st.columns(2)
        with loc_col1:
            city = st.text_input("City", value="Singapore")
        with loc_col2:
            area = st.text_input("Area", placeholder="e.g., Orchard")
        location_data = {"city": city, "area": area}

    submitted = st.form_submit_button(
        "Get Recommendation",
        use_container_width=True,
        type="primary",
    )


if submitted and merchant and amount > 0:
    st.session_state.last_transaction_input = {
        "merchant": merchant,
        "amount": amount,
        "currency": currency,
        "location": location_data,
    }

    with st.spinner("Analyzing transaction..."):
        time.sleep(1)
        result = optimize_one(
            merchant=merchant,
            amount=amount,
            currency=currency,
            location=location_data,
            user_cards=st.session_state.user_cards,
            mock_mode=st.session_state.mock_mode,
        )

    st.session_state.current_recommendation = result
    st.session_state.show_recommendations = True


if st.session_state.show_recommendations and st.session_state.current_recommendation:
    st.markdown("---")
    st.markdown("### Best Cards for This Purchase")

    result = st.session_state.current_recommendation

    if "per_txn" in result and result["per_txn"]:
        txn_data = result["per_txn"][0]
        st.session_state.latest_txn_data = txn_data

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.metric("Category", txn_data["predicted_category"])
        with col2:
            st.metric("MCC", txn_data["predicted_mcc"])
        with col3:
            st.metric("Confidence", f"{txn_data['confidence'] * 100:.0f}%")

        st.markdown("---")

        recommendations = txn_data["explain"].get("recommendations", [])

        for idx, rec in enumerate(recommendations[:3]):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

                with col1:
                    rank_badge = ["🥇", "🥈", "🥉"][idx]
                    st.markdown(f"### {rank_badge} {rec['card']}")
                    st.caption(rec.get("bank", "Card issuer"))

                with col2:
                    reward_value = rec["reward"]
                    reward_pct = (reward_value / amount) * 100 if amount else 0
                    st.metric("Reward Value", f"${reward_value:.2f}")
                    st.progress(min(reward_pct / 5, 1.0))

                with col3:
                    st.markdown("**Details**")
                    st.caption(rec.get("calc_trace", "Reward calculation unavailable"))

                with col4:
                    if st.button(f"Why", key=f"why_{idx}"):
                        st.info(rec.get("matched_rule", "Standard reward rate"))

                    if idx == 0:
                        if st.button("Use this card", key=f"use_{idx}", type="primary"):
                            st.session_state.show_apple_pay = True
                            st.session_state.selected_card = rec


if st.session_state.show_apple_pay and st.session_state.selected_card:
    txn_context = st.session_state.get("latest_txn_data")
    input_context = st.session_state.get("last_transaction_input", {})

    if not txn_context or not input_context:
        st.warning("Transaction context not available. Please generate recommendations again.")
    else:
        st.markdown("---")
        st.markdown("### Confirm Payment")

        amount_value = input_context.get("amount", 0.0)
        currency_code = input_context.get("currency", "SGD")
        merchant_name = input_context.get("merchant", "Merchant")
        location_value = input_context.get("location", {})

        selected = st.session_state.selected_card
        card_last4 = selected.get("last4") or "0000"

        card_container = st.container()
        with card_container:
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                st.markdown(
                    f"""
                    <div style="
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 15px;
                        padding: 30px;
                        text-align: center;
                        color: white;
                        margin: 20px 0;
                    ">
                        <h2>{selected['card']}</h2>
                        <p>**** **** **** {card_last4}</p>
                        <h3>${amount_value:.2f} {currency_code}</h3>
                        <p>{merchant_name}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(
                    """
                    <div style="text-align: center; margin: 20px 0;">
                        <p>Face ID</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button("Confirm Payment", use_container_width=True, type="primary"):
                    with st.spinner("Processing..."):
                        time.sleep(1.5)

                    transaction = {
                        "timestamp": datetime.now().isoformat(),
                        "merchant": merchant_name,
                        "amount": amount_value,
                        "currency": currency_code,
                        "card_used": selected["card"],
                        "reward": selected["reward"],
                        "category": txn_context["predicted_category"],
                        "location": location_value,
                    }
                    st.session_state.transaction_history.append(transaction)

                    card_id = selected.get("card_id")
                    for card in st.session_state.user_cards:
                        if card.get("id") == card_id or card.get("display_name") == selected["card"]:
                            current_used = card.get("used_this_month", 0) or 0
                            card["used_this_month"] = float(current_used) + selected["reward"]
                            break

                    st.balloons()
                    st.success(f"Payment successful! Earned ${selected['reward']:.2f} in rewards")

                    st.session_state.show_apple_pay = False
                    st.session_state.show_recommendations = False
                    st.session_state.selected_card = None

                    if st.button("View Transaction History"):
                        st.switch_page("pages/1_Home.py")


with st.sidebar:
    st.markdown("### Quick Examples")

    examples = [
        {"name": "Din Tai Fung", "amount": 58.20, "location": "Orchard"},
        {"name": "Starbucks", "amount": 12.50, "location": "CBD"},
        {"name": "FairPrice", "amount": 145.30, "location": "Tampines"},
        {"name": "Grab", "amount": 23.40, "location": "Current"},
    ]

    for ex in examples:
        if st.button(f"{ex['name']} (${ex['amount']})"):
            st.session_state.prefill = ex
            st.rerun()
