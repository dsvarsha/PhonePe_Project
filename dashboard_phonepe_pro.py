# dashboard_phonepe_pro.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

DATA_DIR = Path(__file__).parent / "analysis_results"


# ---------- Page setup ----------
st.set_page_config(page_title="📱 PhonePe Business Analytics Dashboard", layout="wide")
st.title("📊 PhonePe Business Analytics — Varsha Sureshkumar")

st.markdown("### Explore transaction, user, and insurance insights across India")

# ---------- Load data ----------
@st.cache_data
def load_csvs():
    data = {
        "states_txn": pd.read_csv(DATA_DIR / "top_states_transaction.csv"),
        "by_category": pd.read_csv(DATA_DIR / "transaction_by_category.csv"),
        "users": pd.read_csv(DATA_DIR / "top_states_users.csv"),
        "insurance": pd.read_csv(DATA_DIR / "top_states_insurance.csv"),
        "districts": pd.read_csv(DATA_DIR / "top_districts_transaction.csv")
    }
    return data

data = load_csvs()

# ---------- Sidebar Filters ----------
st.sidebar.header("🔎 Filter Options")

# dynamic options
state_options = data["states_txn"]["state"].dropna().unique().tolist()
category_options = data["by_category"]["category"].dropna().unique().tolist()

selected_state = st.sidebar.selectbox("Select State", ["All"] + state_options)
selected_category = st.sidebar.selectbox("Select Transaction Category", ["All"] + category_options)

# ---------- KPIs ----------
st.markdown("### 🧭 Key Performance Indicators")

total_value = round(data["states_txn"]["total_in_crores"].sum(), 2)
total_users = int(data["users"]["total_registered_users"].sum())
total_policies = int(data["insurance"]["total_policies"].sum())

col1, col2, col3 = st.columns(3)
col1.metric("Total Transaction Value (₹ Cr)", f"{total_value:,}")
col2.metric("Total Registered Users", f"{total_users:,}")
col3.metric("Total Insurance Policies", f"{total_policies:,}")

st.markdown("---")

# ---------- Tabs ----------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏙️ State Transactions", "💸 Categories", "👥 Users", "🛡️ Insurance", "📍 Districts"
])

# ---------- 1. State Transactions ----------
with tab1:
    st.subheader("Top 10 States by Transaction Value (₹ Crores)")
    df = data["states_txn"]
    if selected_state != "All":
        df = df[df["state"] == selected_state]
    fig = px.bar(df, x="state", y="total_in_crores", text="total_in_crores",
                 color="state", title="Transaction Value by State")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# ---------- 2. Categories ----------
with tab2:
    st.subheader("Transaction Value by Category")
    df = data["by_category"]
    if selected_category != "All":
        df = df[df["category"] == selected_category]
    fig = px.pie(df, names="category", values="total_in_crores",
                 title="Transaction Share by Category")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# ---------- 3. Users ----------
with tab3:
    st.subheader("Top States by Registered Users and App Opens")
    df = data["users"]
    fig = px.bar(df, x="state", y="total_registered_users", text="total_registered_users",
                 color="state", title="Registered Users by State")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# ---------- 4. Insurance ----------
with tab4:
    st.subheader("Top States by Insurance Transactions")
    df = data["insurance"]
    fig = px.bar(df, x="state", y="total_policies", text="total_policies",
                 color="state", title="Insurance Adoption by State")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

# ---------- 5. Districts ----------
with tab5:
    st.subheader("Top Districts by Transaction Value (₹ Crores)")
    df = data["districts"]
    fig = px.bar(df, x="district", y="total_in_crores", text="total_in_crores",
                 color="district", title="District Performance in Transactions")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)

st.markdown("---")
st.caption("Built by Varsha Sureshkumar | ECE | PhonePe Business Analytics Project 2025 ©")

