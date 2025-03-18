from fastapi import FastAPI, HTTPException, Query
import sqlite3
from pydantic import BaseModel
from typing import List, Optional
from math import radians, sin, cos, sqrt, atan2

# ✅ Initialize FastAPI App
app = FastAPI(title="Subway Store API", description="API to serve Subway outlet data, including geographical coordinates.")

DATABASE = "subway_stores.db"

# ✅ Define Pydantic Models
class Store(BaseModel):
    id: int
    store_name: str
    address: str
    operating_hours: Optional[str] = None
    waze_link: Optional[str] = None
    latitude: float
    longitude: float

# ✅ Function to Connect to SQLite
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return data as dictionary-like rows
    return conn

# ✅ Haversine Formula to Calculate Distance Between Two Coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

# ✅ 1️⃣ Get All Stores
@app.get("/stores", response_model=List[Store])
def get_all_stores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subway_stores")
    stores = cursor.fetchall()
    conn.close()
    return [dict(store) for store in stores]

# ✅ 2️⃣ Get Store by ID
@app.get("/stores/{store_id}", response_model=Store)
def get_store_by_id(store_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subway_stores WHERE id = ?", (store_id,))
    store = cursor.fetchone()
    conn.close()

    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    
    return dict(store)

# ✅ 3️⃣ Get Stores Within a Given Radius
@app.get("/stores/nearby", response_model=List[Store])
def get_nearby_stores(lat: float, lon: float, radius: float = Query(5, description="Radius in kilometers")):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subway_stores")
    stores = cursor.fetchall()
    conn.close()

    # Filter stores by distance
    nearby_stores = []
    for store in stores:
        store_dict = dict(store)
        distance = haversine(lat, lon, store_dict["latitude"], store_dict["longitude"])
        if distance <= radius:
            nearby_stores.append(store_dict)

    return nearby_stores
