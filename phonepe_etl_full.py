import os
import json
import mysql.connector
from mysql.connector import Error

# ---------- CONFIGURATION (EDIT THESE) ----------
HOST = "localhost"
USER = "root"
PASSWORD = "varsha2003"          # <-- your MySQL password
DATABASE = "phonepe_db"
DATA_DIR = r"C:\PhonePe_Project\pulse-master\data"   # <-- path to the 'data' folder
# -------------------------------------------------

def connect_mysql():
    try:
        conn = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, database=DATABASE
        )
        return conn
    except Error as e:
        print("❌ Error connecting to MySQL:", e)
        return None

def create_tables(conn):
    cur = conn.cursor()
    # Aggregated
    cur.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_transaction (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, state VARCHAR(100), category VARCHAR(200),
      transaction_type VARCHAR(50), count BIGINT, amount DECIMAL(20,2)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_user (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, state VARCHAR(100), brand VARCHAR(100),
      registered_users BIGINT, app_opens BIGINT, percentage FLOAT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS aggregated_insurance (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, state VARCHAR(100), insurance_type VARCHAR(100),
      count BIGINT, amount DECIMAL(20,2)
    )""")
    # Map
    cur.execute("""
    CREATE TABLE IF NOT EXISTS map_transaction (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, state VARCHAR(100), district VARCHAR(100),
      count BIGINT, amount DECIMAL(20,2)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS map_user (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, state VARCHAR(100), district VARCHAR(100),
      registered_users BIGINT, app_opens BIGINT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS map_insurance (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, state VARCHAR(100), district VARCHAR(100),
      count BIGINT, amount DECIMAL(20,2)
    )""")
    # Top
    cur.execute("""
    CREATE TABLE IF NOT EXISTS top_transaction (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, level VARCHAR(50), entity_name VARCHAR(150),
      count BIGINT, amount DECIMAL(20,2)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS top_user (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, level VARCHAR(50), entity_name VARCHAR(150),
      registered_users BIGINT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS top_insurance (
      id INT AUTO_INCREMENT PRIMARY KEY,
      year INT, quarter INT, level VARCHAR(50), entity_name VARCHAR(150),
      count BIGINT, amount DECIMAL(20,2)
    )""")
    # Processed files (idempotency)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS processed_files (
      file_path VARCHAR(255) PRIMARY KEY,
      processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP) 
      ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)

    conn.commit()
    cur.close()

def extract_year_quarter(file_path):
    # expects .../<year>/<quarter>.json
    p = file_path.replace("\\","/").rstrip("/")
    parts = p.split("/")
    if len(parts) >= 2:
        year = parts[-2]
        quarter = os.path.splitext(parts[-1])[0]
        try:
            return int(year), int(quarter)
        except:
            return None, None
    return None, None

def file_already_processed(cur, normalized_path):
    cur.execute("SELECT 1 FROM processed_files WHERE file_path=%s", (normalized_path,))
    return cur.fetchone() is not None

def mark_file_processed(cur, conn, normalized_path):
    cur.execute("INSERT INTO processed_files (file_path) VALUES (%s)", (normalized_path,))
    conn.commit()

# Each loader returns number of rows inserted (approx)
def aggregated_transaction_etl(cur, conn, file_path, state):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for t in data["data"].get("transactionData", []):
            cat = t.get("name")
            for p in t.get("paymentInstruments", []):
                rows.append((year,q,state,cat,p.get("type"),p.get("count"),p.get("amount")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO aggregated_transaction
            (year,quarter,state,category,transaction_type,count,amount) VALUES (%s,%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def aggregated_user_etl(cur, conn, file_path, state):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        agg = data["data"].get("aggregated", {})
        reg = agg.get("registeredUsers")
        app = agg.get("appOpens")
        for d in data["data"].get("usersByDevice", []):
            rows.append((year,q,state,d.get("brand"), reg, app, d.get("percentage")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO aggregated_user
            (year,quarter,state,brand,registered_users,app_opens,percentage) VALUES (%s,%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def aggregated_insurance_etl(cur, conn, file_path, state):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for t in data["data"].get("transactionData", []):
            cat = t.get("name")
            for p in t.get("paymentInstruments", []):
                rows.append((year,q,state,cat,p.get("count"),p.get("amount")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO aggregated_insurance
            (year,quarter,state,insurance_type,count,amount) VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def map_transaction_etl(cur, conn, file_path, state):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for d in data["data"].get("hoverDataList", []):
            metric = d.get("metric", [])
            if metric:
                m = metric[0]
                rows.append((year,q,state,d.get("name"), m.get("count"), m.get("amount")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO map_transaction
            (year,quarter,state,district,count,amount) VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def map_user_etl(cur, conn, file_path, state):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        hover = data["data"].get("hoverData", {})
        for dist, v in hover.items():
            rows.append((year,q,state,dist, v.get("registeredUsers"), v.get("appOpens")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO map_user
            (year,quarter,state,district,registered_users,app_opens) VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def map_insurance_etl(cur, conn, file_path, state):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for d in data["data"].get("hoverDataList", []):
            metric = d.get("metric", [])
            if metric:
                m = metric[0]
                rows.append((year,q,state,d.get("name"), m.get("count"), m.get("amount")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO map_insurance
            (year,quarter,state,district,count,amount) VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def top_transaction_etl(cur, conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for level in ["states","districts","pincodes"]:
            for e in data["data"].get(level, []):
                m = e.get("metric", {})
                # field may be "entityName" or "name"
                en = e.get("entityName") or e.get("name")
                rows.append((year,q, level[:-1], en, m.get("count"), m.get("amount")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO top_transaction
            (year,quarter,level,entity_name,count,amount) VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def top_user_etl(cur, conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for level in ["states","districts","pincodes"]:
            for e in data["data"].get(level, []):
                en = e.get("entityName") or e.get("name")
                rows.append((year,q, level[:-1], en, e.get("registeredUsers")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO top_user
            (year,quarter,level,entity_name,registered_users) VALUES (%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def top_insurance_etl(cur, conn, file_path):
    with open(file_path, 'r', encoding='utf-8') as f: data = json.load(f)
    year, q = extract_year_quarter(file_path)
    rows=[]
    try:
        for level in ["states","districts","pincodes"]:
            for e in data["data"].get(level, []):
                m = e.get("metric", {})
                en = e.get("entityName") or e.get("name")
                rows.append((year,q, level[:-1], en, m.get("count"), m.get("amount")))
    except Exception:
        pass
    if rows:
        cur.executemany("""INSERT INTO top_insurance
            (year,quarter,level,entity_name,count,amount) VALUES (%s,%s,%s,%s,%s,%s)""", rows)
        conn.commit()
    return len(rows)

def run_full_etl():
    if not os.path.isdir(DATA_DIR):
        print("❌ DATA_DIR not found:", DATA_DIR)
        return

    conn = connect_mysql()
    if conn is None:
        return
    create_tables(conn)
    cur = conn.cursor()

    summary = {
        "aggregated_transaction":0,
        "aggregated_user":0,
        "aggregated_insurance":0,
        "map_transaction":0,
        "map_user":0,
        "map_insurance":0,
        "top_transaction":0,
        "top_user":0,
        "top_insurance":0,
        "files_processed":0
    }

    print("🚀 Starting Full ETL from:", DATA_DIR)
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if not file.lower().endswith(".json"):
                continue
            path = os.path.join(root, file)
            normalized_path = os.path.normpath(path)
            path_lower = normalized_path.replace("\\","/").lower()

            # skip if processed
            if file_already_processed(cur, normalized_path):
                continue

            state = None
            if "/state/" in path_lower:
                state = path_lower.split("/state/")[1].split("/")[0].replace("-", " ").title()

            try:
                if "aggregated/transaction" in path_lower:
                    count = aggregated_transaction_etl(cur, conn, normalized_path, state)
                    summary["aggregated_transaction"] += count
                elif "aggregated/user" in path_lower:
                    count = aggregated_user_etl(cur, conn, normalized_path, state)
                    summary["aggregated_user"] += count
                elif "aggregated/insurance" in path_lower:
                    count = aggregated_insurance_etl(cur, conn, normalized_path, state)
                    summary["aggregated_insurance"] += count
                elif "map/transaction" in path_lower:
                    count = map_transaction_etl(cur, conn, normalized_path, state)
                    summary["map_transaction"] += count
                elif "map/user" in path_lower:
                    count = map_user_etl(cur, conn, normalized_path, state)
                    summary["map_user"] += count
                elif "map/insurance" in path_lower:
                    count = map_insurance_etl(cur, conn, normalized_path, state)
                    summary["map_insurance"] += count
                elif "top/transaction" in path_lower:
                    count = top_transaction_etl(cur, conn, normalized_path)
                    summary["top_transaction"] += count
                elif "top/user" in path_lower:
                    count = top_user_etl(cur, conn, normalized_path)
                    summary["top_user"] += count
                elif "top/insurance" in path_lower:
                    count = top_insurance_etl(cur, conn, normalized_path)
                    summary["top_insurance"] += count
                else:
                    # unknown file location, skip
                    continue

                # mark as processed
                mark_file_processed(cur, conn, normalized_path)
                summary["files_processed"] += 1
                print(f"Processed: {normalized_path} (rows added ~ {count})")

            except Exception as e:
                print("Error processing", normalized_path, ":", e)

    cur.close()
    conn.close()

    print("✅ ETL complete.")
    print("Files processed:", summary["files_processed"])
    print("Rows by table:")
    for k,v in summary.items():
        if k!="files_processed":
            print(f"  {k}: {v}")

if __name__ == "__main__":
    run_full_etl()
