from fastapi import FastAPI
from pydantic import BaseModel
from app.model_utils import load_model, predict_drugs
from app.agent import drug_agent
import sqlite3

# -------------------- Load models --------------------
model, le_drug, le_condition, bert_model, condition_embeddings = load_model()

# -------------------- Database --------------------
conn = sqlite3.connect("logs.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS recommendations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rec_id TEXT,
    name TEXT,
    age INTEGER,
    problem TEXT,
    condition TEXT,
    recommended_drugs TEXT,
    action TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# -------------------- FastAPI --------------------
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

class PredictRequest(BaseModel):
    rec_id: str
    name: str
    age: int
    review: str
    top_k: int = 3

def log_recommendation(rec_id, name, age, problem, condition, drugs, action):
    c.execute(
        "INSERT INTO recommendations(rec_id, name, age, problem, condition, recommended_drugs, action) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (rec_id, name, age, problem, condition, ", ".join(drugs), action)
    )
    conn.commit()

@app.post("/recommend/")
def recommend(request: PredictRequest):
    predictions, condition_input = predict_drugs(
        request.review,
        request.top_k,
        model, le_drug, le_condition, bert_model, condition_embeddings
    )
    
    decision = drug_agent(predictions)
    log_recommendation(
        request.rec_id,
        request.name,
        request.age,
        request.review,
        condition_input,
        decision["drugs"],
        decision["action"]
    )
    
    return {
        "condition_detected": condition_input,
        "predictions": predictions
    }
