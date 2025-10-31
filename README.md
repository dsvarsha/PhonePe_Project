💜 PhonePe Business Analytics Dashboard | 2025
Developed by: Varsha Sureshkumar

B.E. Electronics & Communication Engineering
KGiSL Institute of Technology | Coimbatore
📧 Email: varshasuresh0708@gmail.com

🌐 Live Dashboard on Streamlit

💻 GitHub Repository

🪄 Project Overview

This project presents a comprehensive data analytics pipeline for the PhonePe Pulse Dataset, focused on understanding digital payment trends, user engagement, and insurance growth across India.

The entire process — from data extraction (ETL) to interactive dashboard visualization — was automated using Python, MySQL, and Streamlit.

🎯 Objectives

Automate the ETL (Extract–Transform–Load) process for PhonePe data extraction and storage.

Normalize and store JSON data into a MySQL database using Python.

Generate aggregated datasets (transactions, users, insurance, districts).

Build a Streamlit dashboard to visualize state & district-level insights.

Perform 5 business case studies with meaningful insights and recommendations.

Deploy the dashboard using Streamlit Cloud and integrate with GitHub.

⚙️ Tech Stack
Category	Tools & Technologies
Programming	Python (Pandas, JSON, NumPy)
Database	MySQL
Visualization	Streamlit, Plotly, Power BI
ETL Automation	Python + MySQL Connector
Version Control	Git, GitHub
Frontend Design	HTML, CSS, UI/UX (Figma)
Other Tools	Microsoft Excel, SAP (Data Migration)
🧩 Project Architecture
PhonePe_Project/
│
├── pulse-master/                  # Raw JSON data from PhonePe Pulse
├── phonepe_etl_full.py            # Full ETL pipeline (Extract, Transform, Load)
├── mysql_test.py                  # MySQL connection tester
├── analysis_results/              # Processed CSV files for visualization
│   ├── top_states_transaction.csv
│   ├── transaction_by_category.csv
│   ├── top_states_users.csv
│   ├── top_states_insurance.csv
│   ├── top_districts_transaction.csv
│
├── dashboard_phonepe_pro.py       # Streamlit dashboard (visualization layer)
├── README.md                      # Project documentation
└── Project_Report.pdf / .pptx     # Supporting files for submission

🛠️ ETL Pipeline Summary
🔹 Step 1: Extraction

Parsed 9,000+ JSON files from the PhonePe Pulse dataset using Python.

Extracted data for:

Aggregated Transactions

Aggregated Users

Aggregated Insurance

Map and Top transaction data (state/district/pincode)

🔹 Step 2: Transformation

Cleaned JSON records.

Normalized structure and formatted data types (amounts, counts).

Removed duplicates and null states.

🔹 Step 3: Loading

Stored all processed data into MySQL (phonepe_db) across 9 structured tables.

Tables: aggregated_transaction, map_user, map_insurance, top_transaction, etc.

🔹 Step 4: CSV Export

Queried MySQL to extract summarized datasets for visualization.

Saved outputs as:

top_states_transaction.csv

top_states_users.csv

top_states_insurance.csv

transaction_by_category.csv

top_districts_transaction.csv

📊 Dashboard Modules (Streamlit)
Module	Description	Output
🏠 Dashboard Overview	Summary of pipeline and objectives	Overview page
1️⃣ Transaction Dynamics	Top states & categories by value	Bar & Pie Charts
2️⃣ Device Dominance	Registered users by state/device	Bar Chart
3️⃣ Insurance Penetration	Top states by insurance value	Bar Chart
4️⃣ Market Expansion	District-level performance	Bar Chart
5️⃣ User Engagement	Engagement ratio by state	Line Chart
🧠 Insights Summary	Key findings and business insights	Summary text
📚 Business Case Studies

1️⃣ Decoding Transaction Dynamics
→ Karnataka, Maharashtra, and Tamil Nadu lead with the highest transaction volumes.

2️⃣ Device Dominance and User Engagement
→ Majority of PhonePe users are on Android (Xiaomi, Samsung); strong adoption in Tier-1 states.

3️⃣ Insurance Penetration and Growth Potential
→ Southern states show high insurance uptake; opportunity in Northern regions.

4️⃣ Market Expansion Trends
→ Tier-2 cities and districts like Bihar, MP, and Rajasthan show emerging market potential.

5️⃣ User Engagement & Retention Strategy
→ Metro users exhibit higher app engagement; reward programs can increase loyalty.

📈 Key Insights

💸 Karnataka and Maharashtra are the top-performing states by transaction value.

📱 Xiaomi and Samsung dominate user device registrations.

🧾 Insurance adoption is highest in Southern India.

🌍 Bihar and MP show high growth in Tier-2 expansion.

👥 User retention is driven by app trust and usage frequency.

🚀 Deployment

Hosted on Streamlit Cloud

Linked directly to the GitHub repository for continuous updates

Automatically refreshes upon each commit

🔗 View Live Dashboard

🧠 Future Scope

Integration of real-time API data feeds.

AI-driven predictive analytics for transaction forecasting.

State-wise anomaly detection using ML models.

Enhanced interactive visuals with Power BI or Tableau.

🏁 Conclusion

This project demonstrates the end-to-end implementation of a data analytics solution,
covering everything from ETL automation to visualization.

It highlights PhonePe’s digital payment ecosystem, offering valuable insights into
regional performance, device usage, and insurance growth — bridging technology, data,
and business strategy effectively. 💜

📄 License

This project is open-source under the CDLA Permissive License v2.0, in alignment with the official PhonePe Pulse Dataset