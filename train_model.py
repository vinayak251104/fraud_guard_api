"""
Fraud Detection Model Training Script
Dataset: creditcard.csv
Models Evaluated: Logistic Regression, Random Forest, XGBoost, Neural Network (Keras)
Final Model: Random Forest Classifier
Output: model_credit_card.joblib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils.class_weight import compute_class_weight

from xgboost import XGBClassifier

import tensorflow as tf
from keras import layers, models

# ── Config ────────────────────────────────────────────────────────────────────

DATASET_PATH  = "creditcard.csv"
MODEL_OUTPUT  = "model_credit_card.joblib"
RANDOM_STATE  = 42
TEST_SIZE     = 0.2
THRESHOLDS    = [0.3, 0.5, 0.7]

FEATURE_ORDER = [
    "Time",
    "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
    "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
    "V21","V22","V23","V24","V25","V26","V27","V28",
    "Amount"
]

# ── Load Data ─────────────────────────────────────────────────────────────────

df = pd.read_csv(DATASET_PATH)
print(df.info())
print(df.head())
print("\nClass distribution:\n", df["Class"].value_counts(normalize=True))
print("\nAmount stats:\n", df["Amount"].describe())

# ── EDA ───────────────────────────────────────────────────────────────────────

plt.figure(figsize=(40, 40))
sns.heatmap(df.corr(), annot=True)
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("heatmap.png")
plt.close()

for feature in ["V14", "V19", "Amount"]:
    sns.histplot(data=df, x=feature, hue="Class", bins=50, kde=True)
    plt.title(f"{feature} Distribution by Class")
    plt.savefig(f"dist_{feature}.png")
    plt.close()

# ── Train / Test Split ────────────────────────────────────────────────────────

X = df[FEATURE_ORDER]
y = df["Class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
)

# ── Model 1: Logistic Regression ──────────────────────────────────────────────

print("\n── Logistic Regression ──")
lr_pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(class_weight="balanced", max_iter=1000))
])
lr_pipeline.fit(X_train, y_train)
lr_probs = lr_pipeline.predict_proba(X_test)[:, 1]
lr_pred  = (lr_probs > 0.95).astype(int)
print(confusion_matrix(y_test, lr_pred))
print(classification_report(y_test, lr_pred))

# ── Model 2: Random Forest ────────────────────────────────────────────────────

print("\n── Random Forest ──")
rf_model = RandomForestClassifier(
    n_estimators=200,
    criterion="gini",
    min_samples_split=3,
    min_samples_leaf=3,
    max_features="sqrt",
    class_weight="balanced",
    max_samples=0.8,
    random_state=RANDOM_STATE
)
rf_model.fit(X_train, y_train)

rf_probs = rf_model.predict_proba(X_test)[:, 1]
for t in THRESHOLDS:
    rf_pred = (rf_probs > t).astype(int)
    print(f"\nRandom Forest — Threshold: {t}")
    print(classification_report(y_test, rf_pred))

# ── Model 3: XGBoost ──────────────────────────────────────────────────────────

print("\n── XGBoost ──")
xg_model = XGBClassifier(
    objective="binary:logistic",
    learning_rate=0.1,
    max_depth=6,
    n_estimators=200,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1,
    gamma=1,
    booster="gbtree",
    tree_method="auto",
    scale_pos_weight=580,
    random_state=RANDOM_STATE
)
xg_model.fit(X_train, y_train)

xg_probs = xg_model.predict_proba(X_test)[:, 1]
for t in THRESHOLDS:
    xg_pred = (xg_probs > t).astype(int)
    print(f"\nXGBoost — Threshold: {t}")
    print(classification_report(y_test, xg_pred))

# ── Model 4: Neural Network (Keras) ───────────────────────────────────────────

print("\n── Neural Network ──")

# compute class weights to handle imbalance
classes = np.unique(y_train)
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)
class_weight_dict = {int(k): float(v) for k, v in zip(classes, class_weights)}
print("Class Weights:", class_weight_dict)

nn_model = models.Sequential([
    layers.Input(shape=(X_train.shape[1],)),
    layers.Dense(64, activation="relu"),
    layers.Dense(32, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])
nn_model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
nn_model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=256,
    validation_split=0.2,
    class_weight=class_weight_dict,
    verbose=1
)

nn_probs = nn_model.predict(X_test).ravel()
for t in THRESHOLDS:
    nn_pred = (nn_probs > t).astype(int)
    print(f"\nNeural Network — Threshold: {t}")
    print(classification_report(y_test, nn_pred))

# ── Cross Validation (Final Model: Random Forest) ─────────────────────────────

print("\n── Cross Validation (Random Forest) ──")
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
scores = cross_val_score(rf_model, X, y, cv=skf, scoring="recall")
print("Recall scores:", scores)
print("Mean recall:  ", scores.mean())

# ── Save Final Model ──────────────────────────────────────────────────────────

joblib.dump(rf_model, MODEL_OUTPUT)
print(f"\n Model saved to {MODEL_OUTPUT}")
