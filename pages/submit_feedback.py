# pages/submit_feedback.py

import streamlit as st
from database.db import get_connection
from nlp.predict import predict_sentiment
from utils.ui import apply_theme, page_header

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Submit Feedback | Retail Feedback Analyzer",
    page_icon="📝",
    layout="wide"
)

# ============================================================
# CUSTOM CSS (MATCHING UI IMAGE SPECIFICATIONS)
# ============================================================

st.markdown(
    """
    <style>
    /* Global Page Dark Theme & Glassmorphism */
    .stApp {
        background-color: #0B0E17 !important;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(30, 41, 89, 0.35) 0%, transparent 40%),
            radial-gradient(circle at 90% 90%, rgba(76, 29, 149, 0.25) 0%, transparent 40%);
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Hide default header spacing */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Header Styling */
    .header-title {
        font-size: 26px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.3px;
        margin-bottom: 2px;
    }

    .header-subtitle {
        font-size: 13px;
        color: #94A3B8;
        margin-bottom: 24px;
    }

    /* Form Card Container (Dark Translucent Box) */
    div[data-testid="stForm"] {
        background: rgba(18, 22, 36, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 24px 28px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }

    /* Section Titles inside Form */
    .form-section-title {
        font-size: 16px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 2px;
    }

    .form-section-desc {
        font-size: 12px;
        color: #64748B;
        margin-bottom: 18px;
    }

    /* Input Fields Styling */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        background-color: rgba(10, 14, 26, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 6px !important;
        color: #F8FAFC !important;
        font-size: 13px !important;
    }

    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* Input Field Labels */
    label, div[data-testid="stWidgetLabel"] p {
        color: #CBD5E1 !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        margin-bottom: 4px !important;
    }

    /* Primary Submit Button Styling (Purple/Blue Gradient) */
    div[data-testid="stForm"] button[type="submit"] {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.2s ease-in-out !important;
    }

    div[data-testid="stForm"] button[type="submit"]:hover {
        opacity: 0.92 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.45) !important;
    }

    /* Custom Right Panel Card */
    .prediction-card {
        background: rgba(18, 22, 36, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .prediction-header {
        font-size: 15px;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 2px;
    }

    .prediction-subtext {
        font-size: 12px;
        color: #64748B;
        margin-bottom: 16px;
    }

    /* Result Box inside Right Panel */
    .sentiment-result-box {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }

    .sentiment-result-title {
        font-size: 12px;
        font-weight: 500;
        color: #94A3B8;
        margin-bottom: 8px;
    }

    .sentiment-value-positive {
        color: #10B981;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    .sentiment-value-negative {
        color: #EF4444;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    .sentiment-value-neutral {
        color: #F59E0B;
        font-size: 22px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    /* Metric Display Panel */
    .metric-summary-card {
        background: rgba(18, 22, 36, 0.75);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 10px;
        padding: 16px;
        margin-top: 15px;
    }

    .metric-summary-header {
        font-size: 13px;
        font-weight: 600;
        color: #10B981;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .metric-item {
        font-size: 12px;
        color: #CBD5E1;
        margin-bottom: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
apply_theme()

# ============================================================
# HEADER
# ============================================================

page_header(
    "Submit Feedback",
    "Capture customer feedback and analyze sentiment instantly"
)

# ============================================================
# GET CATEGORIES FROM MYSQL
# ============================================================

connection = get_connection()

if connection is None:
    st.error("Unable to connect to the MySQL database.")
    st.stop()

try:
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT DISTINCT category
        FROM feedback
        WHERE category IS NOT NULL
          AND category != ''
        ORDER BY category
        """
    )

    categories = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

except Exception as e:
    connection.close()
    st.error("Unable to load product categories.")
    st.stop()

# ============================================================
# TWO-COLUMN LAYOUT (FORM ON LEFT, PREDICTION ON RIGHT)
# ============================================================

col_form, col_side = st.columns([1.8, 1])

# ------------------------------------------------------------
# LEFT COLUMN: FEEDBACK FORM
# ------------------------------------------------------------

with col_form:
    with st.form("feedback_form"):

        st.markdown('<div class="form-section-title">Customer Feedback</div>', unsafe_allow_html=True)
        st.markdown('<div class="form-section-desc">Enter the customer\'s review details below.</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # --------------------------------------------------------
        # UNIQUE ID
        # --------------------------------------------------------
        with col1:
            unique_id = st.text_input(
                "Unique ID *",
                placeholder="Enter unique customer feedback ID"
            )

        # --------------------------------------------------------
        # CATEGORY
        # --------------------------------------------------------
        with col2:
            if categories:
                category = st.selectbox(
                    "Product Category *",
                    categories
                )
            else:
                category = st.text_input(
                    "Product Category *",
                    placeholder="Select category..."
                )

        # --------------------------------------------------------
        # REVIEW HEADER
        # --------------------------------------------------------
        review_header = st.text_input(
            "Review Title",
            placeholder="Write a short title for your review"
        )

        # --------------------------------------------------------
        # REVIEW TEXT
        # --------------------------------------------------------
        review_text = st.text_area(
            "Customer Review *",
            placeholder="Tell us about your experience with the product...",
            height=140
        )

        # --------------------------------------------------------
        # RATING
        # --------------------------------------------------------
        st.markdown('<div class="form-section-title" style="margin-top:10px;">Customer Rating</div>', unsafe_allow_html=True)

        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=5,
            step=1
        )

        rating_labels = {
            1: "⭐ Very Poor (1/5)",
            2: "⭐⭐ Poor (2/5)",
            3: "⭐⭐⭐ Average (3/5)",
            4: "⭐⭐⭐⭐ Good (4/5)",
            5: "⭐⭐⭐⭐⭐ Excellent (5/5)"
        }

        st.caption(rating_labels[rating])

        st.markdown("")

        submitted = st.form_submit_button(
            "Analyze & Submit Feedback",
            use_container_width=True
        )

# ------------------------------------------------------------
# RIGHT COLUMN: PREDICTION DISPLAY & RESULTS
# ------------------------------------------------------------

with col_side:
    st.markdown('<div class="prediction-header">Prediction Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="prediction-subtext">Specify the customer\'s stated sentiment analysis model.</div>', unsafe_allow_html=True)

    # Initialize placeholders for submission results
    result_container = st.container()

    with result_container:
        st.markdown(
            """
            <div class="prediction-card">
                <div class="sentiment-result-box">
                    <div class="sentiment-result-title">Sentiment Prediction</div>
                    <div style="color: #64748B; font-size: 14px; margin-top: 10px;">
                        Submit feedback to generate real-time NLP sentiment prediction.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ============================================================
# SUBMIT FEEDBACK PROCESSING
# ============================================================

if submitted:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not unique_id.strip():
        st.error("Please enter the Unique ID.")
        st.stop()

    if not category or not category.strip():
        st.error("Please select or enter a product category.")
        st.stop()

    if not review_text.strip():
        st.error("Please enter the review text.")
        st.stop()

    # --------------------------------------------------------
    # SENTIMENT PREDICTION
    # --------------------------------------------------------

    with st.spinner("Analyzing customer sentiment..."):

        try:
            predicted_sentiment = predict_sentiment(
                review_text.strip()
            )

        except Exception as e:
            st.error(
                "Unable to analyze sentiment. "
                "Please check the NLP model."
            )
            st.stop()

    # --------------------------------------------------------
    # NORMALIZE SENTIMENT
    # --------------------------------------------------------

    if predicted_sentiment:
        predicted_sentiment = str(
            predicted_sentiment
        ).strip().capitalize()
    else:
        predicted_sentiment = None

    # --------------------------------------------------------
    # VALID SENTIMENT CHECK
    # --------------------------------------------------------

    valid_sentiments = {
        "Positive",
        "Neutral",
        "Negative"
    }

    if predicted_sentiment not in valid_sentiments:
        st.error(
            "The sentiment model returned an invalid result."
        )
        st.stop()

    # ========================================================
    # INSERT INTO MYSQL
    # ========================================================

    connection = get_connection()

    if connection is None:
        st.error(
            "Unable to connect to the MySQL database."
        )
        st.stop()

    try:

        cursor = connection.cursor()
        cursor.execute("DESCRIBE feedback")
        existing_columns = {row[0] for row in cursor.fetchall()}

        # ----------------------------------------------------
        # CHECK DUPLICATE UNIQUE ID
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT feedback_id
            FROM feedback
            WHERE unique_id = %s
            """,
            (unique_id.strip(),)
        )

        existing_record = cursor.fetchone()

        if existing_record:
            st.error(
                f"Feedback ID {unique_id.strip()} already exists."
            )

            cursor.close()
            connection.close()

            st.stop()

        # ----------------------------------------------------
        # INSERT FEEDBACK
        # ----------------------------------------------------

        insert_values = {
            "unique_id": unique_id.strip(),
            "category": category.strip(),
            "review_header": review_header.strip(),
            "review_text": review_text.strip(),
            "rating": rating,
            "own_rating": predicted_sentiment if "predicted_sentiment" not in existing_columns else None,
            "predicted_sentiment": predicted_sentiment,
        }

        insert_columns = [
            column
            for column in insert_values
            if column in existing_columns
        ]

        placeholders = ", ".join(["%s"] * len(insert_columns))
        query = f"""
            INSERT INTO feedback ({", ".join(insert_columns)})
            VALUES ({placeholders})
        """

        values = tuple(insert_values[column] for column in insert_columns)

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()
        connection.close()

        # ====================================================
        # UPDATE RIGHT PANEL DISPLAY ON SUCCESS
        # ====================================================

        with result_container:
            sentiment_emoji = "😃" if predicted_sentiment == "Positive" else ("😞" if predicted_sentiment == "Negative" else "😐")
            sentiment_class = f"sentiment-value-{predicted_sentiment.lower()}"

            st.markdown(
                f"""
                <div class="prediction-card">
                    <div class="sentiment-result-box">
                        <div class="sentiment-result-title">Sentiment Prediction</div>
                        <div class="{sentiment_class}">
                            <span>{sentiment_emoji}</span> {predicted_sentiment}
                        </div>
                        <div style="color: #64748B; font-size: 11px; margin-top: 6px;">
                            Prediction generated by the sentiment analysis model
                        </div>
                    </div>

                    <div class="metric-summary-card">
                        <div class="metric-summary-header">
                            ✓ Feedback Submitted
                        </div>
                        <div class="metric-item"><b>ID:</b> {unique_id.strip()}</div>
                        <div class="metric-item"><b>Category:</b> {category.strip()}</div>
                        <div class="metric-item"><b>Rating:</b> {"★" * rating}{"☆" * (5 - rating)}</div>
                        <div class="metric-item"><b>Predicted Sentiment:</b> {sentiment_emoji} {predicted_sentiment}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.success("✓ Feedback submitted successfully")

        # ----------------------------------------------------
        # SENTIMENT MESSAGE
        # ----------------------------------------------------

        if predicted_sentiment == "Positive":
            st.success(
                "😊 The NLP model classified this review as Positive."
            )

        elif predicted_sentiment == "Negative":
            st.error(
                "😞 The NLP model classified this review as Negative."
            )

        else:
            st.warning(
                "😐 The NLP model classified this review as Neutral."
            )

    except Exception as e:

        try:
            connection.rollback()
        except Exception:
            pass

        try:
            cursor.close()
        except Exception:
            pass

        try:
            connection.close()
        except Exception:
            pass

        st.error(
            "❌ Unable to save the feedback. Please try again."
        )
