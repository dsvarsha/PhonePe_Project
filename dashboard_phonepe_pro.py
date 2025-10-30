# ---------------------------------------------------------------
# 📊 PHONEPE BUSINESS ANALYTICS DASHBOARD
# Developed by: Varsha Sureshkumar 💜
# ---------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------------------------------------
# 🧹 UNIVERSAL CLEANING FUNCTION
# ---------------------------------------------------------------
def clean_state_df(df):
    """
    Normalize and clean DataFrame with a state column and numeric columns.
    - standardize column names
    - replace NULL/NaN with 'Total (India)'
    - rename numeric columns (total_value_in_crores → total_amount)
    """
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Identify state column
    state_candidates = ["state", "entityname", "state name", "statename"]
    state_col = next((c for c in state_candidates if c in df.columns), df.columns[0])

    # Normalize text
    df[state_col] = (
        df[state_col]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.strip()
        .str.lower()
    )

    # Replace null/empty with "Total (India)"
    df[state_col] = df[state_col].replace(
        {"": "total (india)", "null": "total (india)", "none": "total (india)", "nan": "total (india)"}
    )

    # Rename to 'state'
    if state_col != "state":
        df.rename(columns={state_col: "state"}, inplace=True)

    # Rename numeric columns
    rename_map = {
        "total_value_in_crores": "total_amount",
        "total_in_crores": "total_amount",
        "total_value": "total_amount",
        "total_policies": "policy_count",
        "total_count": "count",
        "registered_users_": "registered_users",
        "total_registered_users": "registered_users",
        "registereduser": "registered_users",
        "appopens": "app_opens",
        "total_app_opens": "app_opens"
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    # Convert numerics
    for col in ["total_amount", "policy_count", "count", "registered_users", "app_opens"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# ---------------------------------------------------------------
# ⚙️ PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="PhonePe Business Analytics Dashboard", layout="wide")

# Sidebar header
st.sidebar.title("📊 PhonePe Business Analytics | 2025")
st.sidebar.markdown("**Developed by:** Varsha Sureshkumar 💜")
st.sidebar.markdown("B.E Electronics & Communication | KGiSL Institute of Technology")
st.sidebar.markdown("---")

# ---------------------------------------------------------------
# 📁 LOAD DATASETS
# ---------------------------------------------------------------
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

# Clean all datasets
for key, df in data.items():
    data[key] = clean_state_df(df)

# ---------------------------------------------------------------
# 📋 SIDEBAR MENU
# ---------------------------------------------------------------
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
# 🏠 OVERVIEW
# ---------------------------------------------------------------
if menu == "🏠 Dashboard Overview":
    st.title("📊 PhonePe Business Analytics Dashboard")
    st.markdown("""
    Welcome to the **PhonePe Business Analytics Dashboard** —  
    an interactive data-driven platform to explore insights from PhonePe’s Pulse dataset.

    **Project Highlights:**
    - Automated ETL Pipeline (Python + MySQL)
    - Clean Data Transformation & Visualization
    - Real-time Analysis via Streamlit & Plotly
    - Business Case Studies (Transactions, Devices, Insurance, Expansion, Engagement)
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/f2/PhonePe_Logo.png", width=250)
    st.success("💡 Use the sidebar to explore various sections of the project.")

# ---------------------------------------------------------------
# 1️⃣ TRANSACTION DYNAMICS
# ---------------------------------------------------------------
elif menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = data["txn_state"].copy()
    df_cat = data["txn_category"].copy()

    # Bar chart for Top States
    fig1 = px.bar(
        df_state.sort_values("total_amount", ascending=False).head(10),
        x="state",
        y="total_amount",
        color="total_amount",
        title="Top 10 States by Transaction Value (₹ in Crores)",
        text_auto=".2s"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Detect category and value column
    cat_cols = [c.lower() for c in df_cat.columns]
    name_col = next((c for c in ["category", "name", "payment_category"] if c in cat_cols), df_cat.columns[0])
    value_col = next((c for c in ["total_amount", "total_value_in_crores", "total_value", "total_in_crores"] if c in cat_cols), None)

    if value_col:
        fig2 = px.pie(df_cat, values=value_col, names=name_col, title="Transaction Split by Category")
        st.plotly_chart(fig2, use_container_width=True)

    # Insights
    top_state = df_state.loc[df_state["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state'].title()} leads with ₹{top_state['total_amount']:.2f} Cr in transactions. "
        f"The overall India total is ₹{df_state['total_amount'].sum():.2f} Cr."
    )

# ---------------------------------------------------------------
# 2️⃣ DEVICE DOMINANCE
# ---------------------------------------------------------------
elif menu == "2️⃣ Device Dominance":
    st.title("📱 Device Dominance and User Engagement")

    df_user = data["user_device"].copy()
    if "registered_users" not in df_user.columns:
        st.error("⚠️ No valid user data found.")
    else:
        fig = px.bar(
            df_user.sort_values("registered_users", ascending=False).head(10),
            x="state",
            y="registered_users",
            color="registered_users",
            title="Top 10 States by Registered Users",
            text_auto=".2s"
        )
        st.plotly_chart(fig, use_container_width=True)

        top_state = df_user.loc[df_user["registered_users"].idxmax()]
        st.info(
            f"📊 **Insight:** {top_state['state'].title()} has the highest PhonePe user registrations — {int(top_state['registered_users']):,} users."
        )

# ---------------------------------------------------------------
# 3️⃣ INSURANCE PENETRATION
# ---------------------------------------------------------------
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = data["insurance_state"].copy()
    df_ins = df_ins.sort_values("total_amount", ascending=False)

    fig = px.bar(
        df_ins.head(10),
        x="state",
        y="total_amount",
        color="total_amount",
        title="Top 10 States by Insurance Premium Value (₹ in Crores)",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_ins.loc[df_ins["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state'].title()} leads insurance penetration with ₹{top_state['total_amount']:.2f} Cr "
        f"across {int(top_state['policy_count']):,} total policies."
    )

# ---------------------------------------------------------------
# 4️⃣ MARKET EXPANSION
# ---------------------------------------------------------------
elif menu == "4️⃣ Market Expansion":
    st.title("🌍 Market Expansion and Growth Trends")

    df_dist = data["district_txn"].copy()
    y_col = "total_amount" if "total_amount" in df_dist.columns else "count"

    fig = px.bar(
        df_dist.sort_values(y_col, ascending=False).head(10),
        x="district",
        y=y_col,
        color=y_col,
        title="Top 10 Districts by Transaction Value (₹ in Crores)",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_district = df_dist.loc[df_dist[y_col].idxmax()]
    st.warning(
        f"🚀 **Insight:** {top_district['district'].title()} shows the strongest market expansion potential."
    )

# ---------------------------------------------------------------
# 5️⃣ USER ENGAGEMENT
# ---------------------------------------------------------------
elif menu == "5️⃣ User Engagement":
    st.title("👥 User Engagement and Growth Strategy")

    df_user = data["user_device"].copy()
    if "registered_users" in df_user.columns and "app_opens" in df_user.columns:
        df_user["engagement_ratio"] = (df_user["app_opens"] / df_user["registered_users"]) * 100
        fig = px.line(
            df_user.sort_values("engagement_ratio", ascending=False),
            x="state",
            y="engagement_ratio",
            markers=True,
            title="User Engagement Ratio by State (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

        top_state = df_user.loc[df_user["engagement_ratio"].idxmax()]
        st.info(
            f"💡 **Insight:** {top_state['state'].title()} has the highest engagement ratio at "
            f"{top_state['engagement_ratio']:.2f}%."
        )
    else:
        st.error("⚠️ Missing columns: required 'registered_users' and 'app_opens' for engagement ratio.")

# ---------------------------------------------------------------
# 🧠 INSIGHTS SUMMARY
# ---------------------------------------------------------------
elif menu == "🧠 Insights Summary":
    st.title("🧠 Insights Summary & Business Analysis")
    st.markdown("---")

    st.subheader("📈 Transaction Dynamics")
    st.markdown("""
    - **Total (India)** recorded the highest overall transaction volume.  
    - Karnataka and Maharashtra follow closely in state-level performance.  
    - Utility-based payments like **Recharge & Bill Payments** dominate.
    """)

    st.subheader("📱 Device Dominance")
    st.markdown("""
    - Highest user registrations seen in **Maharashtra**, **Uttar Pradesh**, and **Karnataka**.  
    - Majority users access PhonePe on **Android devices** (Xiaomi, Samsung).  
    - Optimizing app UI for Android ensures wider reach.
    """)

    st.subheader("🧾 Insurance Penetration")
    st.markdown("""
    - Southern states like **Tamil Nadu**, **Karnataka**, and **Andhra Pradesh** dominate insurance adoption.  
    - Indicates higher financial awareness and secure digital payment behavior.  
    - Opportunity to expand in Northern and Eastern regions.
    """)

    st.subheader("🌍 Market Expansion")
    st.markdown("""
    - Tier-2 and Tier-3 cities show fast growth, led by **Bihar** and **Madhya Pradesh**.  
    - Expanding merchant and local partnerships can accelerate penetration.
    """)

    st.subheader("👥 User Engagement")
    st.markdown("""
    - Engagement ratios are highest in high-tech urban regions.  
    - Daily app opens increasing year over year — reflecting user trust.  
    - Reward and cashback programs can enhance retention.
    """)

    st.markdown("---")
    st.success("💬 Summary: The dashboard provides a holistic view of PhonePe’s transaction ecosystem, from usage trends to regional opportunities and growth potential.")

# ---------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------
st.markdown("---")
st.caption("© 2025 | PhonePe Business Analytics Dashboard | Developed by Varsha Sureshkumar 💜")
