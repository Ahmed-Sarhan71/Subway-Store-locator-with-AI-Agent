import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import folium_static
from geopy.distance import geodesic


# ✅ Ensure this is the FIRST Streamlit command
st.set_page_config(page_title="Subway Outlets & AI Chatbot", layout="wide")

# ✅ API Base URLs
MAP_API_BASE_URL = "http://127.0.0.1:8001"  # Subway Stores API
CHATBOT_API_BASE_URL = "http://127.0.0.1:8000"  # AI Agent API

# ✅ Tabs for Navigation
tab1, tab2 = st.tabs(["📍 Subway Outlets Map", "🤖 Subway Chatbot"])

# ✅ 🚀 TAB 1: Subway Outlets Map (Uses API on Port 8001)
with tab1:
    st.markdown("<h1>📍 Subway Outlets in Kuala Lumpur</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Visualizing Subway store locations with a 5KM catchment radius.</h3>", unsafe_allow_html=True)

    # ✅ Fetch store data from Subway API (Port 8001)
    @st.cache_data
    def fetch_stores():
        """Get store data from Subway Stores API (Port 8001)."""
        try:
            response = requests.get(f"{MAP_API_BASE_URL}/stores")
            response.raise_for_status()  # Raise error for HTTP issues
            return response.json()  # Return parsed JSON data
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ API request failed: {e}")
            return []

    # ✅ Load data
    stores = fetch_stores()
    df = pd.DataFrame(stores)

    # ✅ Create Folium Map
    m = folium.Map(location=[3.1390, 101.6869], zoom_start=12)

    # ✅ Function to check overlapping 5KM radius
    def check_overlap(store1, store2):
        """Check if two stores' 5KM radii overlap."""
        lat1, lon1 = store1["latitude"], store1["longitude"]
        lat2, lon2 = store2["latitude"], store2["longitude"]
        return geodesic((lat1, lon1), (lat2, lon2)).km < 5  # Distance in KM

    # ✅ Add Markers & Circles
    for store in stores:
        lat, lon = store["latitude"], store["longitude"]
        store_name = store["store_name"]

        # Check if this store overlaps with any other store
        is_intersecting = any(check_overlap(store, other) for other in stores if store != other)
        circle_color = "red" if is_intersecting else "blue"

        popup_html = f'<div style="white-space: nowrap; font-weight: bold;">{store_name}</div>'

        folium.Marker([lat, lon], popup=folium.Popup(popup_html, max_width=300)).add_to(m)

        folium.Circle(
            location=[lat, lon],
            radius=5000,  # 5KM radius
            color=circle_color,
            fill=True,
            fill_color=circle_color,
            fill_opacity=0.001
        ).add_to(m)

    # ✅ Display Map
    folium_static(m)

# ✅ 🚀 TAB 2: Subway AI Chatbot (Uses API on Port 8000)
with tab2:
    st.title("🤖 Subway Chatbot")
    st.write("Ask me anything about Subway stores in Kuala Lumpur!")

    # ✅ Function to Query the AI Agent API (Port 8000)
    def query_ai_agent(user_input):
        try:
            response = requests.post(f"{CHATBOT_API_BASE_URL}/query", json={"question": user_input})
            response.raise_for_status()  # Raise error for HTTP issues
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ API request failed: {e}")
            return None

    # ✅ User Input Box
    user_query = st.text_input("Type your question here:")

    # ✅ Handle User Query
    if user_query:
        with st.spinner("Thinking... 🤔"):
            # ✅ Send query to FastAPI AI agent
            response = query_ai_agent(user_query)

            # ✅ Display SQL Debugging (if available)
            if response and "sql_query" in response:
                st.write(f"**Generated SQL Query (Debugging):** `{response['sql_query']}`")  # Debugging Only

            # ✅ Display AI Response
            if response and "response" in response:
                st.success(response["response"])
            else:
                st.error("I couldn't process that request. Please try again.")
