"""
Insights Page
Show spending patterns and recommendations
"""

import pandas as pd
import streamlit as st


st.set_page_config(page_title="AURA - Insights", page_icon="📊", layout="wide")

st.title("📊 Insights & Analytics")
st.subheader("Optimize your reward strategy")


insights_data = {
    "spending_by_category": {
        "Dining": 450.30,
        "Transport": 234.50,
        "Groceries": 567.80,
        "Shopping": 890.20,
        "Entertainment": 123.40,
    },
    "rewards_by_card": {
        "Citi Cash Back+": 45.30,
        "DBS Altitude": 32.10,
        "UOB One": 28.50,
        "OCBC 365": 15.20,
    },
    "optimization_tips": [
        {"tip": "Switch to UOB One for groceries", "potential": 23.40},
        {"tip": "Use DBS Altitude for overseas spending", "potential": 45.00},
        {"tip": "Maximize dining cap with Citi Cash Back+", "potential": 12.30},
    ],
}


st.markdown("### Spending by Category")

df_spending = pd.DataFrame(
    list(insights_data["spending_by_category"].items()),
    columns=["Category", "Amount"],
)

col1, col2 = st.columns([2, 1])

with col1:
    max_value = max(insights_data["spending_by_category"].values())
    for category, amount in insights_data["spending_by_category"].items():
        cols = st.columns([2, 3, 1])
        with cols[0]:
            st.text(category)
        with cols[1]:
            st.progress(amount / max_value if max_value else 0)
        with cols[2]:
            st.text(f"${amount:.2f}")

with col2:
    total_spending = sum(insights_data["spending_by_category"].values())
    st.metric("Total Spending", f"${total_spending:.2f}")
    st.metric("Average per Category", f"${total_spending / len(df_spending):.2f}")


st.divider()
st.markdown("### Rewards Performance")

col1, col2, col3 = st.columns(3)

total_rewards = sum(insights_data["rewards_by_card"].values())
best_card = max(insights_data["rewards_by_card"], key=insights_data["rewards_by_card"].get)

with col1:
    st.metric("Total Rewards", f"${total_rewards:.2f}")
with col2:
    st.metric("Best Performer", best_card)
with col3:
    st.metric("Average Reward Rate", f"{(total_rewards / total_spending) * 100:.1f}%")


st.markdown("### Optimization Opportunities")

total_potential = sum(tip["potential"] for tip in insights_data["optimization_tips"])
st.info(f"You could earn an additional ${total_potential:.2f} per month.")

for tip in insights_data["optimization_tips"]:
    with st.container():
        col1, col2, col3 = st.columns([4, 2, 1])

        with col1:
            st.markdown(f"**{tip['tip']}**")
        with col2:
            st.metric("Potential", f"+${tip['potential']:.2f}", label_visibility="collapsed")
        with col3:
            if st.button("Apply", key=f"apply_{tip['tip'][:10]}"):
                st.success("Tip saved to preferences")


st.markdown("### Monthly Targets")

targets = [
    {"name": "Citi Cash Back+", "target": "$600 dining", "progress": 75},
    {"name": "DBS Altitude", "target": "5,000 miles", "progress": 60},
    {"name": "UOB One", "target": "$500 spend", "progress": 90},
]

for target in targets:
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.text(target["name"])
    with col2:
        st.progress(target["progress"] / 100)
    with col3:
        st.text(f"{target['progress']}%")


st.markdown("### Recommended Actions")

actions = [
    "Enable location services for better recommendations",
    "You are $120 away from the UOB One bonus tier",
    "Consider applying for HSBC Revolution (high dining rewards)",
    "Review your recurring subscriptions for optimization",
]

for action in actions:
    st.info(action)
