# ---------------------------------------------------------------
# 📊 PHONEPE BUSINESS ANALYTICS DASHBOARD
# Developed by: Varsha Sureshkumar 💜
# ---------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------- Data cleaning helper ----------
def clean_state_df(df):
    """
    Normalize and clean DataFrame with a state column and numeric columns.
    - lowercase column names
    - find and standardize state column to 'state'
    - strip quotes/spaces, convert 'NULL' to NaN and drop NULL states
    - standardize numeric column names and convert to numeric types
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # identify state column (common candidates)
    state_candidates = ["state", "entityname", "state name", "statename"]
    state_col = None
    for c in state_candidates:
        if c in df.columns:
            state_col = c
            break
    if state_col is None:
        state_col = df.columns[0]   # fallback to first column

    # normalize state text
    df[state_col] = df[state_col].astype(str).str.replace('"', '', regex=False).str.strip()
    df[state_col] = df[state_col].replace({"": pd.NA, "null": pd.NA, "none": pd.NA})

    # rename to 'state'
    if state_col != "state":
        df.rename(columns={state_col: "state"}, inplace=True)

    # common renames for numeric/value cols
    rename_map = {
        "total_value_in_crores": "total_amount",
        "total_in_crores": "total_amount",
        "total_value": "total_amount",
        "total_policies": "policy_count",
        "total_count": "count",
        "totalcount": "count",
        "registered_users_": "registered_users",
        "registereduser": "registered_users"
    }
    for k, v in rename_map.items():
        if k in df.columns and v not in df.columns:
            df.rename(columns={k: v}, inplace=True)

    # convert numeric cols to numeric dtype (coerce bad values to NaN)
    for col in ["total_amount", "policy_count", "count", "registered_users"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # drop rows where state is missing
    df = df.dropna(subset=["state"])

    # If total_amount exists, drop rows missing it (we can't compute top without value)
    if "total_amount" in df.columns:
        df = df.dropna(subset=["total_amount"])

    return df
# ---------- end helper ----------


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

# ---------- GLOBAL CLEANING FIX ----------
for key, df in data.items():
    df = clean_state_df(df)
    data[key] = df
# -----------------------------------------

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

    if not df_state.empty:
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

    if not df_user.empty and y_col in df_user.columns:
        top_state = df_user.loc[df_user[y_col].idxmax()]
        state_name = top_state.get(x_col, "Unknown")
        user_count = top_state.get(y_col, 0)
        st.info(
            f"📊 **Insight:** {state_name} has the highest number of PhonePe users — {int(user_count):,} total users."
        )
    else:
        st.warning("No valid user data available after cleaning.")

# ---------------------------------------------------------------
# 3️⃣ INSURANCE PENETRATION
# ---------------------------------------------------------------
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = data["insurance_state"].copy()
    df_ins = clean_state_df(df_ins)

    if "state" in df_ins.columns and "total_amount" in df_ins.columns:
        df_plot = df_ins.sort_values("total_amount", ascending=False).head(10)
        fig = px.bar(
            df_plot,
            x="state",
            y="total_amount",
            color="total_amount",
            title="Top 10 States by Insurance Premium Value (₹ in Crores)",
            text_auto=".2s"
        )
        st.plotly_chart(fig, use_container_width=True)

        if not df_ins.empty:
            top_state = df_ins.loc[df_ins["total_amount"].idxmax()]
            state_name = top_state.get("state", "Unknown")
            amount_val = top_state.get("total_amount", 0)
            policy_val = top_state.get("policy_count", "N/A")
            st.success(
                f"💡 **Insight:** {state_name} recorded the highest insurance value at ₹{amount_val:.2f} Cr "
                f"with {policy_val} total policies."
            )
    else:
        st.warning("No valid insurance data available after cleaning.")

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

    if not df_dist.empty:
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

        if not df_user.empty:
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
