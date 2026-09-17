import os
import pandas as pd
from database.db import get_connection


CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "../data/feedback.csv"
)


def import_feedback():

    # -----------------------------
    # Read CSV
    # -----------------------------
    df = pd.read_csv(CSV_PATH)

    print(f"CSV loaded: {len(df)} records")

    # -----------------------------
    # Handle missing values
    # -----------------------------
    df["Review_text"] = df["Review_text"].fillna("")
    df["Review_Header"] = df["Review_Header"].fillna("")
    df["Category"] = df["Category"].fillna("")
    df["Own_Rating"] = df["Own_Rating"].fillna("")

    # -----------------------------
    # Database connection
    # -----------------------------
    connection = get_connection()

    if connection is None:
        print("Database connection failed.")
        return

    cursor = connection.cursor()

    query = """
        INSERT INTO feedback
        (
            unique_id,
            category,
            review_header,
            review_text,
            rating,
            own_rating
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                str(row["Unique_ID"]),
                row["Category"],
                row["Review_Header"],
                row["Review_text"],
                int(row["Rating"]),
                row["Own_Rating"]
            )
        )

    # -----------------------------
    # Insert records
    # -----------------------------
    cursor.executemany(query, records)

    connection.commit()

    print(f"{cursor.rowcount} records inserted successfully.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    import_feedback()