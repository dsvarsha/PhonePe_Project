💳 PhonePe Business Analytics Dashboard
📊 End-to-End Data Analysis and Visualization using Python, MySQL, and Streamlit
👩‍💻 Developed by: Varsha Sureshkumar

📧 Email: varshasuresh0708@gmail.com

🎓 Department: Electronics and Communication Engineering
🏫 Institution: KGiSL Institute of Technology

📖 Table of Contents

Overview

Goal

Guide

Documentation

Architecture

Database Schema

Dashboard Features

Business Case Studies

Insights & Findings

Future Scope

Installation Guide

Data Source

License

Author

🏗️ Overview

The PhonePe Business Analytics Dashboard is a complete data engineering and visualization project that analyzes India’s digital payments landscape using open-source PhonePe Pulse data.

This project implements an ETL pipeline (Extract, Transform, Load) to convert raw JSON data into an organized MySQL database, and visualizes the findings interactively using Streamlit and Plotly.

🎯 Goal

To design and develop a scalable analytics platform that:

Extracts and transforms raw JSON data into structured relational databases.

Enables interactive, real-time visualization of financial and user data.

Provides business insights for understanding digital transaction trends in India.

🧭 Guide

This project is categorized into three data modules derived from the PhonePe Pulse dataset:

Module	Description
Aggregated Data	Summarized data of transactions, users, and insurance trends.
Map Data	Regional data distribution across states and districts.
Top Data	Lists top-performing states, districts, and pin codes by volume and value.
📘 Documentation

Dataset: PhonePe Pulse - Open Data Platform

Format: JSON

Coverage: 2018–2024

Domains: Transactions, Users, Insurance

License: CDLA-Permissive-2.0

🧩 Architecture
1️⃣ Data Extraction

Extracted JSON data directly from the PhonePe Pulse GitHub repository.

Parsed and processed multiple JSON structures using Python scripts.

2️⃣ Data Transformation

Cleaned, standardized, and structured the raw data using Pandas.

Created structured DataFrames for each analytical category.

3️⃣ Data Loading

Built a MySQL database consisting of 9 structured tables.

Automated data loading with MySQL Connector (9000+ records processed).

4️⃣ Visualization

Designed an interactive dashboard using Streamlit and Plotly.

Added filtering features for year, quarter, category, and state.

5️⃣ Deployment

Hosted live on Streamlit Cloud for easy public access.

Integrated GitHub for continuous version management and updates.

🧮 Database Schema
Table	Description
aggregated_transaction	Quarterly transaction data by type and category.
aggregated_user	User registration and app engagement metrics.
aggregated_insurance	Insurance transaction records by region.
map_transaction	State and district-level transaction distribution.
map_user	Regional user base and app activity.
map_insurance	State-wise insurance analytics.
top_transaction	Top states and districts by transaction value.
top_user	Top states/districts by user registrations.
top_insurance	Leading states in insurance adoption.
🖥️ Dashboard Features

📊 Transaction Trends: Quarterly and category-wise analytics.

👥 User Insights: Registered users and app opens by device brand.

🛡️ Insurance Analytics: Policy adoption patterns and growth.

🌍 Geographical View: Interactive maps by state and district.

🕒 Time Trends: Analyze by year, quarter, and region.

⚙️ Dynamic Filters: Easily toggle data views for deeper insights.

📈 Business Case Studies
Case Study	Description
1. Transaction Dynamics	Study of growth patterns and category shifts in digital payments.
2. Device Dominance	Analysis of user engagement across device brands.
3. Insurance Penetration	Regional analysis of insurance adoption.
4. Market Expansion	Identifying underperforming but high-potential regions.
5. User Engagement	Tracking user registrations and app opens per region.
📊 Insights & Findings

Karnataka, Maharashtra, and Telangana dominate India’s digital payments landscape.

UPI transactions show steady growth every quarter.

Android is the most preferred platform for PhonePe usage.

Insurance adoption is increasing rapidly in Tier-2 regions.

The dashboard enables instant, real-time data exploration.

🚀 Future Scope

This project can be enhanced with the following advanced features:

🧠 Machine Learning Integration: Predict future transaction trends using regression or time-series forecasting models.

📡 Real-Time API Integration: Connect with live UPI or fintech APIs for streaming transaction data.

📊 Power BI Dashboard Expansion: Create enterprise-level visualization dashboards for deeper analytics.

🗺️ Advanced Geospatial Mapping: Integrate Plotly Mapbox or Folium for granular location-based visualization.

🔐 User Authentication: Enable role-based access for personalized dashboards.

💬 AI Insights Engine: Incorporate NLP models to automatically summarize insights from datasets.

These upgrades would transform the dashboard into a smart fintech analytics platform, bridging data science, IoT, and business intelligence.

⚙️ Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/dsvarsha/PhonePe_Project.git

2️⃣ Open the Folder
cd PhonePe_Project

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Application
streamlit run dashboard_phonepe_pro.py

5️⃣ View the Dashboard

Open your browser and go to → http://localhost:8501

🌐 Live Dashboard

🎯 Access the live deployed dashboard here:
🔗 PhonePe Business Analytics Dashboard

📊 Data Source

Dataset: PhonePe Pulse Open Data Repository

License: CDLA-Permissive-2.0

Update Frequency: Quarterly

Data Categories: Transactions, Users, Insurance

🧑‍💻 Author

Varsha Sureshkumar
🎓 ECE Undergraduate | KGiSL Institute of Technology
📧 varshasuresh0708@gmail.com

🔗 GitHub Profile

📜 License

Licensed under the CDLA-Permissive-2.0 License.
Developed for academic and research purposes only.

🏁 Conclusion

The PhonePe Business Analytics Dashboard demonstrates a seamless integration of data extraction, transformation, and visualization using real-world fintech data.
It bridges technical expertise from electronics, software, and data analytics, showcasing Varsha’s ability to develop scalable, data-driven solutions for financial intelligence.

✅ “Transforming Data into Insights, and Insights into Innovation.”

🪩 Keywords

Python • MySQL • Streamlit • Plotly • Data Analytics • ETL • Fintech • Business Intelligence • Power BI • IoT