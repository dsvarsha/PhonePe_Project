import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="PhonePe Business Analytics", layout="wide")

st.sidebar.title("📊 PhonePe Business Analytics")
st.sidebar.markdown("Developed by **Varsha Sureshkumar 💜**")
st.sidebar.markdown("---")

# Load CSV data
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

menu = st.sidebar.radio(
    "📁 Choose Business Case Study",
    [
        "1️⃣ Transaction Dynamics",
        "2️⃣ Device Dominance",
        "3️⃣ Insurance Penetration",
        "4️⃣ Market Expansion",
        "5️⃣ User Engagement"
    ]
)

# ---- Case 1 ----
if menu == "1️⃣ Transaction Dynamics":
    st.title("📈 Transaction Dynamics Across States")

    df_state = data["txn_state"]
    df_cat = data["txn_category"]

    fig1 = px.bar(df_state, x="state", y="total_amount",
                  title="Top 10 States by Transaction Value",
                  color="total_amount", text_auto='.2s')
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(df_cat, values="total_amount", names="category",
                  title="Transaction Split by Category")
    st.plotly_chart(fig2, use_container_width=True)

    top_state = df_state.loc[df_state["total_amount"].idxmax()]
    top_cat = df_cat.loc[df_cat["total_amount"].idxmax()]
    st.success(f"💡 **Insight:** {top_state['state']} leads all states with ₹{top_state['total_amount']/1e9:.2f}B worth of transactions. "
               f"The most popular category overall is **{top_cat['category']}**.")

# ---- Case 2 ----
elif menu == "2️⃣ Device Dominance":
    st.title("📱 Device Dominance and User Engagement")

    df_user = data["user_device"]
    fig = px.bar(df_user, x="state", y="registered_users",
                 color="registered_users", title="Registered Users by State")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user["registered_users"].idxmax()]
    st.info(f"💡 **Insight:** {top_state['state']} has the highest registered users on PhonePe "
            f"with {int(top_state['registered_users']):,} total users.")

# ---- Case 3 ----
elif menu == "3️⃣ Insurance Penetration":
    st.title("🧾 Insurance Penetration Across States")

    df_ins = data["insurance_state"]
    fig = px.bar(df_ins, x="state", y="total_amount", color="total_amount",
                 title="Top 10 States by Insurance Value")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_ins.loc[df_ins["total_amount"].idxmax()]
    st.success(f"💡 **Insight:** {top_state['state']} leads in insurance value with ₹{top_state['total_amount']/1e9:.2f}B worth of policies sold.")

# ---- Case 4 ----
elif menu == "4️⃣ Market Expansion":
    st.title("🌍 Market Expansion and Growth Trends")

    df_dist = data["district_txn"]
    fig = px.bar(df_dist, x="district", y="total_amount", color="total_amount",
                 title="Top 10 Districts by Transaction Value")
    st.plotly_chart(fig, use_container_width=True)

    top_dist = df_dist.loc[df_dist["total_amount"].idxmax()]
    st.warning(f"💡 **Insight:** {top_dist['district']} is the top district, showing strong market expansion potential.")

# ---- Case 5 ----
elif menu == "5️⃣ User Engagement":
    st.title("👥 User Engagement and Growth Strategy")

    df_user = data["user_device"]
    df_user["engagement_ratio"] = (df_user["registered_users"] / df_user["registered_users"].max()) * 100
    fig = px.line(df_user, x="state", y="engagement_ratio", markers=True,
                  title="Engagement Ratio by State")
    st.plotly_chart(fig, use_container_width=True)

    top_state = df_user.loc[df_user["engagement_ratio"].idxmax()]
    st.info(f"💡 **Insight:** {top_state['state']} shows the highest engagement ratio, "
            f"indicating highly active users in this region.")
