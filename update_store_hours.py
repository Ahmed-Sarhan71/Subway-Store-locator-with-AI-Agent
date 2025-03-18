import sqlite3

DATABASE = "subway_stores.db"

new_operating_hours = [
    "Monday - Sunday: 08:00 AM - 08:00 PM",
    "Monday - Saturday: 08:00 AM - 09:00 PM | Sunday: 11:30 AM - 06:30 PM",
    "Monday - Saturday: 08:00 AM - 08:30 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Saturday: 08:00 AM - 09:00 PM",
    "Monday - Friday: 08:00 AM - 06:30 PM | Saturday - Sunday & Public Holiday: 08:00 AM - 03:00 PM",
    "Monday - Sunday: 09:30 AM - 09:30 PM",
    "Monday - Sunday: 08:30 AM - 09:00 PM",
    "Monday - Friday: 08:00 AM - 09:00 PM | Saturday - Sunday: 10:00 AM - 07:00 PM",
    "Monday - Sunday: 10:15 AM - 09:30 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 09:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 08:00 PM | Friday: 09:00 AM - 09:00 PM",
    "Monday - Sunday: 10:00 AM - 08:00 PM",
    "Monday - Sunday: 08:00 AM - 09:00 PM",
    "Monday - Sunday: 08:00 AM - 09:30 PM",
    "Monday: 10:00 AM - 08:00 PM | Tuesday - Thursday: 08:00 AM - 08:00 PM | Friday: 08:20 AM - 08:00 PM | Saturday: 09:00 AM - 09:00 PM",
    "Monday - Sunday: 08:00 AM - 10:30 PM",
    "Monday - Sunday: 08:30 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 08:00 PM",
    "Monday - Saturday: 08:30 AM - 10:00 PM | Sunday: 08:30 AM - 09:30 PM",
    "Monday - Sunday: 09:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Friday: 08:30 AM - 08:30 PM | Saturday - Sunday: 09:30 AM - 08:30 PM",
    "Monday - Sunday: 09:00 AM - 09:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 09:00 AM - 10:00 PM",
    "Monday - Sunday: 09:00 AM - 10:00 PM",
    "Tuesday - Sunday: 10:00 AM - 09:30 PM | Monday: 08:00 AM - 09:30 PM",
    "Monday - Sunday: 09:00 AM - 09:30 PM",
    "Sunday - Thursday: 10:00 AM - 08:00 PM | Friday - Saturday: 09:00 AM - 08:00 PM",
    "Monday - Sunday: 10:00 AM - 09:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 08:30 PM",
    "Monday - Sunday: 08:00 AM - 08:30 PM",
    "Monday - Sunday: 07:30 AM - 10:00 PM",
    "Monday - Sunday: 09:30 AM - 10:00 PM",
    "Monday - Sunday: 09:30 AM - 09:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Sunday - Thursday: 10:00 AM - 10:00 PM | Friday - Saturday: 10:00 AM - 10:30 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 08:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM",
    "Monday - Sunday: 10:00 AM - 10:00 PM"
]

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Fetch all store IDs
cursor.execute("SELECT id FROM subway_stores")
store_ids = cursor.fetchall()

# Ensure there are enough operating hours for each store
if len(store_ids) != len(new_operating_hours):
    print("⚠️ The number of stores and operating hours data do not match!")
else:
    # Update each store's operating hours
    for i, (store_id,) in enumerate(store_ids):
        cursor.execute("UPDATE subway_stores SET operating_hours = ? WHERE id = ?", (new_operating_hours[i], store_id))

    conn.commit()
    print("✅ Operating hours updated successfully!")

conn.close()
