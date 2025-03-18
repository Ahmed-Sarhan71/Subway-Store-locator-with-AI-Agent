
# Subway Store locator with AI Agent

A comprehensive system for scraping Subway store data, processing it, and providing API/chatbot access. Built with Python, FastAPI, Streamlit, and NVIDIA NIM.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

## Features
- Web scraping for Subway store locations
- SQLite database integration
- Address geocoding using Google Maps API
- Store hours normalization
- REST API backend
- AI chatbot integration (Llama3-8B)
- Streamlit web interface

## Prerequisites

- Python 3.11
- SQLite Browser
- Google Cloud account (for Geocoding API)
- NVIDIA API key (for LLM access)
- Basic terminal/command prompt knowledge

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Ahmed-Sarhan71/Scraping-Storing-and-Processing-v2
cd Scraping-Storing-and-Processing-v2
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python create_database.py
```
*Creates SQLite database with proper schema for storing store information*

## Configuration

### Google Maps API
1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Create `.env` file in project root:
```env
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### NVIDIA NIM Setup
1. Get API key from [NVIDIA NGC](https://build.nvidia.com/)
2. Add to `.env`:
```env
API_KEY=your_nvidia_key_here
BASE_URL=https://integrate.api.nvidia.com/v1
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

## Usage

### Data Pipeline
1. **Scrape Store Data**
```bash
python subway_scrapper.py
```
*Gathers raw store data from Subway website*

2. **Standardize Inconsistent Format and Update Database**
```bash
python update_store_hours.py
```
*Converts operating hours to standardized format*

3. **Data Processing & Normalization**
```bash
python parse_and_store_operating_hours.py
```
*The operating hours were stored in a single text field initially as unstructured text. This script uses regex to extract and separate them into structured fields: `day_of_week`, `opening_time`, and `closing_time`.*

4. **Geocode Addresses**
```bash
python geocode_subway_stores.py
```
*Converts physical addresses to GPS coordinates using Google Maps API*

### Start Backend Services
```bash
# Store API (port 8001)
uvicorn subway_api:app --reload --port 8001

# Chatbot API (port 8000)
uvicorn ai_agent_api:app --reload --port 8000
```
*Note: Keep both terminals open or run in background*

### Launch Web Interface
```bash
streamlit run app.py
```
*Access UI at http://localhost:8501*

## API Endpoints

### Store API (`:8001`)
- `GET /stores` - List all stores
- `GET /stores/{id}` - Get specific store details
- `GET /stores/search?location=...` - Search stores by location

### Chatbot API (`:8000`)
- `POST /chat` - Natural language query interface
```json
{
  "message": "How many stores are open on Sundays?"
}
```

## Project Structure
```
├── app.py                # Streamlit frontend
├── subway_api.py         # Store data API
├── ai_agent_api.py       # LLM chatbot API
├── subway_scrapper.py    # Web scraping script
├── geocode_subway_stores.py  # Address conversion
├── create_database.py    # DB initialization
├── requirements.txt      # Python dependencies
├── .env                  # Store API keys
└── test_api.py           # API test suite
```

## Testing
Verify system functionality with:
```bash
python test_api.py
```
*Tests both API endpoints and basic data integrity*

---

**Note:** Ensure ports 8000, 8001, and 8501 are available before starting services.

