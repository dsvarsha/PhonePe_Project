import pandas as pd
import plotly.express as px
from pathlib import Path

# Path where all CSVs are saved
DATA_DIR = Path(r"C:\PhonePe_Project\analysis_results")

def save_chart(fig, filename):
    fig.write_image(str(DATA_DIR / filename))
    print("✅ Saved chart:", filename)

# 1️⃣ Top States by Transaction Value
df1 = pd.read_csv(DATA_DIR / "top_states_transaction.csv")
fig1 = px.bar(df1, x="state", y="total_in_crores",
              title="Top 10 States by Transaction Value (₹ Crores)",
              text="total_in_crores", color="state")
save_chart(fig1, "chart_top_states.png")

# 2️⃣ Transaction by Category
df2 = pd.read_csv(DATA_DIR / "transaction_by_category.csv")
fig2 = px.pie(df2, names="category", values="total_in_crores",
              title="Transaction Value by Category (₹ Crores)")
save_chart(fig2, "chart_by_category.png")

# 3️⃣ Top States by Registered Users
df3 = pd.read_csv(DATA_DIR / "top_states_users.csv")
fig3 = px.bar(df3, x="state", y="total_registered_users",
              title="Top 10 States by Registered Users",
              text="total_registered_users", color="state")
save_chart(fig3, "chart_top_users.png")

# 4️⃣ Top States by Insurance Policies
df4 = pd.read_csv(DATA_DIR / "top_states_insurance.csv")
fig4 = px.bar(df4, x="state", y="total_policies",
              title="Top 10 States by Insurance Transactions",
              text="total_policies", color="state")
save_chart(fig4, "chart_top_insurance.png")

# 5️⃣ Top Districts by Transaction Value
df5 = pd.read_csv(DATA_DIR / "top_districts_transaction.csv")
fig5 = px.bar(df5, x="district", y="total_in_crores",
              title="Top 10 Districts by Transaction Value (₹ Crores)",
              text="total_in_crores", color="district")
save_chart(fig5, "chart_top_districts.png")

print("\n🎉 All charts generated successfully in:", DATA_DIR)
