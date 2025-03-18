import sqlite3

# ✅ Database File
DATABASE = "subway_stores.db"

# ✅ Connect to SQLite
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# ✅ Create subway_stores Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subway_stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_name TEXT NOT NULL,
    address TEXT NOT NULL,
    operating_hours TEXT NOT NULL,
    waze_link TEXT,
    latitude REAL ,
    longitude REAL
);
""")

# ✅ Create subway_store_operating_hours Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS subway_store_operating_hours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    day_of_week TEXT NOT NULL,
    opening_time TEXT NOT NULL,
    closing_time TEXT NOT NULL,
    FOREIGN KEY (store_id) REFERENCES subway_stores(id) ON DELETE CASCADE
);
""")

# ✅ Commit and Close Connection
conn.commit()
conn.close()

print("✅ Database and tables created successfully!")
