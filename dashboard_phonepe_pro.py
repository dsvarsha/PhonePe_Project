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
# ---------------------------------------------------------------
# 1️⃣ TRANSACTION DYNAMICS (Advanced)
# ---------------------------------------------------------------
elif menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = data["txn_state"].copy()
    df_cat = data["txn_category"].copy()

    # Clean & standardize
    for df in [df_state, df_cat]:
        df.columns = df.columns.str.strip().str.lower()

    rename_map = {
        "total_value_in_crores": "total_amount",
        "total_in_crores": "total_amount",
        "total_value": "total_amount",
        "category_name": "category",
        "name": "category"
    }
    df_cat.rename(columns=rename_map, inplace=True)
    df_state.rename(columns=rename_map, inplace=True)

    for col in ["total_amount"]:
        if col in df_cat.columns:
            df_cat[col] = pd.to_numeric(df_cat[col], errors="coerce")
        if col in df_state.columns:
            df_state[col] = pd.to_numeric(df_state[col], errors="coerce")

    df_state = df_state[~df_state["state"].isin(["Total (India)", "Null", "None", "Nan"])]

    # Chart 1 – Top 10 States
    fig1 = px.bar(
        df_state.sort_values("total_amount", ascending=False).head(10),
        x="state", y="total_amount", color="total_amount",
        text_auto=".2s",
        hover_data={"state": True, "total_amount": ":,.2f"},
        title="Top 10 States by Transaction Value (₹ in Crores)"
    )
    fig1.update_traces(marker_line_width=1, marker_line_color="black")
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 – Category Distribution
    if "category" in df_cat.columns and "total_amount" in df_cat.columns:
        total_sum = df_cat["total_amount"].sum()
        df_cat["share_%"] = (df_cat["total_amount"] / total_sum) * 100

        fig2 = px.bar(
            df_cat.sort_values("total_amount", ascending=False),
            x="category", y="total_amount",
            color="share_%", text_auto=".2s",
            hover_data={"share_%": ":.2f"},
            title="Distribution of Transaction Categories (Share %)"
        )
        fig2.update_layout(xaxis_title="Transaction Category", yaxis_title="Total Value (₹ Crores)")
        st.plotly_chart(fig2, use_container_width=True)

        top_cat = df_cat.loc[df_cat["total_amount"].idxmax()]
        st.success(
            f"💡 **Insight:** '{top_cat['category']}' is the most used category, "
            f"contributing {top_cat['share_%']:.2f}% of all transactions nationwide."
        )

    # Summary insight
    top_state = df_state.loc[df_state["total_amount"].idxmax()]
    total_amount_all = df_state["total_amount"].sum()
    share = (top_state["total_amount"] / total_amount_all) * 100

    st.info(
        f"📊 **Insight:** {top_state['state']} contributes ₹{top_state['total_amount']:.2f} Cr "
        f"({share:.2f}% of total India transactions). "
        f"Total across all states: ₹{total_amount_all:,.2f} Cr."
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
# ---------------------------------------------------------------
# 3️⃣ INSURANCE PENETRATION (Advanced)
# ---------------------------------------------------------------
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = data["insurance_state"].copy()
    df_ins.columns = df_ins.columns.str.strip().str.lower()

    rename_map = {
        "total_value_in_crores": "total_amount",
        "total_in_crores": "total_amount",
        "total_value": "total_amount",
        "total_policies": "policy_count",
        "count": "policy_count"
    }
    df_ins.rename(columns=rename_map, inplace=True)

    df_ins["total_amount"] = pd.to_numeric(df_ins["total_amount"], errors="coerce")
    df_ins["policy_count"] = pd.to_numeric(df_ins["policy_count"], errors="coerce")
    df_ins.dropna(subset=["state"], inplace=True)
    df_ins = df_ins[~df_ins["state"].isin(["Total (India)", "Null", "None", "Nan"])]

    # Average policy value
    df_ins["avg_policy_value"] = df_ins["total_amount"] / df_ins["policy_count"]

    # Chart 1 – Top 10 States by Total Premium Value
    fig = px.bar(
        df_ins.sort_values("total_amount", ascending=False).head(10),
        x="state", y="total_amount", color="avg_policy_value",
        text_auto=".2s",
        hover_data={"policy_count": ":,.0f", "avg_policy_value": ":,.2f"},
        title="Top 10 States by Insurance Premium Value (₹ in Crores)"
    )
    fig.update_layout(xaxis_title="State", yaxis_title="Total Insurance Value (₹ Crores)")
    st.plotly_chart(fig, use_container_width=True)

    # Insight 1
    top_state = df_ins.loc[df_ins["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} leads with ₹{top_state['total_amount']:.2f} Cr "
        f"across {int(top_state['policy_count']):,} policies "
        f"(avg ₹{top_state['avg_policy_value']:.2f} per policy)."
    )

    # Chart 2 – Average Policy Value by State
    fig2 = px.bar(
        df_ins.sort_values("avg_policy_value", ascending=False).head(10),
        x="state", y="avg_policy_value",
        color="avg_policy_value", text_auto=".2f",
        title="Average Policy Value by State (₹ per Policy)"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Regional comparison (South vs North)
    southern_states = ["Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh", "Telangana"]
    south_avg = df_ins[df_ins["state"].isin(southern_states)]["total_amount"].mean()
    north_avg = df_ins[~df_ins["state"].isin(southern_states)]["total_amount"].mean()

    diff = ((south_avg - north_avg) / north_avg) * 100
    if diff > 0:
        st.info(
            f"📍 **Regional Insight:** Southern India shows {diff:.2f}% higher insurance penetration than northern states."
        )
    else:
        st.info(
            f"📍 **Regional Insight:** Northern regions slightly outperform southern states in insurance values."
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
