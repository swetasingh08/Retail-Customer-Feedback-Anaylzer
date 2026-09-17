import pandas as pd


# ============================================================
# BASIC INSIGHTS
# ============================================================

def get_basic_insights(total_feedback, average_rating):
    """
    Generate basic overall feedback insights.
    """

    return {
        "total_feedback": total_feedback,
        "average_rating": round(average_rating, 2)
    }


# ============================================================
# SENTIMENT INSIGHTS
# ============================================================

def get_sentiment_insights(sentiment_data):
    """
    Analyze overall sentiment distribution.
    """

    if not sentiment_data:
        return None

    df = pd.DataFrame(sentiment_data)

    df["count"] = pd.to_numeric(
        df["count"],
        errors="coerce"
    )

    total = df["count"].sum()

    if total == 0:
        return None

    df["percentage"] = (
        df["count"] / total * 100
    ).round(2)

    highest = df.loc[
        df["count"].idxmax()
    ]

    return {
        "highest_sentiment": highest["sentiment"],
        "highest_count": int(highest["count"]),
        "highest_percentage": float(
            highest["percentage"]
        ),
        "distribution": df
    }


# ============================================================
# HIGHEST RATED CATEGORY
# ============================================================

def get_highest_rated_category(category_data):
    """
    Find the category with the highest average rating.
    """

    if not category_data:
        return None

    df = pd.DataFrame(category_data)

    df["average_rating"] = pd.to_numeric(
        df["average_rating"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["average_rating"]
    )

    if df.empty:
        return None

    row = df.loc[
        df["average_rating"].idxmax()
    ]

    return {
        "category": row["category"],
        "rating": float(row["average_rating"])
    }


# ============================================================
# LOWEST RATED CATEGORY
# ============================================================

def get_lowest_rated_category(category_data):
    """
    Find the category with the lowest average rating.
    """

    if not category_data:
        return None

    df = pd.DataFrame(category_data)

    df["average_rating"] = pd.to_numeric(
        df["average_rating"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["average_rating"]
    )

    if df.empty:
        return None

    row = df.loc[
        df["average_rating"].idxmin()
    ]

    return {
        "category": row["category"],
        "rating": float(row["average_rating"])
    }


# ============================================================
# MOST REVIEWED CATEGORY
# ============================================================

def get_most_reviewed_category(category_data):
    """
    Find the category with the highest number of reviews.
    """

    if not category_data:
        return None

    df = pd.DataFrame(category_data)

    df["total_reviews"] = pd.to_numeric(
        df["total_reviews"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["total_reviews"]
    )

    if df.empty:
        return None

    row = df.loc[
        df["total_reviews"].idxmax()
    ]

    return {
        "category": row["category"],
        "reviews": int(row["total_reviews"])
    }


# ============================================================
# MOST NEGATIVE CATEGORY
# ============================================================

def get_most_negative_category(category_data):
    """
    Find the category with the highest number
    of negative reviews.
    """

    if not category_data:
        return None

    df = pd.DataFrame(category_data)

    df["negative_reviews"] = pd.to_numeric(
        df["negative_reviews"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["negative_reviews"]
    )

    if df.empty:
        return None

    row = df.loc[
        df["negative_reviews"].idxmax()
    ]

    return {
        "category": row["category"],
        "negative_reviews": int(
            row["negative_reviews"]
        )
    }


# ============================================================
# HIGHEST POSITIVE CATEGORY
# ============================================================

def get_most_positive_category(category_data):
    """
    Find the category with the highest number
    of positive reviews.
    """

    if not category_data:
        return None

    df = pd.DataFrame(category_data)

    df["positive_reviews"] = pd.to_numeric(
        df["positive_reviews"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["positive_reviews"]
    )

    if df.empty:
        return None

    row = df.loc[
        df["positive_reviews"].idxmax()
    ]

    return {
        "category": row["category"],
        "positive_reviews": int(
            row["positive_reviews"]
        )
    }


# ============================================================
# CATEGORY PERFORMANCE
# ============================================================

def prepare_category_performance(category_data):
    """
    Prepare category-level performance data
    for dashboard tables and charts.
    """

    if not category_data:
        return pd.DataFrame()

    df = pd.DataFrame(category_data)

    numeric_columns = [
        "total_reviews",
        "average_rating",
        "positive_reviews",
        "neutral_reviews",
        "negative_reviews"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "total_reviews" in df.columns:

        df["positive_percentage"] = (
            df["positive_reviews"]
            / df["total_reviews"]
            * 100
        ).round(2)

        df["neutral_percentage"] = (
            df["neutral_reviews"]
            / df["total_reviews"]
            * 100
        ).round(2)

        df["negative_percentage"] = (
            df["negative_reviews"]
            / df["total_reviews"]
            * 100
        ).round(2)

    return df


# ============================================================
# REVIEW LENGTH INSIGHTS
# ============================================================

def get_review_length_insights(review_data):
    """
    Analyze review length.
    """

    if not review_data:
        return None

    df = pd.DataFrame(review_data)

    df["review_length"] = pd.to_numeric(
        df["review_length"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["review_length"]
    )

    if df.empty:
        return None

    return {
        "average_length": round(
            df["review_length"].mean(),
            2
        ),

        "shortest_length": int(
            df["review_length"].min()
        ),

        "longest_length": int(
            df["review_length"].max()
        )
    }


# ============================================================
# RATING INSIGHTS
# ============================================================

def get_rating_insights(rating_data):
    """
    Analyze rating distribution.
    """

    if not rating_data:
        return None

    df = pd.DataFrame(rating_data)

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    df["count"] = pd.to_numeric(
        df["count"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["rating", "count"]
    )

    if df.empty:
        return None

    row = df.loc[
        df["count"].idxmax()
    ]

    return {
        "most_common_rating": int(
            row["rating"]
        ),
        "count": int(row["count"]),
        "distribution": df
    }


# ============================================================
# MASTER INSIGHTS
# ============================================================

def generate_business_insights(
    total_feedback,
    average_rating,
    sentiment_data,
    category_data,
    rating_data=None,
    review_data=None
):
    """
    Generate all major business insights
    required by the application.
    """

    insights = {}

    # -----------------------------
    # Basic
    # -----------------------------

    insights["total_feedback"] = total_feedback
    insights["average_rating"] = round(
        average_rating,
        2
    )

    # -----------------------------
    # Sentiment
    # -----------------------------

    sentiment = get_sentiment_insights(
        sentiment_data
    )

    insights["sentiment"] = sentiment

    # -----------------------------
    # Categories
    # -----------------------------

    insights["highest_rated_category"] = (
        get_highest_rated_category(
            category_data
        )
    )

    insights["lowest_rated_category"] = (
        get_lowest_rated_category(
            category_data
        )
    )

    insights["most_reviewed_category"] = (
        get_most_reviewed_category(
            category_data
        )
    )

    insights["most_negative_category"] = (
        get_most_negative_category(
            category_data
        )
    )

    insights["most_positive_category"] = (
        get_most_positive_category(
            category_data
        )
    )

    # -----------------------------
    # Rating
    # -----------------------------

    if rating_data is not None:

        insights["rating"] = (
            get_rating_insights(
                rating_data
            )
        )

    # -----------------------------
    # Review Length
    # -----------------------------

    if review_data is not None:

        insights["review_length"] = (
            get_review_length_insights(
                review_data
            )
        )

    return insights


"""4. What insights Phase 6 will provide

Your application can now answer questions such as:

Overall
How many reviews do we have?
What is the average rating?
Sentiment
What percentage of customers are Positive?
What percentage are Neutral?
What percentage are Negative?
Which sentiment is dominant?
Category
Which category has the most reviews?
Which category has the highest average rating?
Which category has the lowest average rating?
Which category has the most negative reviews?
Which category has the most positive reviews?
Rating
How many 1-star reviews?
How many 2-star reviews?
...
How many 5-star reviews?
Which rating is most common?
Review text
What is the average review length?
What is the shortest review?
What is the longest review?
How does review length vary with sentiment/rating?"""