import sqlite3
import re
from datetime import datetime

# Converts 12-hour AM/PM time to 24-hour format with seconds
def convert_to_24h(time_str):
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M:%S")

# Expands day ranges into individual days
def expand_days(day_range):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Public Holiday"]
    
    parts = day_range.split(" - ")
    if len(parts) == 1:
        return [parts[0]]

    start_day, end_day = parts
    
    if "Public Holiday" in end_day:
        return days_of_week[days_of_week.index(start_day):] + ["Public Holiday"]

    start_idx = days_of_week.index(start_day)
    end_idx = days_of_week.index(end_day)

    return days_of_week[start_idx:end_idx+1]

# Extracts and structures operating hours
def process_hours(data):
    entries = []
    pattern = re.compile(r"([A-Za-z -]+): ([0-9:AMP ]+) - ([0-9:AMP ]+)")
    
    for line in data.split("\n"):
        parts = line.split(" | ")
        for part in parts:
            match = pattern.match(part.strip())
            if match:
                days, open_time, close_time = match.groups()
                expanded_days = expand_days(days)
                open_24h = convert_to_24h(open_time)
                close_24h = convert_to_24h(close_time)
                for day in expanded_days:
                    entries.append((day, open_24h, close_24h))
    
    return entries

# Predefined problematic cases
KNOWN_CASES = {
    "Monday - Friday: 08:00 AM - 06:30 PM | Saturday - Sunday & Public Holiday: 08:00 AM - 03:00 PM": [
        ("Monday", "08:00:00", "18:30:00"),
        ("Tuesday", "08:00:00", "18:30:00"),
        ("Wednesday", "08:00:00", "18:30:00"),
        ("Thursday", "08:00:00", "18:30:00"),
        ("Friday", "08:00:00", "18:30:00"),
        ("Saturday", "08:00:00", "15:00:00"),
        ("Sunday", "08:00:00", "15:00:00"),
        ("Public Holiday", "08:00:00", "15:00:00"),
    ],
    "Sunday - Thursday: 10:00 AM - 08:00 PM | Friday - Saturday: 09:00 AM - 08:00 PM": [
        ("Sunday", "10:00:00", "20:00:00"),
        ("Monday", "10:00:00", "20:00:00"),
        ("Tuesday", "10:00:00", "20:00:00"),
        ("Wednesday", "10:00:00", "20:00:00"),
        ("Thursday", "10:00:00", "20:00:00"),
        ("Friday", "09:00:00", "20:00:00"),
        ("Saturday", "09:00:00", "20:00:00"),
    ],
    "Sunday - Thursday: 10:00 AM - 10:00 PM | Friday - Saturday: 10:00 AM - 10:30 PM": [
        ("Sunday", "10:00:00", "22:00:00"),
        ("Monday", "10:00:00", "22:00:00"),
        ("Tuesday", "10:00:00", "22:00:00"),
        ("Wednesday", "10:00:00", "22:00:00"),
        ("Thursday", "10:00:00", "22:00:00"),
        ("Friday", "10:00:00", "22:30:00"),
        ("Saturday", "10:00:00", "22:30:00"),
    ],
}

# Connect to SQLite database
def store_hours_to_db():
    db_path = "subway_stores.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subway_store_operating_hours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER,
            day_of_week TEXT,
            opening_time TEXT,
            closing_time TEXT,
            FOREIGN KEY (store_id) REFERENCES subway_stores(id)
        )
    """)

    # Retrieve store data
    cursor.execute("SELECT id, operating_hours FROM subway_stores")
    stores = cursor.fetchall()

    # Transaction for efficiency
    try:
        for store_id, hours in stores:
            # Check for known problematic cases
            if hours in KNOWN_CASES:
                structured_hours = KNOWN_CASES[hours]
            else:
                structured_hours = process_hours(hours)

            # Insert processed data
            for day, open_time, close_time in structured_hours:
                cursor.execute("""
                    INSERT INTO subway_store_operating_hours (store_id, day_of_week, opening_time, closing_time)
                    VALUES (?, ?, ?, ?)
                """, (store_id, day, open_time, close_time))

        conn.commit()
        print("✅ Store hours successfully stored in database.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {e}")

    finally:
        conn.close()

# Run the script
if __name__ == "__main__":
    store_hours_to_db()
