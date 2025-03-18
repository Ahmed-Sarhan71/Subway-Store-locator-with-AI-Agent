from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()

# ✅ Initialize FastAPI
app = FastAPI(title="Subway AI Agent API", description="API to handle chatbot queries and execute SQL.")

# ✅ NVIDIA NIM API Setup
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)


DATABASE = "subway_stores.db"

# ✅ Define Request Model
class QueryRequest(BaseModel):
    question: str  # User's natural language question

# ✅ Generate SQL Query with NVIDIA NIM
def generate_sql_query(user_input: str) -> str:
    completion = client.chat.completions.create(
        model="meta/llama3-8b-instruct",
        messages=[{"role": "user", "content": f"""
            Convert this question into an SQL query using the tables:
            1️⃣ `subway_stores` (id, store_name, address, latitude, longitude)
            2️⃣ `subway_store_operating_hours` (store_id, day_of_week, opening_time, closing_time)
            
            Ensure the SQL query is in correct **SQLite** syntax.
            Only return the SQL query itself without explanations.

            User question: {user_input}
        """}],
        temperature=0,
        max_tokens=100
    )
    return completion.choices[0].message.content.strip()

# ✅ Execute SQL Query
def execute_sql_query(sql_query: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        conn.close()
        return f"SQL Error: {e}"

# ✅ Format AI Response
def format_response(user_input: str, sql_result):
    if not sql_result or sql_result == [(0,)]:
        return "I'm sorry, but I couldn't find any relevant data."

    completion = client.chat.completions.create(
        model="meta/llama3-8b-instruct",
        messages=[{"role": "user", "content": f"""
            Convert this database result into a conversational response.
            Question: {user_input}
            Result: {sql_result}
            Do NOT include raw SQL output.
        """}],
        temperature=0.5,
        max_tokens=300
    )
    return completion.choices[0].message.content.strip()

# ✅ API Endpoint to Process Queries
@app.post("/query")
def process_query(request: QueryRequest):
    user_question = request.question
    sql_query = generate_sql_query(user_question)
    sql_result = execute_sql_query(sql_query)
    response = format_response(user_question, sql_result)
    
    return {"sql_query": sql_query, "response": response}
