# ---------------------------------------------------------------
# 📊 PHONEPE BUSINESS ANALYTICS DASHBOARD
# Developed by: Varsha Sureshkumar 💜
# ---------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------- PAGE CONFIG ----------------------------
st.set_page_config(page_title="PhonePe Business Analytics Dashboard", layout="wide")

# ---------------------- SIDEBAR HEADER --------------------------
st.sidebar.title("📊 PhonePe Business Analytics | 2025")
st.sidebar.markdown("**Developed by:** Varsha Sureshkumar 💜")
st.sidebar.markdown("B.E Electronics & Communication | KGiSL Institute of Technology")
st.sidebar.markdown("---")

# ---------------------- DATA LOADING ----------------------------
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

# ---------------------- CLEAN COLUMN NAMES ----------------------
for key, df in data.items():
    df.columns = df.columns.str.strip().str.lower()
    rename_map = {
        "total_in_crores": "total_amount",
        "total_value": "total_amount",
        "total_count": "count",
        "totalcount": "count",
        "registereduser": "registered_users",
        "registered_users_": "registered_users",
        "total_registered_users": "registered_users"
    }
    df.rename(columns=rename_map, inplace=True)
    data[key] = df

# ---------------------- SIDEBAR MENU ----------------------------
menu = st.sidebar.radio(
    "📁 Select Section",
    [
        "🏠 Dashboard Overview",
        "1️⃣ Transaction Dynamics",
        "2️⃣ Device Dominance",
        "3️⃣ Insurance Penetration",
        "4️⃣ Market Expansion",
        "5️⃣ User Engagement",
        "🧠 Insights Summary"
    ]
)

# ---------------------------------------------------------------
# 🏠 HOME PAGE
# ---------------------------------------------------------------
if menu == "🏠 Dashboard Overview":
    st.title("📊 PhonePe Business Analytics Dashboard")
    st.markdown("""
    This dashboard presents an in-depth **data analysis of PhonePe Pulse transactions** across India.  
    It demonstrates a complete data pipeline — from JSON extraction to MySQL integration,  
    CSV generation, and final interactive visualization using **Streamlit** & **Plotly**.

    **Key Focus Areas:**
    - Transaction Trends & Payment Categories  
    - Device-Based User Insights  
    - Insurance Growth Analysis  
    - Regional Market Expansion  
    - User Engagement Ratios  

    Use the left sidebar to explore each section.
    """)

    st.image("https://upload.wikimedia.org/wikipedia/commons/f/f2/PhonePe_Logo.png", width=250)
    st.success("💡 Tip: Click on any section in the sidebar to view detailed visualizations and insights.")

# ---------------------------------------------------------------
# 1️⃣ TRANSACTION DYNAMICS
# ---------------------------------------------------------------
elif menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = data["txn_state"]
    df_cat = data["txn_category"]

    fig1 = px.bar(df_state, x="state", y="total_amount", color="total_amount",
                  title="Top 10 States by Transaction Value (₹ in Crores)", text_auto=".2s")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(df_cat, values="total_amount", names="category",
                  title="Transaction Split by Category")
    st.plotly_chart(fig2, use_container_width=True)

    top_state = df_state.loc[df_state["total_amount"].idxmax()]
    top_cat = df_cat.loc[df_cat["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} leads all states with ₹{top_state['total_amount']:.2f} Cr in transactions. "
        f"The most used category is **{top_cat['category']}**."
    )

# ---------------------------------------------------------------
# 2️⃣ DEVICE DOMINANCE
# ---------------------------------------------------------------
elif menu == "2️⃣ Device Dominance":
    st.title("📱 Device Dominance and User Engagement")

    df_user = data["user_device"]
    x_col = "state" if "state" in df_user.columns else df_user.columns[0]
    y_col = "registered_users" if "registered_users" in df_user.columns else "count"

    fig = px.bar(df_user, x=x_col, y=y_col, color=y_col,
                 title="Registered Users by State", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user[y_col].idxmax()]
    st.info(
        f"📊 **Insight:** {top_state[x_col]} has the highest number of PhonePe users — {int(top_state[y_col]):,} total users."
    )

# ---------------------------------------------------------------
# 3️⃣ INSURANCE PENETRATION
# ---------------------------------------------------------------
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = data["insurance_state"]
    y_col = "total_amount" if "total_amount" in df_ins.columns else "count"

    fig = px.bar(df_ins, x="state", y=y_col, color=y_col,
                 title="Top States by Insurance Premium Value (₹ in Crores)", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_ins.loc[df_ins[y_col].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} leads in insurance premium value with ₹{top_state[y_col]:.2f} Cr."
    )

# ---------------------------------------------------------------
# 4️⃣ MARKET EXPANSION
# ---------------------------------------------------------------
elif menu == "4️⃣ Market Expansion":
    st.title("🌍 Market Expansion and Growth Trends")

    df_dist = data["district_txn"]
    y_col = "total_amount" if "total_amount" in df_dist.columns else "count"

    fig = px.bar(df_dist, x="district", y=y_col, color=y_col,
                 title="Top 10 Districts by Transaction Value (₹ in Crores)", text_auto=".2s")
    st.plotly_chart(fig, use_container_width=True)

    top_district = df_dist.loc[df_dist[y_col].idxmax()]
    st.warning(
        f"🚀 **Insight:** {top_district['district']} is the top-performing district, showing strong market expansion potential."
    )

# ---------------------------------------------------------------
# 5️⃣ USER ENGAGEMENT
# ---------------------------------------------------------------
elif menu == "5️⃣ User Engagement":
    st.title("👥 User Engagement and Growth Strategy")

    df_user = data["user_device"]
    if "registered_users" in df_user.columns:
        df_user["engagement_ratio"] = (df_user["registered_users"] / df_user["registered_users"].max()) * 100
        fig = px.line(df_user, x="state", y="engagement_ratio", markers=True,
                      title="User Engagement Ratio by State (%)")
        st.plotly_chart(fig, use_container_width=True)

        top_state = df_user.loc[df_user["engagement_ratio"].idxmax()]
        st.info(
            f"💡 **Insight:** {top_state['state']} shows the highest engagement ratio "
            f"({top_state['engagement_ratio']:.2f}%), indicating highly active users."
        )
    else:
        st.error("⚠️ Missing 'registered_users' column in user data CSV.")

# ---------------------------------------------------------------
# 🧠 INSIGHTS SUMMARY PAGE
# ---------------------------------------------------------------
elif menu == "🧠 Insights Summary":
    st.title("🧠 Insights Summary & Business Analysis")
    st.markdown("---")

    st.subheader("📈 Transaction Dynamics")
    st.markdown("""
    - Karnataka, Maharashtra, and Tamil Nadu lead with the highest transaction values.  
    - **Recharge & Bill Payments** and **Peer-to-Peer Transfers** dominate usage.  
    - Suggests strong adoption in utility-based digital payments.
    """)

    st.subheader("📱 Device Dominance")
    st.markdown("""
    - Most active users access PhonePe on **Xiaomi** and **Samsung** devices.  
    - Majority of user base is Android, mid-range device segment.  
    - UI optimization for Android devices can enhance engagement.
    """)

    st.subheader("🧾 Insurance Penetration")
    st.markdown("""
    - Insurance adoption is strongest in Southern India (Karnataka, Andhra Pradesh, Tamil Nadu).  
    - Indicates higher financial awareness and product acceptance.  
    - Expansion opportunity in Northern & Eastern states.
    """)

    st.subheader("🌍 Market Expansion")
    st.markdown("""
    - Rapid growth seen in Tier-2 & Tier-3 cities like Bihar and Madhya Pradesh.  
    - Non-metro adoption shows potential for merchant onboarding programs.
    """)

    st.subheader("👥 User Engagement")
    st.markdown("""
    - Metro states show high engagement, while Tier-2 states are catching up quickly.  
    - Growth in daily app opens reflects increasing trust and retention.  
    - Introduce reward programs for consistent daily usage.
    """)

    st.markdown("---")
    st.success("💬 These insights highlight regional opportunities, device-specific optimizations, and engagement strategies for expanding PhonePe’s market presence.")

# ---------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------
st.markdown("---")
st.caption("© 2025 | PhonePe Business Analytics Dashboard | Developed by Varsha Sureshkumar 💜")
