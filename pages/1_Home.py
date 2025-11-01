"""
Home Dashboard Page
Shows overview and quick stats
"""

import pandas as pd
import streamlit as st


if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []
if "user_cards" not in st.session_state:
    st.session_state.user_cards = []


st.set_page_config(page_title="AURA - Home", page_icon="🏠", layout="wide")

st.title("🏠 Dashboard")
st.subheader("Your Rewards Overview")


if not st.session_state.transaction_history:
    st.info("No transactions yet. Start optimizing your rewards!")
else:
    st.markdown("### Recent Transactions")

    df = pd.DataFrame(st.session_state.transaction_history)

    for txn in df.head(5).to_dict("records"):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            with col1:
                st.text(f"{txn['merchant']}")
            with col2:
                st.text(f"{txn.get('card_used', 'N/A')}")
            with col3:
                st.text(f"${txn['amount']:.2f}")
            with col4:
                st.text(f"+${txn.get('reward', 0):.2f}")


st.markdown("### This Month")

col1, col2, col3 = st.columns(3)

monthly_spend = sum(t.get("amount", 0) for t in st.session_state.transaction_history)
monthly_rewards = sum(t.get("reward", 0) for t in st.session_state.transaction_history)

with col1:
    st.metric("Total Spend", f"${monthly_spend:.2f}")

with col2:
    st.metric("Rewards Earned", f"${monthly_rewards:.2f}")

with col3:
    reward_rate = (monthly_rewards / monthly_spend) * 100 if monthly_spend else 0
    st.metric("Effective Rate", f"{reward_rate:.1f}%")


st.markdown("### Insights")

insights = [
    "You are earning 2.3% average cashback",
    "DBS Altitude has $200 remaining in the dining reward cap",
    "Consider using UOB One for groceries (5% back)",
    "You are 2,340 miles away from your next free flight",
]

for insight in insights:
    st.info(insight)


st.markdown("---")
if st.button("Add Transaction"):
    st.switch_page("pages/2_Transactions.py")
