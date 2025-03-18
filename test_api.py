import requests

API_URL = "http://127.0.0.1:8000/query"

test_queries = [
    "How many Subway stores are there?",
    "Which Subway outlets open the earliest?",
    "How many stores operate on Sundays?",
]

def test_api():
    for query in test_queries:
        print(f"\n🔍 Testing Query: {query}")
        
        response = requests.post(API_URL, json={"question": query})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SQL Query: {data.get('sql_query', 'N/A')}")
            print(f"🤖 Response: {data.get('response', 'No response')}")
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_api()
