import pandas as pd


# ============================================================
# BASIC STATISTICS
# ============================================================

def get_total_feedback(connection):
    """
    Return the total number of feedback records.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM feedback
    """)

    result = cursor.fetchone()[0]

    cursor.close()

    return result


def get_average_rating(connection):
    """
    Return the average customer rating.
    """

    cursor = connection.cursor()

    cursor.execute("""
        SELECT ROUND(AVG(rating), 2)
        FROM feedback
    """)

    result = cursor.fetchone()[0]

    cursor.close()

    return float(result) if result is not None else 0.0


# ============================================================
# SENTIMENT STATISTICS
# ============================================================

def get_sentiment_distribution(connection):
    """
    Return number of Positive, Neutral and Negative reviews.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            own_rating AS sentiment,
            COUNT(*) AS count
        FROM feedback
        WHERE own_rating IS NOT NULL
          AND own_rating != ''
        GROUP BY own_rating
        ORDER BY count DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


def get_sentiment_percentage(connection):
    """
    Return sentiment distribution as percentages.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            own_rating AS sentiment,
            COUNT(*) AS count,
            ROUND(
                COUNT(*) * 100.0 /
                (SELECT COUNT(*)
                 FROM feedback
                 WHERE own_rating IS NOT NULL
                   AND own_rating != ''),
                2
            ) AS percentage
        FROM feedback
        WHERE own_rating IS NOT NULL
          AND own_rating != ''
        GROUP BY own_rating
        ORDER BY percentage DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# CATEGORY STATISTICS
# ============================================================

def get_category_distribution(connection):
    """
    Return the number of reviews for each category.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,
            COUNT(*) AS total_reviews
        FROM feedback
        GROUP BY category
        ORDER BY total_reviews DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


def get_category_rating(connection):
    """
    Return average rating for each category.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,
            COUNT(*) AS total_reviews,
            ROUND(AVG(rating), 2) AS average_rating
        FROM feedback
        GROUP BY category
        ORDER BY average_rating DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


def get_category_sentiment(connection):
    """
    Return sentiment counts for every category.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,

            COUNT(*) AS total_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Positive'
                    THEN 1
                    ELSE 0
                END
            ) AS positive_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Neutral'
                    THEN 1
                    ELSE 0
                END
            ) AS neutral_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Negative'
                    THEN 1
                    ELSE 0
                END
            ) AS negative_reviews

        FROM feedback

        GROUP BY category

        ORDER BY total_reviews DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# COMPLETE CATEGORY PERFORMANCE
# ============================================================

def get_category_performance(connection):
    """
    Return complete performance information
    for every product category.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,

            COUNT(*) AS total_reviews,

            ROUND(AVG(rating), 2) AS average_rating,

            SUM(
                CASE
                    WHEN own_rating = 'Positive'
                    THEN 1
                    ELSE 0
                END
            ) AS positive_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Neutral'
                    THEN 1
                    ELSE 0
                END
            ) AS neutral_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Negative'
                    THEN 1
                    ELSE 0
                END
            ) AS negative_reviews

        FROM feedback

        GROUP BY category

        ORDER BY total_reviews DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# RATING STATISTICS
# ============================================================

def get_rating_distribution(connection):
    """
    Return the number of reviews for each rating.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            rating,
            COUNT(*) AS count
        FROM feedback
        GROUP BY rating
        ORDER BY rating
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# RATING + SENTIMENT
# ============================================================

def get_rating_sentiment(connection):
    """
    Return sentiment distribution for every rating.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            rating,

            SUM(
                CASE
                    WHEN own_rating = 'Positive'
                    THEN 1
                    ELSE 0
                END
            ) AS positive_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Neutral'
                    THEN 1
                    ELSE 0
                END
            ) AS neutral_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Negative'
                    THEN 1
                    ELSE 0
                END
            ) AS negative_reviews,

            COUNT(*) AS total_reviews

        FROM feedback

        GROUP BY rating

        ORDER BY rating
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# REVIEW STATISTICS
# ============================================================

def get_review_statistics(connection):
    """
    Return review text length statistics.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            MIN(CHAR_LENGTH(review_text)) AS shortest_review,
            MAX(CHAR_LENGTH(review_text)) AS longest_review,
            ROUND(AVG(CHAR_LENGTH(review_text)), 2) AS average_review_length
        FROM feedback
        WHERE review_text IS NOT NULL
    """)

    result = cursor.fetchone()

    cursor.close()

    return result


# ============================================================
# REVIEW LENGTH DATA
# ============================================================

def get_review_length_data(connection):
    """
    Return review length along with rating and sentiment.
    Useful for analytics charts.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,
            rating,
            own_rating AS sentiment,
            CHAR_LENGTH(review_text) AS review_length
        FROM feedback
        WHERE review_text IS NOT NULL
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# NEGATIVE REVIEW DATA
# ============================================================

def get_negative_reviews(connection):
    """
    Return all negative reviews.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            unique_id,
            category,
            review_header,
            review_text,
            rating,
            own_rating
        FROM feedback
        WHERE own_rating = 'Negative'
        ORDER BY rating ASC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# TOP CATEGORIES
# ============================================================

def get_top_categories(connection, limit=5):
    """
    Return categories with the highest number of reviews.
    """

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            category,
            COUNT(*) AS total_reviews
        FROM feedback
        GROUP BY category
        ORDER BY total_reviews DESC
        LIMIT %s
    """

    cursor.execute(query, (limit,))

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# MOST NEGATIVE CATEGORIES
# ============================================================

def get_negative_categories(connection):
    """
    Return categories ranked by number of negative reviews.
    """

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            category,

            COUNT(*) AS total_reviews,

            SUM(
                CASE
                    WHEN own_rating = 'Negative'
                    THEN 1
                    ELSE 0
                END
            ) AS negative_reviews

        FROM feedback

        GROUP BY category

        ORDER BY negative_reviews DESC
    """)

    result = cursor.fetchall()

    cursor.close()

    return result


# ============================================================
# DATAFRAME HELPER
# ============================================================

def get_category_performance_dataframe(connection):
    """
    Return category performance as a pandas DataFrame.

    Useful for Streamlit charts and analytics.
    """

    data = get_category_performance(connection)

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame(data)

    # Convert database numeric values to numeric types
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

    # Calculate percentages
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