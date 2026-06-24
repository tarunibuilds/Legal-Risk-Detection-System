import pickle
import numpy as np
from src.preprocess import preprocess_text

print("✅ UPDATED PREDICT.PY LOADED")

# ==============================
# LOAD MODELS
# ==============================

category_model = pickle.load(open("models/category_model.pkl", "rb"))
risk_model = pickle.load(open("models/risk_model.pkl", "rb"))

# ==============================
# EXPLANATION ENGINE
# ==============================

def generate_explanation(clause, risk):
    text = clause.lower()

    if "without" in text and "notice" in text:
        return "This clause allows termination without prior notice, which is highly risky."

    if "penalty" in text or "fine" in text:
        return "This clause includes a financial penalty, increasing legal risk."

    if "non-refundable" in text:
        return "This clause states payments are non-refundable, which may lead to financial loss."

    if "liability" in text or "indemnify" in text:
        return "This clause imposes legal or financial responsibility on a party."

    if "breach" in text:
        return "This clause defines consequences of contract violation."

    if risk == "High":
        return "This clause contains legally sensitive or restrictive terms."

    return "This clause appears standard with no major risk indicators."

# ==============================
# RULE ENGINE (SMART)
# ==============================

def get_rule_score(text):
    text = text.lower()
    score = 0

    high_keywords = [
        "immediate termination",
        "non-refundable",
        "sole discretion",
        "terminate immediately",
        "no liability",
        "indemnify",
        "binding decision"
    ]

    medium_keywords = [
        "penalty",
        "breach",
        "liability",
        "delay",
        "obligation",
        "fine",
        "charge"
    ]

    # 🔥 Smart detection
    if "without" in text and "notice" in text:
        score += 3

    for word in high_keywords:
        if word in text:
            score += 3

    for word in medium_keywords:
        if word in text:
            score += 2

    return score

# ==============================
# CONFIDENCE FIX
# ==============================

def compute_confidence(scores):
    try:
        raw = abs(float(np.max(scores)))
        confidence = (raw / (raw + 0.5)) * 100
        confidence = max(65, min(confidence + 10, 95))
        return round(confidence, 2)
    except:
        return 65.0

# ==============================
# MAIN FUNCTION
# ==============================

def predict_clause(clause):

    clean_text = preprocess_text(clause)
    X_input = [clean_text]

    # ML predictions
    category = category_model.predict(X_input)[0]
    ml_risk = risk_model.predict(X_input)[0]

    # Confidence
    try:
        cat_scores = category_model.decision_function(X_input)
        risk_scores = risk_model.decision_function(X_input)

        cat_conf = compute_confidence(cat_scores)
        risk_conf = compute_confidence(risk_scores)

    except:
        cat_conf = 65.0
        risk_conf = 65.0

    # Rule scoring
    rule_score = get_rule_score(clause)
    print(f"DEBUG → Rule Score: {rule_score}")

    # Hybrid logic
    if rule_score >= 3:
        final_risk = "High"
        source = "Rule-Based Override"
    elif rule_score >= 2:
        final_risk = "Medium"
        source = "Rule-Based Adjustment"
    else:
        final_risk = ml_risk
        source = "ML Model"

    explanation = generate_explanation(clause, final_risk)

    return (
        category,
        final_risk,
        rule_score,
        cat_conf,
        risk_conf,
        source,
        explanation
    )

# ==============================
# TEST
# ==============================

if __name__ == "__main__":
    test = "The company may terminate employment without prior notice."
    print("\nTest Clause:", test)
    print("Output:", predict_clause(test))