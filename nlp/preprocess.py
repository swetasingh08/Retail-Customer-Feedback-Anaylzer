import re
import string
import pandas as pd

import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


# --------------------------------------------------
# NLTK resources
# --------------------------------------------------

# Run these downloads once during environment setup.
# nltk.download("punkt")
# nltk.download("punkt_tab")
# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("omw-1.4")


# --------------------------------------------------
# NLP objects
# --------------------------------------------------
# Initialize NLP tools
stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


# Preserve important sentiment-related negation words
negation_words = {
    "no",
    "not",
    "never",
    "nor",
    "neither",
    "hardly",
    "scarcely",
    "barely"
}

custom_stop_words = stop_words - negation_words


def combine_reviews(review_header, review_text):
    """
    Combine Review_Header and Review_text into one text field.
    Missing values are treated as empty strings.
    """

    header = "" if pd.isna(review_header) else str(review_header)
    review = "" if pd.isna(review_text) else str(review_text)

    return f"{header} {review}".strip()


def preprocess_text(text):
    """
    Clean and normalize customer review text.

    Steps:
    1. Handle missing values
    2. Convert to lowercase
    3. Remove URLs
    4. Remove HTML tags
    5. Normalize repeated characters
    6. Remove punctuation
    7. Normalize whitespace
    8. Tokenize
    9. Remove stopwords while preserving negation
    10. Lemmatize
    """

    # Handle missing values
    if pd.isna(text):
        return ""

    # Convert to string
    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+|https\S+",
        "",
        text
    )

    # Remove HTML tags
    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    # Normalize repeated characters
    # Example: goooood -> good
    text = re.sub(
        r"(.)\1{2,}",
        r"\1\1",
        text
    )

    # Remove punctuation
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Normalize whitespace
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    # Tokenization
    tokens = word_tokenize(text)

    # Stopword removal
    tokens = [
        word
        for word in tokens
        if word not in custom_stop_words
    ]

    # Lemmatization
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    # Convert tokens back into text
    cleaned_text = " ".join(tokens)

    return cleaned_text


def conservative_preprocess_text(text):
    """
    Create a conservative text representation for sentiment modeling.

    This keeps more signal than preprocess_text by avoiding stopword removal,
    lemmatization, repeated-word collapsing, and repeated-character normalization.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Remove URLs and HTML tags while keeping the surrounding words separated.
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)

    # Drop punctuation/symbols, but keep letters, numbers, and whitespace.
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Normalize whitespace deterministically.
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_dataframe(df):
    """
    Apply the complete preprocessing pipeline
    to the customer feedback dataframe.
    """

    df = df.copy()

    # Combine header and review text
    df["Combined_Text"] = df.apply(
        lambda row: combine_reviews(
            row["Review_Header"],
            row["Review_text"]
        ),
        axis=1
    )

    # Clean combined text
    df["Cleaned_Text"] = (
        df["Combined_Text"]
        .apply(preprocess_text)
    )

    return df
