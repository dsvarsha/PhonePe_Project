💳 PhonePe Business Analytics Dashboard
📊 An End-to-End Data Analytics and Visualization Project using Python, MySQL, and Streamlit
👩‍💻 Developed by: Varsha Sureshkumar

📧 Email: varshasuresh0708@gmail.com

🎓 Department: Electronics and Communication Engineering
🏫 Institution: KGiSL Institute of Technology

🏗️ Project Overview

The PhonePe Business Analytics Dashboard is a comprehensive data analytics solution designed to explore, process, and visualize India’s digital payment trends using the PhonePe Pulse Dataset.
This project demonstrates the entire ETL (Extract, Transform, Load) process — from reading raw JSON data to creating an interactive web-based dashboard for business insights.

The goal is to analyze transaction patterns, user engagement, and insurance growth to uncover meaningful insights that support fintech-driven decision-making.

🎯 Objectives

To build a robust ETL pipeline for large-scale JSON datasets.

To design a relational database (MySQL) for efficient data storage and querying.

To develop an interactive visualization dashboard for real-time analytics.

To identify high-performing states, emerging markets, and transaction trends.

To deliver data-driven business intelligence for strategic growth.

⚙️ Technology Stack
Category	Tools / Technologies
Programming Languages	Python, SQL
Libraries & Frameworks	Pandas, Plotly, Streamlit, MySQL Connector
Database	MySQL
Visualization Tools	Streamlit, Power BI
Version Control	Git, GitHub
Other Tools	Microsoft Excel, SAP (Data Migration), Figma
🧩 Workflow Overview
1️⃣ Data Extraction

Extracted JSON data from the official PhonePe Pulse Dataset
.

Used Python’s os and json libraries to read multiple data files automatically.

2️⃣ Data Transformation

Processed and cleaned the raw data using Pandas.

Created structured dataframes containing columns such as year, quarter, state, transaction type, count, and amount.

3️⃣ Data Loading

Designed and normalized 9 SQL tables for efficient querying:

aggregated_transaction

aggregated_user

aggregated_insurance

map_transaction

map_user

map_insurance

top_transaction

top_user

top_insurance

Loaded over 9000 records into MySQL through automated ETL scripts.

4️⃣ Dashboard Development

Created an interactive dashboard using Streamlit and Plotly.

Integrated filters by state, district, year, and category for real-time exploration.

5️⃣ Deployment

Deployed the dashboard on Streamlit Cloud for live access.

Version control handled using Git and GitHub.

🗂️ Database Schema Summary
Table	Description
aggregated_transaction	Aggregated data of transactions by category and quarter
aggregated_user	Device and user registration data
aggregated_insurance	Insurance policy transaction records
map_transaction	District-wise mapping of transaction data
map_user	District-level user distribution
map_insurance	District-level insurance adoption
top_transaction	Highest transaction values per state
top_user	Top registered users by category
top_insurance	Top-performing states in insurance
📊 Business Case Studies

The project includes analytical insights across multiple business domains:

Case Study	Description
1. Transaction Dynamics	Examines regional and category-wise growth patterns.
2. Device Dominance	Identifies top-used devices across states.
3. Insurance Penetration	Studies insurance transaction trends and potential growth areas.
4. User Engagement	Evaluates active users and app engagement metrics.
5. Market Expansion	Detects underperforming regions with future market opportunities.
📈 Key Insights

Karnataka, Maharashtra, and Telangana lead in overall transaction value.

UPI payments show consistent growth across all quarters.

Android devices dominate user engagement.

Insurance transactions are rising rapidly in Tier-2 and Tier-3 states.

Generated actionable business insights for regional strategy formulation.

💻 How to Run the Project
Step 1️⃣: Clone this Repository
git clone https://github.com/dsvarsha/PhonePe_Project.git

Step 2️⃣: Navigate into the Folder
cd PhonePe_Project

Step 3️⃣: Install Required Packages
pip install -r requirements.txt

Step 4️⃣: Run the Streamlit Dashboard
streamlit run dashboard_phonepe_pro.py


Then open your browser and visit:
👉 http://localhost:8501

🌐 Live Dashboard

View the deployed dashboard here 👇
🔗 PhonePe Business Analytics — Streamlit App

🧠 Learning Outcomes

Gained practical knowledge of ETL pipelines and data warehousing.

Applied data visualization techniques using Streamlit and Plotly.

Developed strong SQL querying and database design skills.

Learned deployment and version control using GitHub and Streamlit Cloud.

🧩 Future Enhancements

Integration with real-time APIs for live transaction data.

Addition of Machine Learning models for predictive analytics.

Building Power BI reports for advanced business intelligence.

🧑‍💻 Author Details

Varsha Sureshkumar
📍 ECE Undergraduate, KGiSL Institute of Technology
📧 varshasuresh0708@gmail.com

🔗 GitHub Profile

🌐 Streamlit Dashboard

🏁 Conclusion

This project demonstrates the complete journey from raw data to meaningful insight generation, combining software development, data analytics, and IoT domain understanding.
It reflects the importance of data visualization and real-time analytics in the fintech industry.

🌟 Acknowledgements

Dataset: PhonePe Pulse GitHub Repository

Tools & Technologies: Streamlit, Plotly, MySQL, Python

Guided by: Faculty mentors from KGiSL Institute of Technology

🪪 License

This project is developed for educational and academic purposes only.

✅ "Turning data into insight, and insight into innovation."

📜 Keywords

Python • Streamlit • Plotly • MySQL • Data Analytics • ETL • Fintech • Business Intelligence • IoT • Power BI