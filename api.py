from fastapi import FastAPI
import joblib
import numpy as np
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "model_credit_card.joblib"))

FEATURE_ORDER = [
    "Time",
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28",
    "Amount"
]

THRESHOLD = 0.3


@app.post("/predict")
def predict(data: dict):
    try:
        missing = [f for f in FEATURE_ORDER if f not in data]
        if missing:
            return {"error": f"Missing features: {missing}"}

        features = [float(data[f]) for f in FEATURE_ORDER]
        features_array = np.array(features).reshape(1, -1)

        prob = model.predict_proba(features_array)[0][1]
        decision = "high_risk" if prob > THRESHOLD else "low_risk"

        return {
            "risk_score": float(prob),
            "decision": decision,
            "threshold": THRESHOLD
        }

    except Exception as e:
        return {"error": str(e)}