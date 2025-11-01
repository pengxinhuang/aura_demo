"""
AURA: Adaptive User Rewards Agent
Main Streamlit App Entry Point
"""

import json
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="AURA Wallet",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "AURA - Smart Credit Card Rewards System"},
)


if "mock_mode" not in st.session_state:
    st.session_state.mock_mode = True
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []
if "user_cards" not in st.session_state:
    st.session_state.user_cards = []
if "selected_card" not in st.session_state:
    st.session_state.selected_card = None


@st.cache_data
def load_mock_data():
    data_path = Path("data")

    with open(data_path / "mock_user_cards.json", "r", encoding="utf-8") as f:
        cards = json.load(f)

    with open(data_path / "mock_transactions.json", "r", encoding="utf-8") as f:
        transactions = json.load(f)

    return cards, transactions


if not st.session_state.user_cards:
    cards, transactions = load_mock_data()
    st.session_state.user_cards = cards
    st.session_state.sample_transactions = transactions


with st.sidebar:
    st.title("⚙️ Settings")

    mode = st.toggle(
        "Live Mode",
        value=not st.session_state.mock_mode,
        help="Toggle between mock data and live API calls",
    )
    st.session_state.mock_mode = not mode

    if st.session_state.mock_mode:
        st.info("Using mock data")
    else:
        st.warning("Live mode (agents not connected)")

    st.divider()
    st.caption("Use the navigation to explore other pages")


st.title("🎯 AURA Wallet")
st.subheader("Adaptive User Rewards Agent")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Active Cards", len(st.session_state.user_cards), help="Cards in your wallet")

with col2:
    total_rewards = sum(t.get("reward", 0) for t in st.session_state.transaction_history)
    st.metric("Total Rewards", f"${total_rewards:.2f}", help="Cashback earned to date")

with col3:
    st.metric(
        "Transactions",
        len(st.session_state.transaction_history),
        help="Optimized transactions processed",
    )


st.markdown("---")
st.markdown(
    """
### Welcome to AURA

Your intelligent credit card companion that helps you:
- **Maximize rewards** on every purchase
- **Deliver location-aware** recommendations
- **Track spending** and reward caps
- **Offer smart insights** for better decisions

Start by exploring the **Transactions** page to run a recommendation.
"""
)


st.markdown("### Quick Actions")
col1, col2 = st.columns(2)

with col1:
    if st.button("New Transaction", use_container_width=True):
        st.switch_page("pages/2_Transactions.py")

with col2:
    if st.button("My Cards", use_container_width=True):
        st.switch_page("pages/3_Cards.py")


st.markdown("---")
st.caption("AURA v1.0 - SMU IS625 Group 11 | Mock Demo")
