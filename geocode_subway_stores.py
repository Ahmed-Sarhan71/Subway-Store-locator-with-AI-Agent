import googlemaps
import sqlite3
import time
import os
from dotenv import load_dotenv

load_dotenv()

# 1️⃣ Initialize Google Maps API Client
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")  # Replace with your API key
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# 2️⃣ Connect to SQLite Database
conn = sqlite3.connect("subway_stores.db")
cursor = conn.cursor()


# Fetch all stores without coordinates
cursor.execute("SELECT id, address FROM subway_stores WHERE latitude IS NULL OR longitude IS NULL")
stores = cursor.fetchall()

for store in stores:
    store_id, address = store
    try:
        print(f"Geocoding: {address}")
        
        # 4️⃣ Get latitude & longitude using Google Maps API
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            latitude, longitude = location['lat'], location['lng']
            print(f"Found: {latitude}, {longitude}")

            # 5️⃣ Update database with new coordinates
            cursor.execute("""
                UPDATE subway_stores 
                SET latitude = ?, longitude = ? 
                WHERE id = ?
            """, (latitude, longitude, store_id))
            conn.commit()
        else:
            print("Location not found.")

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(1)  # Sleep to prevent hitting API rate limits

# Close database connection
conn.close()
print("✅ Geocoding complete. Database updated.")
