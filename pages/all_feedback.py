# pages/all_feedback.py

import streamlit as st
import pandas as pd
from database.db import get_connection
from utils.data import load_feedback_frame
from utils.ui import apply_theme, metric_card, page_header


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="All Feedback",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# CUSTOM CSS FOR MATCHING DARK UI DESIGN
# ============================================================

st.markdown(
    """
    <style>
    /* Global Page Styling */
    .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Page Header */
    .page-title {
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }

    .page-subtitle {
        font-size: 13px;
        color: #8b949e;
        margin-bottom: 20px;
    }

    /* Top KPI Cards Grid */
    .kpi-card {
        background: #161b22;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    
    .kpi-title {
        font-size: 12px;
        font-weight: 600;
        color: #8b949e;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
    }

    .kpi-subtext {
        font-size: 10px;
        color: #6e7681;
        margin-top: 4px;
    }

    /* Specific Metric Highlight Borders */
    .card-total { border-left: 3px solid #388bfd; }
    .card-pos { border-left: 3px solid #238636; }
    .card-neu { border-left: 3px solid #d29922; }
    .card-neg { border-left: 3px solid #da3633; }

    /* Custom Container Box */
    .panel-box {
        background: #161b22;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }

    .panel-title {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 12px;
    }

    .record-count-text {
        font-size: 13px;
        color: #8b949e;
        margin-bottom: 10px;
        font-weight: 500;
    }

    /* Streamlit Dataframe Dark UI Tweaks */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        background-color: #161b22;
    }

    /* Button Customizations */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
apply_theme()


# ============================================================
# LOAD DATA FROM MYSQL
# ============================================================

@st.cache_data
def load_feedback():
    data, error = load_feedback_frame(order="DESC")
    if error:
        return None
    return data


df = load_feedback()


# ============================================================
# DATABASE ERROR
# ============================================================

if df is None:

    st.error(
        "Unable to load feedback data from the MySQL database."
    )

    st.stop()


# ============================================================
# EMPTY DATA
# ============================================================

if df.empty:

    st.warning(
        "No feedback data available."
    )

    st.info(
        "Submit customer feedback to start building your feedback database."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    page_header(
        "All Customer Feedback",
        "Explore, search and analyze customer feedback records"
    )

with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True):
        load_feedback.clear()
        st.rerun()


# ============================================================
# FILTER SIDEBAR / TOP PANELS & APPLIED FILTERING
# ============================================================

df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["category"] = df["category"].fillna("Unknown").astype(str)
df["own_rating"] = df["own_rating"].fillna("Unknown").astype(str)
df["predicted_sentiment"] = df["predicted_sentiment"].fillna("Unknown").astype(str)
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

# Filter layout with Left Column for Filters and Right Column for Content
main_left, main_right = st.columns([1, 3.2], gap="large")

with main_left:
    st.markdown("### 🔎 Filters")

    # ------------------------------------------------------------
    # CATEGORY FILTER
    # ------------------------------------------------------------
    category_options = sorted(
        df["category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    category_filter = st.multiselect(
        "Product Category",
        options=category_options,
        default=category_options
    )

    # ------------------------------------------------------------
    # RATING FILTER
    # ------------------------------------------------------------
    rating_filter = st.slider(
        "Rating Range",
        min_value=1,
        max_value=5,
        value=(1, 5),
        step=1
    )

    # ------------------------------------------------------------
    # SENTIMENT FILTER
    # ------------------------------------------------------------
    sentiment_options = [
        "Positive",
        "Neutral",
        "Negative"
    ]

    available_sentiments = [
        sentiment
        for sentiment in sentiment_options
        if sentiment in df["own_rating"].dropna().unique()
    ]

    sentiment_filter = st.multiselect(
        "Customer Sentiment",
        options=available_sentiments,
        default=available_sentiments
    )

    # ------------------------------------------------------------
    # PREDICTED SENTIMENT FILTER
    # ------------------------------------------------------------
    prediction_options = [
        "Positive",
        "Neutral",
        "Negative"
    ]

    available_predictions = [
        sentiment
        for sentiment in prediction_options
        if sentiment in df["predicted_sentiment"].dropna().unique()
    ]

    prediction_filter = st.multiselect(
        "Predicted Sentiment",
        options=available_predictions,
        default=available_predictions
    )


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

# Customer sentiment
if sentiment_filter:
    filtered_df = filtered_df[
        filtered_df["own_rating"].isin(
            sentiment_filter
        )
    ]

# Rating
filtered_df = filtered_df[
    (filtered_df["rating"] >= rating_filter[0])
    &
    (filtered_df["rating"] <= rating_filter[1])
]

# Category
if category_filter:
    filtered_df = filtered_df[
        filtered_df["category"].isin(
            category_filter
        )
    ]

# Predicted sentiment
if prediction_filter:
    filtered_df = filtered_df[
        filtered_df["predicted_sentiment"].isin(
            prediction_filter
        )
    ]


# ============================================================
# MAIN RIGHT CONTENT AREA (KPI CARDS & FEEDBACK TABLE)
# ============================================================

with main_right:

    # ------------------------------------------------------------
    # KPI TOP SUMMARY METRICS
    # ------------------------------------------------------------
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)

    total_cnt = len(df)
    pos_cnt = (filtered_df["own_rating"] == "Positive").sum() if not filtered_df.empty else 0
    neu_cnt = (filtered_df["own_rating"] == "Neutral").sum() if not filtered_df.empty else 0
    neg_cnt = (filtered_df["own_rating"] == "Negative").sum() if not filtered_df.empty else 0

    with sum_col1:
        metric_card("Total Feedback", f"{total_cnt:,}", "Overall database entries", "blue")

    with sum_col2:
        metric_card("Positive Feedback", f"{pos_cnt:,}", "Based on own_rating", "green")

    with sum_col3:
        metric_card("Neutral Feedback", f"{neu_cnt:,}", "Based on own_rating", "yellow")

    with sum_col4:
        metric_card("Negative Feedback", f"{neg_cnt:,}", "Based on own_rating", "red")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------------------
    # RESULT COUNT & EXPORT BAR
    # ------------------------------------------------------------
    res_col1, res_col2 = st.columns([3, 1])

    with res_col1:
        st.markdown(
            f'<div class="record-count-text">Showing {len(filtered_df)} of {len(df)} records</div>',
            unsafe_allow_html=True
        )

    with res_col2:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name="filtered_feedback.csv",
            mime="text/csv",
            use_container_width=True
        )

    # ------------------------------------------------------------
    # FEEDBACK TABLE
    # ------------------------------------------------------------
    if filtered_df.empty:
        st.info("No feedback matches the selected filters.")
    else:
        display_df = filtered_df[
            [
                "feedback_id",
                "unique_id",
                "category",
                "review_header",
                "rating",
                "own_rating",
                "predicted_sentiment",
                "created_at"
            ]
        ].copy()

        display_df = display_df.rename(
            columns={
                "feedback_id": "ID",
                "unique_id": "Unique ID",
                "category": "Category",
                "review_header": "Review Header",
                "rating": "Rating",
                "own_rating": "Customer Sentiment",
                "predicted_sentiment": "Predicted Sentiment",
                "created_at": "Created At"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Rating": st.column_config.NumberColumn(
                    "Rating ⭐",
                    min_value=1,
                    max_value=5,
                    format="%d ⭐"
                ),
                "Customer Sentiment": st.column_config.TextColumn(
                    "Customer Sentiment"
                ),
                "Predicted Sentiment": st.column_config.TextColumn(
                    "Predicted Sentiment"
                ),
                "Created At": st.column_config.DatetimeColumn(
                    "Created At",
                    format="DD MMM YYYY, HH:mm"
                )
            }
        )


# ============================================================
# REVIEW DETAILS & MANAGEMENT
# ============================================================

st.markdown("---")

det_col1, det_col2 = st.columns(2, gap="large")

with det_col1:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🔍 Review Details</div>', unsafe_allow_html=True)

    if not filtered_df.empty:
        selected_id = st.selectbox(
            "Select a feedback record",
            filtered_df["feedback_id"].tolist()
        )

        selected_feedback = filtered_df[
            filtered_df["feedback_id"] == selected_id
        ].iloc[0]

        st.markdown(f"**Unique ID:** `{selected_feedback['unique_id']}`")
        st.markdown(f"**Category:** `{selected_feedback['category']}`")
        st.markdown(f"**Review Header:** {selected_feedback['review_header']}")
        st.markdown(f"**Rating:** {selected_feedback['rating']} / 5 ⭐")

        st.markdown("---")
        st.markdown("**Customer Review:**")
        st.write(selected_feedback["review_text"])

        st.markdown("---")
        customer_sentiment = selected_feedback["own_rating"]
        predicted_sentiment = selected_feedback["predicted_sentiment"]

        st.markdown(f"**Customer Sentiment:** `{customer_sentiment if pd.notna(customer_sentiment) else 'Not Available'}`")
        st.markdown(f"**Predicted Sentiment:** `{predicted_sentiment if pd.notna(predicted_sentiment) else 'Not Available'}`")
        st.markdown(f"**Created At:** {selected_feedback['created_at']}")
    else:
        st.write("No feedback selected.")

    st.markdown('</div>', unsafe_allow_html=True)


with det_col2:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🗑️ Delete Feedback Record</div>', unsafe_allow_html=True)
    st.warning("Deleting a feedback record is permanent.")

    delete_id = st.number_input(
        "Enter Feedback ID",
        min_value=1,
        step=1,
        value=1
    )

    if st.button(
        "🗑️ Delete Feedback",
        type="primary",
        use_container_width=True
    ):
        connection = get_connection()

        if connection is None:
            st.error("Unable to connect to MySQL.")
        else:
            try:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    DELETE FROM feedback
                    WHERE feedback_id = %s
                    """,
                    (delete_id,)
                )

                if cursor.rowcount == 0:
                    st.warning(f"No feedback found with ID {delete_id}.")
                else:
                    connection.commit()
                    st.success(f"Feedback {delete_id} deleted successfully.")

                    # Clear cached data
                    load_feedback.clear()

                    st.rerun()

                cursor.close()
                connection.close()

            except Exception:
                try:
                    connection.rollback()
                except Exception:
                    pass

                try:
                    connection.close()
                except Exception:
                    pass

                st.error("Unable to delete the feedback record.")

    st.markdown('</div>', unsafe_allow_html=True)
