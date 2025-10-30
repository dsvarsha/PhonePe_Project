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
    - remove NULL or total rows
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
        .str.title()
    )

    # Drop null or total rows
    df = df[~df[state_col].str.lower().isin(["null", "none", "nan", "total", "total (india)"])]
    df = df[df[state_col] != ""]

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

    df.dropna(subset=["state"], inplace=True)
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
    an interactive platform visualizing key insights from the PhonePe Pulse dataset.

    **Key Features:**
    - ETL Process: JSON → MySQL → CSV → Streamlit
    - Analysis on Transactions, Users, and Insurance
    - Business insights and case studies integrated
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/f2/PhonePe_Logo.png", width=250)
    st.success("💡 Use the sidebar to explore different analytical sections.")

# ---------------------------------------------------------------
# 1️⃣ TRANSACTION DYNAMICS
# ---------------------------------------------------------------
elif menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = data["txn_state"].copy()
    df_cat = data["txn_category"].copy()

    fig1 = px.bar(
        df_state.sort_values("total_amount", ascending=False).head(10),
        x="state",
        y="total_amount",
        color="total_amount",
        title="Top 10 States by Transaction Value (₹ in Crores)",
        text_auto=".2s"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Detect category/value columns
    cat_cols = [c.lower() for c in df_cat.columns]
    name_col = next((c for c in ["category", "name", "payment_category"] if c in cat_cols), df_cat.columns[0])
    value_col = next((c for c in ["total_amount", "total_value_in_crores", "total_value", "total_in_crores"] if c in cat_cols), None)

    if value_col:
        fig2 = px.pie(df_cat, values=value_col, names=name_col, title="Transaction Split by Category")
        st.plotly_chart(fig2, use_container_width=True)

    top_state = df_state.loc[df_state["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} recorded the highest transaction value — ₹{top_state['total_amount']:.2f} Cr."
    )

# ---------------------------------------------------------------
# 2️⃣ DEVICE DOMINANCE
# ---------------------------------------------------------------
elif menu == "2️⃣ Device Dominance":
    st.title("📱 Device Dominance and User Engagement")

    df_user = data["user_device"].copy()
    if "registered_users" in df_user.columns:
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
            f"📊 **Insight:** {top_state['state']} has the highest number of registered users — {int(top_state['registered_users']):,}."
        )
    else:
        st.warning("⚠️ Registered user data not found.")

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
        f"💡 **Insight:** {top_state['state']} leads insurance penetration with ₹{top_state['total_amount']:.2f} Cr "
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
        f"🚀 **Insight:** {top_district['district']} shows the strongest market expansion potential."
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
            f"💡 **Insight:** {top_state['state']} shows the highest engagement ratio — {top_state['engagement_ratio']:.2f}%."
        )
    else:
        st.error("⚠️ Missing 'registered_users' or 'app_opens' column in user data.")

# ---------------------------------------------------------------
# 🧠 INSIGHTS SUMMARY
# ---------------------------------------------------------------
elif menu == "🧠 Insights Summary":
    st.title("🧠 Insights Summary & Business Analysis")
    st.markdown("---")

    st.subheader("📈 Transaction Dynamics")
    st.markdown("""
    - Karnataka and Maharashtra lead in transaction value.  
    - Utility payments dominate digital transactions.
    """)

    st.subheader("📱 Device Dominance")
    st.markdown("""
    - Maharashtra and Uttar Pradesh have the most registered users.  
    - Majority of users are on Android devices.
    """)

    st.subheader("🧾 Insurance Penetration")
    st.markdown("""
    - Tamil Nadu and Karnataka show highest insurance adoption.  
    - Indicates strong digital finance trust.
    """)

    st.subheader("🌍 Market Expansion")
    st.markdown("""
    - Tier-2 and Tier-3 districts show growth potential.  
    - Market expansion beyond metros increasing.
    """)

    st.subheader("👥 User Engagement")
    st.markdown("""
    - Strong engagement in urban states like Karnataka and Maharashtra.  
    - Consistent app opens reflect user loyalty.
    """)

    st.success("💬 Summary: The dashboard reveals regional strengths, device trends, and engagement opportunities for PhonePe’s market growth.")

# ---------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------
st.markdown("---")
st.caption("© 2025 | PhonePe Business Analytics Dashboard | Developed by Varsha Sureshkumar 💜")
