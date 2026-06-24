import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score

# LOAD DATA
data = pd.read_csv("data/final_legal_dataset.csv")
data.columns = data.columns.str.strip()

print("\nDetected Columns:", data.columns)

# VALIDATION
if "Clause" not in data.columns or "Category" not in data.columns:
    raise ValueError("Missing required columns")

risk_column = None
for col in ["Risk", "Risk_Level"]:
    if col in data.columns:
        risk_column = col
        break

if risk_column is None:
    raise ValueError("Risk column not found")

print("Using Risk Column:", risk_column)

X = data["Clause"]
y_category = data["Category"]
y_risk = data[risk_column]

# SPLIT
X_train, X_test, y_cat_train, y_cat_test = train_test_split(
    X, y_category, test_size=0.2, random_state=42
)

X_train_r, X_test_r, y_risk_train, y_risk_test = train_test_split(
    X, y_risk, test_size=0.2, random_state=42
)

# CATEGORY MODEL
category_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000, stop_words='english')),
    ("clf", LinearSVC(class_weight="balanced"))
])

category_pipeline.fit(X_train, y_cat_train)
y_pred_cat = category_pipeline.predict(X_test)

print("\nCATEGORY MODEL")
print("Accuracy:", round(accuracy_score(y_cat_test, y_pred_cat), 3))
print(classification_report(y_cat_test, y_pred_cat))

# RISK MODEL
risk_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000, stop_words='english')),
    ("clf", LinearSVC(class_weight="balanced"))
])

risk_pipeline.fit(X_train_r, y_risk_train)
y_pred_risk = risk_pipeline.predict(X_test_r)

print("\nRISK MODEL")
print("Accuracy:", round(accuracy_score(y_risk_test, y_pred_risk), 3))
print(classification_report(y_risk_test, y_pred_risk))

# SAVE
os.makedirs("models", exist_ok=True)

pickle.dump(category_pipeline, open("models/category_model.pkl", "wb"))
pickle.dump(risk_pipeline, open("models/risk_model.pkl", "wb"))

print("\n✅ Models saved successfully!")



