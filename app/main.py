from fastapi import FastAPI
from pydantic import BaseModel
from app.model_utils import load_model, predict_drugs
from app.agent import send_email
import sqlite3

model, le_drug, le_condition, bert_model, condition_embeddings = load_model()

conn = sqlite3.connect("logs.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS recommendations(
    rec_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    email TEXT,
    problem TEXT,
    recommended_drugs TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

class PredictRequest(BaseModel):
    name: str
    age: int
    email: str
    review: str
    top_k: int = 3

def log_recommendation(name, age, email, problem, drugs):
    c.execute(
        "INSERT INTO recommendations(name, age, email, problem, recommended_drugs) VALUES (?, ?, ?, ?, ?)",
        (name, age, email, problem, ", ".join(drugs))
    )
    conn.commit()
    return c.lastrowid  # return auto-generated rec_id

@app.post("/recommend/")
def recommend(request: PredictRequest):
    predictions, _ = predict_drugs(
        request.review,
        request.top_k,
        model, le_drug, le_condition, bert_model, condition_embeddings
    )
    top_drugs = [drug for drug, _ in predictions]

    rec_id = log_recommendation(request.name, request.age, request.email, request.review, top_drugs)

    try:
        send_email(request.email, rec_id, request.name, request.age, request.review, top_drugs)
    except Exception as e:
        return {"error": f"Failed to send email: {e}"}

    return {"rec_id": rec_id, "predictions": top_drugs}
