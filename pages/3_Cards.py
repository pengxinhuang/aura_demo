"""
Cards Management Page
Display user's credit cards and usage
"""

import streamlit as st


st.set_page_config(page_title="AURA - My Cards", page_icon="💳", layout="wide")

st.title("💳 My Cards")
st.subheader("Manage your credit card wallet")


def _get_amount(card_dict, key) -> float:
    value = card_dict.get(key, 0) or 0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


if st.session_state.user_cards:
    for card in st.session_state.user_cards:
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

            with col1:
                st.markdown(f"### {card['display_name']}")
                st.caption(f"{card['bank']} **** {card.get('last4', '0000')}")

            with col2:
                reward_earned = _get_amount(card, "used_this_month")
                reward_cap = max(_get_amount(card, "monthly_cap"), 0)
                usage_ratio = min(reward_earned / reward_cap, 1.0) if reward_cap else 0.0

                st.metric("Rewards Earned", f"${reward_earned:.2f} / ${reward_cap:.2f}")
                st.progress(usage_ratio)

            with col3:
                st.markdown("**Key Benefits**")
                for benefit in card.get("benefits", [])[:2]:
                    st.caption(f"- {benefit}")

            with col4:
                is_preferred = card.get("id") == st.session_state.get("preferred_card")
                if st.checkbox("Preferred", value=is_preferred, key=f"pref_{card['id']}"):
                    st.session_state.preferred_card = card["id"]

        st.divider()
else:
    st.info("No cards in your wallet yet. Add one below to get started.")


st.markdown("### Add New Card")

with st.expander("Add a credit card"):
    with st.form("add_card_form"):
        col1, col2 = st.columns(2)

        with col1:
            bank = st.selectbox("Bank", ["DBS", "OCBC", "UOB", "Citibank", "StanChart"])
            card_name = st.text_input("Card Name", placeholder="e.g., Rewards Plus")

        with col2:
            last4 = st.text_input("Last 4 digits", max_chars=4)
            monthly_cap = st.number_input("Monthly Reward Cap ($)", min_value=0.0, value=500.0, step=50.0)

        if st.form_submit_button("Add Card"):
            new_card = {
                "id": f"card_{len(st.session_state.user_cards) + 1}",
                "bank": bank,
                "display_name": card_name,
                "last4": last4,
                "monthly_cap": monthly_cap,
                "used_this_month": 0.0,
                "benefits": ["General cashback"],
            }
            st.session_state.user_cards.append(new_card)
            st.success(f"Added {card_name} to your wallet!")
            st.rerun()


st.markdown("### 📊 Wallet Summary")

col1, col2, col3 = st.columns(3)

total_limit = sum(_get_amount(card, "monthly_cap") for card in st.session_state.user_cards)
total_used = sum(_get_amount(card, "used_this_month") for card in st.session_state.user_cards)

with col1:
    st.metric("Total Cards", len(st.session_state.user_cards))
with col2:
    st.metric("Monthly Reward Cap", f"${total_limit:.2f}")
with col3:
    st.metric("Reward Remaining", f"${max(total_limit - total_used, 0):.2f}")
