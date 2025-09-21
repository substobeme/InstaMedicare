def drug_agent(predictions, min_confidence=0.3):
    """Decide drugs to recommend based on probability."""
    top_drugs = [drug for drug, prob in predictions if prob >= min_confidence]
    action = "recommend" if top_drugs else "flag_for_review"
    return {"action": action, "drugs": top_drugs}
