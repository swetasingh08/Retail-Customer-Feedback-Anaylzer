import joblib

from pathlib import Path

from nlp.preprocess import conservative_preprocess_text


# --------------------------------------------------
# Model paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT /
    "models" /
    "sentiment_model.pkl"
)

VECTORIZER_PATH = (
    PROJECT_ROOT /
    "models" /
    "vectorizer.pkl"
)


# --------------------------------------------------
# Load model
# --------------------------------------------------

model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)


# --------------------------------------------------
# Prediction function
# --------------------------------------------------

def predict_sentiment_with_confidence(review_text):
    """
    Predict sentiment and confidence
    for a customer review.
    """

    model_text = conservative_preprocess_text(
        review_text
    )

    text_vector = vectorizer.transform(
        [model_text]
    )

    prediction = model.predict(
        text_vector
    )[0]

    probabilities = model.predict_proba(
        text_vector
    )[0]

    confidence = probabilities.max()

    return {
        "sentiment": prediction,
        "confidence": float(confidence),
        "model_text": model_text
    }


def predict_sentiment(review_text):
    """Return only the predicted sentiment label."""

    return predict_sentiment_with_confidence(review_text)["sentiment"]
