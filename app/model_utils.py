import joblib
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_model():
    model = joblib.load("models/xgb_drug_model.pkl")
    le_drug = joblib.load("models/le_drug.pkl")
    le_condition = joblib.load("models/le_condition.pkl")
    bert_model = SentenceTransformer("bert_model")
    known_conditions = list(le_condition.classes_)
    condition_embeddings = bert_model.encode(known_conditions)
    return model, le_drug, le_condition, bert_model, condition_embeddings

def extract_condition_nn(user_text, known_conditions, condition_embeddings, bert_model, threshold=0.5):
    user_emb = bert_model.encode([user_text])
    sim_scores = cosine_similarity(user_emb, condition_embeddings)[0]
    best_idx = sim_scores.argmax()
    if sim_scores[best_idx] < threshold:
        return "unknown"
    return known_conditions[best_idx]

def predict_drugs(review, top_k, model, le_drug, le_condition, bert_model, condition_embeddings):
    known_conditions = list(le_condition.classes_)
    condition_input = extract_condition_nn(review, known_conditions, condition_embeddings, bert_model)
    cond_enc = le_condition.transform([condition_input])[0]

    review_emb = bert_model.encode([review])
    user_rating = 10
    count_reviews = 1
    numeric_feats = np.array([[user_rating, count_reviews, cond_enc]])

    X_input = np.hstack([review_emb, numeric_feats])
    probs = model.predict_proba(X_input)[0]

    top_idx = np.argsort(probs)[::-1][:top_k]
    top_drugs = le_drug.inverse_transform(top_idx)
    top_probs = probs[top_idx].tolist()
    predictions = list(zip(top_drugs, top_probs))

    return predictions, condition_input

