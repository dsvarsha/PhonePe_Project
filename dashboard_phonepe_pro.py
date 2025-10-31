# ---------------------------------------------------------------
# 📊 PHONEPE BUSINESS ANALYTICS DASHBOARD
# Developed by: Varsha Sureshkumar 💜
# ---------------------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------------------------------------
# 📂 PATH CONFIGURATION
# ---------------------------------------------------------------
DATA_DIR = Path(r"C:\PhonePe_Project\analysis_results")

# ---------------------------------------------------------------
# 🧹 HELPER FUNCTION TO CLEAN DATAFRAMES
# ---------------------------------------------------------------
def clean_state_df(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # Identify and rename state column
    state_candidates = ["state", "entityname", "state name", "statename"]
    state_col = next((c for c in state_candidates if c in df.columns), df.columns[0])
    df.rename(columns={state_col: "state"}, inplace=True)

    # Normalize text
    df["state"] = df["state"].astype(str).str.replace('"', '').str.strip()
    df["state"].replace({"": pd.NA, "null": pd.NA, "none": pd.NA, "nan": pd.NA}, inplace=True)
    df.dropna(subset=["state"], inplace=True)

    # Rename common numeric columns
    rename_map = {
        "total_value_in_crores": "total_amount",
        "total_in_crores": "total_amount",
        "total_value": "total_amount",
        "total_policies": "policy_count",
        "total_count": "count",
        "registered_users_": "registered_users",
        "total_registered_users": "registered_users"
    }
    df.rename(columns=rename_map, inplace=True)

    # Convert numeric columns
    for col in ["total_amount", "policy_count", "count", "registered_users"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(subset=["state"], inplace=True)
    return df


# ---------------------------------------------------------------
# 🖥️ PAGE SETUP
# ---------------------------------------------------------------
st.set_page_config(page_title="PhonePe Business Analytics Dashboard", layout="wide")

# Sidebar
st.sidebar.title("📊 PhonePe Business Analytics | 2025")
st.sidebar.markdown("**Developed by:** Varsha Sureshkumar 💜")
st.sidebar.markdown("B.E Electronics & Communication | KGiSL Institute of Technology")
st.sidebar.markdown("---")

# ---------------------------------------------------------------
# 📥 LOAD CSV FILES
# ---------------------------------------------------------------
@st.cache_data
def load_csvs():
    files = {
        "txn_state": "top_states_transaction.csv",
        "txn_category": "transaction_by_category.csv",
        "user_device": "top_states_users.csv",
        "insurance_state": "top_states_insurance.csv",
        "district_txn": "top_districts_transaction.csv"
    }
    data = {}
    for key, filename in files.items():
        path = DATA_DIR / filename
        if path.exists():
            data[key] = pd.read_csv(path)
        else:
            st.warning(f"⚠️ File missing: {filename}")
            data[key] = pd.DataFrame()
    return data

data = load_csvs()

# ---------------------------------------------------------------
# 📍 MENU NAVIGATION
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
    This dashboard presents an in-depth **data analysis of PhonePe Pulse transactions** across India.  
    It demonstrates a full data pipeline — from **ETL (Extract, Transform, Load)** to **visualization** using Streamlit and Plotly.

    **Modules covered:**
    - Transaction Dynamics  
    - Device & User Insights  
    - Insurance Penetration  
    - Market Expansion  
    - User Engagement  
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/f2/PhonePe_Logo.png", width=250)
    st.success("💡 Use the sidebar to explore each section.")

# ---------------------------------------------------------------
# 1️⃣ TRANSACTION DYNAMICS
# ---------------------------------------------------------------
elif menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = clean_state_df(data["txn_state"])
    df_cat = data["txn_category"].copy()

    if "category" in df_cat.columns:
        df_cat.rename(columns={"category": "payment_category"}, inplace=True)

    # Chart 1 – Top 10 States
    fig1 = px.bar(df_state.sort_values("total_amount", ascending=False).head(10),
                  x="state", y="total_amount", color="total_amount",
                  text_auto=".2s",
                  title="Top 10 States by Transaction Value (₹ Crores)")
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 – Category Split (if available)
    if "payment_category" in df_cat.columns:
        fig2 = px.pie(df_cat, names="payment_category", values="total_amount",
                      title="Transaction Share by Payment Category")
        st.plotly_chart(fig2, use_container_width=True)

    # Insight
    st.success(
        "💡 **Insight:** Karnataka, Maharashtra, and Tamil Nadu dominate in total transaction value. "
        "Recharge & Bill Payments are the most used payment category nationwide."
    )

# ---------------------------------------------------------------
# 2️⃣ DEVICE DOMINANCE
# ---------------------------------------------------------------
elif menu == "2️⃣ Device Dominance":
    st.title("📱 Device Dominance and User Engagement")

    df_user = clean_state_df(data["user_device"])
    fig = px.bar(df_user, x="state", y="registered_users", color="registered_users",
                 text_auto=".2s",
                 title="Registered Users by State (in millions)")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user["registered_users"].idxmax()]
    st.info(f"📊 **Insight:** {top_state['state']} has the highest number of PhonePe users "
            f"with {int(top_state['registered_users']):,} registered accounts.")

# ---------------------------------------------------------------
# 3️⃣ INSURANCE PENETRATION
# ---------------------------------------------------------------
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = clean_state_df(data["insurance_state"])
    df_ins["avg_policy_value"] = df_ins["total_amount"] / df_ins["policy_count"]

    fig = px.bar(df_ins.sort_values("total_amount", ascending=False).head(10),
                 x="state", y="total_amount", color="avg_policy_value",
                 text_auto=".2s",
                 title="Top 10 States by Total Insurance Value (₹ Crores)")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_ins.loc[df_ins["total_amount"].idxmax()]
    st.success(
        f"💡 **Insight:** {top_state['state']} recorded the highest insurance value — ₹{top_state['total_amount']:.2f} Cr "
        f"across {int(top_state['policy_count']):,} policies (Avg ₹{top_state['avg_policy_value']:.2f} per policy)."
    )

# ---------------------------------------------------------------
# 4️⃣ MARKET EXPANSION
# ---------------------------------------------------------------
elif menu == "4️⃣ Market Expansion":
    st.title("🌍 Market Expansion Across India")

    df_dist = clean_state_df(data["district_txn"])

    # Chart – Top 10 Districts
    fig = px.bar(
        df_dist.sort_values("total_amount", ascending=False).head(10),
        x="district", y="total_amount", color="total_amount", text_auto=".2s",
        title="Top 10 Districts by Transaction Value (₹ Crores)"
    )
    st.plotly_chart(fig, use_container_width=True)

    top_district = df_dist.loc[df_dist["total_amount"].idxmax()]
    st.success(
        f"🚀 **Insight:** {top_district['district']} (in {top_district['state']}) leads with ₹{top_district['total_amount']:.2f} Cr "
        "in transaction value, showing strong market growth potential."
    )

    st.info(
        "💡 **Business Insight:** Tier-2 cities like Coimbatore and Vizag are emerging as high-growth zones, "
        "indicating strong adoption beyond metros."
    )

# ---------------------------------------------------------------
# 5️⃣ USER ENGAGEMENT
# ---------------------------------------------------------------
elif menu == "5️⃣ User Engagement":
    st.title("👥 User Engagement and Growth Strategy")

    df_user = clean_state_df(data["user_device"])
    df_user["engagement_ratio"] = (df_user["registered_users"] / df_user["registered_users"].max()) * 100

    fig = px.line(df_user, x="state", y="engagement_ratio", markers=True,
                  title="User Engagement Ratio by State (%)")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user["engagement_ratio"].idxmax()]
    st.info(
        f"💡 **Insight:** {top_state['state']} shows the highest engagement ratio "
        f"({top_state['engagement_ratio']:.2f}%), indicating very active and loyal users."
    )

# ---------------------------------------------------------------
# 🧠 INSIGHTS SUMMARY
# ---------------------------------------------------------------
elif menu == "🧠 Insights Summary":
    st.title("🧠 Summary of Key Business Insights")
    st.markdown("---")

    st.markdown("""
    ✅ **Transaction Dynamics:**  
    Karnataka, Maharashtra, and Tamil Nadu drive the highest transaction volumes.  
    Recharge & Bill Payments lead category-wise transactions.

    ✅ **Device Insights:**  
    Android-based devices dominate the market, primarily Xiaomi & Samsung.

    ✅ **Insurance Penetration:**  
    South Indian states lead insurance adoption; policy values show growing financial awareness.

    ✅ **Market Expansion:**  
    Tier-2 and Tier-3 districts are emerging as PhonePe’s next big opportunity zones.

    ✅ **User Engagement:**  
    High correlation between registered users and transaction activity in metro & semi-urban regions.
    """)
    st.success("💬 These insights highlight PhonePe’s rapid digital adoption, regional opportunities, and user engagement trends across India.")

# ---------------------------------------------------------------
# 📎 FOOTER
# ---------------------------------------------------------------
st.markdown("---")
st.caption("© 2025 | PhonePe Business Analytics Dashboard | Developed by Varsha Sureshkumar 💜")
