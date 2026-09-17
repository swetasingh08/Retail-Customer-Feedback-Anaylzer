import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT /
    "data" /
    "processed_feedback.csv"
)

MODEL_DIR = (
    PROJECT_ROOT /
    "models"
)

MODEL_DIR.mkdir(
    exist_ok=True
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print(
    f"Loaded {len(df):,} records."
)


# --------------------------------------------------
# Prepare data
# --------------------------------------------------

df["processed_review"] = (
    df["processed_review"]
    .fillna("")
    .astype(str)
)

df = df[
    df["processed_review"].str.strip() != ""
].copy()

X = df["processed_review"]

y = df["sentiment"]


# --------------------------------------------------
# Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# TF-IDF
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(
    X_train
)

X_test_tfidf = vectorizer.transform(
    X_test
)


# --------------------------------------------------
# Train model
# --------------------------------------------------

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(
    X_train_tfidf,
    y_train
)


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

y_pred = model.predict(
    X_test_tfidf
)

accuracy = accuracy_score(
    y_test,
    y_pred
)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)


# --------------------------------------------------
# Save artifacts
# --------------------------------------------------

joblib.dump(
    model,
    MODEL_DIR / "sentiment_model.pkl"
)

joblib.dump(
    vectorizer,
    MODEL_DIR / "vectorizer.pkl"
)

print("\nModel saved:")
print(
    MODEL_DIR / "sentiment_model.pkl"
)

print("Vectorizer saved:")
print(
    MODEL_DIR / "vectorizer.pkl"
)