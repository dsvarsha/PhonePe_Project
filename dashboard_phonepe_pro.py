# ---------------------------------------------------------------
# 📊 PhonePe Business Analytics Dashboard
# Developed by: Varsha Sureshkumar 💜
# Purpose: Visualize PhonePe Transaction, User, and Insurance Data
# ---------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# 🟣 Streamlit page setup
st.set_page_config(page_title="PhonePe Business Analytics Dashboard", layout="wide")

# 🟣 Sidebar header
st.sidebar.title("📊 PhonePe Business Analytics Dashboard | 2025")
st.sidebar.markdown("**Developed by:** Varsha Sureshkumar 💜")
st.sidebar.markdown("B.E Electronics & Communication | KGiSL Institute of Technology")
st.sidebar.markdown("---")

# 🟣 Load CSVs from analysis_results folder
DATA_DIR = Path(__file__).parent / "analysis_results"

@st.cache_data
def load_csvs():
    return {
        "txn_state": pd.read_csv(DATA_DIR / "top_states_transaction.csv"),
        "txn_category": pd.read_csv(DATA_DIR / "transaction_by_category.csv"),
        "user_device": pd.read_csv(DATA_DIR / "top_states_users.csv"),
        "insurance_state": pd.read_csv(DATA_DIR / "top_states_insurance.csv"),
        "district_txn": pd.read_csv(DATA_DIR / "top_districts_transaction.csv")
    }

data = load_csvs()

# 🟣 Clean & Normalize Column Names
for key, df in data.items():
    df.columns = df.columns.str.strip().str.lower()
    if "total_in_crores" in df.columns:
        df.rename(columns={"total_in_crores": "total_amount"}, inplace=True)
    if "total_count" in df.columns:
        df.rename(columns={"total_count": "count"}, inplace=True)
    if "total_value" in df.columns:
        df.rename(columns={"total_value": "total_amount"}, inplace=True)

# 🟣 Sidebar Menu
menu = st.sidebar.radio(
    "📁 Select Business Case Study",
    [
        "1️⃣ Transaction Dynamics",
        "2️⃣ Device Dominance",
        "3️⃣ Insurance Penetration",
        "4️⃣ Market Expansion",
        "5️⃣ User Engagement"
    ]
)

# ---------------------------------------------------------------
# CASE STUDY 1: Transaction Dynamics
# ---------------------------------------------------------------
if menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = data["txn_state"]
    df_cat = data["txn_category"]

    # Bar Chart — Top States
    fig1 = px.bar(
        df_state,
        x="state",
        y="total_amount",
        color="total_amount",
        title="Top 10 States by Transaction Value (₹ in Crores)",
        text_auto=".2s"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Pie Chart — Categories
    fig2 = px.pie(
        df_cat,
        values="total_amount",
        names="category",
        title="Transaction Split by Category"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 💡 Insights
    top_state = df_state.loc[df_state["total_amount"].idxmax()]
    top_cat = df_cat.loc[df_cat["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} leads all states with a total transaction value of ₹{top_state['total_amount']:.2f} Cr. "
        f"The most popular category overall is **{top_cat['category']}**."
    )

# ---------------------------------------------------------------
# CASE STUDY 2: Device Dominance
# ---------------------------------------------------------------
elif menu == "2️⃣ Device Dominance":
    st.title("📱 Device Dominance and User Engagement")

    df_user = data["user_device"]
    fig = px.bar(
        df_user,
        x="state",
        y="registered_users",
        color="registered_users",
        title="Registered Users by State"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user["registered_users"].idxmax()]
    st.info(
        f"📊 **Insight:** {top_state['state']} has the highest number of registered users on PhonePe "
        f"with {int(top_state['registered_users']):,} total users."
    )

# ---------------------------------------------------------------
# CASE STUDY 3: Insurance Penetration
# ---------------------------------------------------------------
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = data["insurance_state"]
    fig = px.bar(
        df_ins,
        x="state",
        y="total_amount",
        color="total_amount",
        title="Top 10 States by Insurance Premium Value"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_ins.loc[df_ins["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} leads in insurance value with ₹{top_state['total_amount']:.2f} Cr worth of policies sold."
    )

# ---------------------------------------------------------------
# CASE STUDY 4: Market Expansion
# ---------------------------------------------------------------
elif menu == "4️⃣ Market Expansion":
    st.title("🌍 Market Expansion and Growth Trends")

    df_dist = data["district_txn"]
    fig = px.bar(
        df_dist,
        x="district",
        y="total_amount",
        color="total_amount",
        title="Top 10 Districts by Transaction Value (₹ in Crores)"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_district = df_dist.loc[df_dist["total_amount"].idxmax()]
    st.warning(
        f"🚀 **Insight:** {top_district['district']} is the top-performing district, showing strong market expansion potential for PhonePe."
    )

# ---------------------------------------------------------------
# CASE STUDY 5: User Engagement
# ---------------------------------------------------------------
elif menu == "5️⃣ User Engagement":
    st.title("👥 User Engagement and Growth Strategy")

    df_user = data["user_device"]
    df_user["engagement_ratio"] = (
        df_user["registered_users"] / df_user["registered_users"].max()
    ) * 100

    fig = px.line(
        df_user,
        x="state",
        y="engagement_ratio",
        markers=True,
        title="Engagement Ratio by State (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user["engagement_ratio"].idxmax()]
    st.info(
        f"💡 **Insight:** {top_state['state']} shows the highest user engagement ratio "
        f"({top_state['engagement_ratio']:.2f}%), indicating active daily users in this region."
    )

# ---------------------------------------------------------------
# Footer
# ---------------------------------------------------------------
st.markdown("---")
st.caption("© 2025 | PhonePe Business Analytics Dashboard | Created by Varsha Sureshkumar 💜")
