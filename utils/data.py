import pandas as pd

from database.db import get_connection


FEEDBACK_COLUMNS = [
    "feedback_id",
    "unique_id",
    "category",
    "review_header",
    "review_text",
    "rating",
    "own_rating",
    "predicted_sentiment",
    "created_at",
]


def load_feedback_frame(order="DESC"):
    connection = get_connection()

    if connection is None:
        return None, "Unable to connect to the MySQL database."

    try:
        cursor = connection.cursor()
        cursor.execute("DESCRIBE feedback")
        existing_columns = {row[0] for row in cursor.fetchall()}
        cursor.close()

        selected_columns = [column for column in FEEDBACK_COLUMNS if column in existing_columns]
        if not selected_columns:
            connection.close()
            return pd.DataFrame(columns=FEEDBACK_COLUMNS), None

        order = "ASC" if str(order).upper() == "ASC" else "DESC"
        order_clause = f"ORDER BY created_at {order}" if "created_at" in existing_columns else ""
        query = f"SELECT {', '.join(selected_columns)} FROM feedback {order_clause}"
        df = pd.read_sql(query, connection)
        connection.close()

        for column in FEEDBACK_COLUMNS:
            if column not in df.columns:
                df[column] = None

        df = df[FEEDBACK_COLUMNS]
        df["category"] = df["category"].fillna("Unknown").astype(str)
        df["review_text"] = df["review_text"].fillna("").astype(str)
        df["review_header"] = df["review_header"].fillna("").astype(str)
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

        if df["predicted_sentiment"].isna().all() and "own_rating" in df:
            df["predicted_sentiment"] = df["own_rating"]

        df["own_rating"] = df["own_rating"].fillna("Unknown").astype(str)
        df["predicted_sentiment"] = df["predicted_sentiment"].fillna("Unknown").astype(str)

        return df, None

    except Exception as error:
        try:
            connection.close()
        except Exception:
            pass
        return None, f"Unable to load feedback data: {error}"
