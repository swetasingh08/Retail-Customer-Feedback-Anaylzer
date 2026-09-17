# pages/analytics.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from nlp.preprocess import preprocess_text
from utils.data import load_feedback_frame
from utils.ui import apply_theme, bar_chart, donut_chart, metric_card, page_header, plotly_layout


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)


apply_theme()


# ============================================================
# HEADER
# ============================================================

page_header(
    "Analytics",
    "Understand customer sentiment, ratings and product performance through data-driven insights."
)


# ============================================================
# LOAD DATA FROM MYSQL
# ============================================================

@st.cache_data
def load_feedback():
    data, error = load_feedback_frame(order="ASC")
    if error:
        st.error(error)
        return pd.DataFrame()
    return data


df = load_feedback()


# ============================================================
# EMPTY DATA
# ============================================================

if df.empty:

    st.warning(
        "No feedback data available for analytics."
    )

    st.stop()


# ============================================================
# DATA CLEANING
# ============================================================

df["review_text"] = (
    df["review_text"]
    .fillna("")
    .astype(str)
)

df["category"] = (
    df["category"]
    .fillna("Unknown")
    .astype(str)
)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["created_at"] = pd.to_datetime(
    df["created_at"],
    errors="coerce"
)


# ============================================================
# ANALYTICS TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "😊 Sentiment",
        "💡 Topics",
        "📊 Trends",
        "☁️ Word Cloud"
    ]
)


# ============================================================
# TAB 1 — SENTIMENT ANALYSIS
# ============================================================

with tab1:

    st.subheader(
        "😊 Sentiment Analysis"
    )

    # --------------------------------------------------------
    # Select sentiment source
    # --------------------------------------------------------

    sentiment_source = st.radio(
        "Sentiment Source",
        [
            "AI Predicted Sentiment",
            "Dataset Sentiment"
        ],
        horizontal=True
    )


    if sentiment_source == "AI Predicted Sentiment":

        sentiment_column = "predicted_sentiment"

    else:

        sentiment_column = "own_rating"


    sentiment_df = df[
        df[sentiment_column].notna()
    ].copy()


    # --------------------------------------------------------
    # Sentiment counts
    # --------------------------------------------------------

    sentiment_order = [
        "Positive",
        "Neutral",
        "Negative"
    ]

    sentiment_counts = (
        sentiment_df[sentiment_column]
        .value_counts()
        .reindex(
            sentiment_order,
            fill_value=0
        )
    )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    total = len(sentiment_df)

    positive = int(
        sentiment_counts.get(
            "Positive",
            0
        )
    )

    neutral = int(
        sentiment_counts.get(
            "Neutral",
            0
        )
    )

    negative = int(
        sentiment_counts.get(
            "Negative",
            0
        )
    )


    positive_pct = (
        positive / total * 100
        if total > 0
        else 0
    )

    neutral_pct = (
        neutral / total * 100
        if total > 0
        else 0
    )

    negative_pct = (
        negative / total * 100
        if total > 0
        else 0
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:
        metric_card("Total Reviews", f"{total:,}", "Comparable records", "blue")


    with col2:
        metric_card("Positive %", f"{positive_pct:.1f}%", f"{positive:,} reviews", "green")


    with col3:
        metric_card("Neutral %", f"{neutral_pct:.1f}%", f"{neutral:,} reviews", "yellow")


    with col4:
        metric_card("Negative %", f"{negative_pct:.1f}%", f"{negative:,} reviews", "red")


    # --------------------------------------------------------
    # Sentiment charts
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.markdown('<div class="section-title">Customer Sentiment Distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(donut_chart(sentiment_counts.index, sentiment_counts.values), use_container_width=True)


    with col2:

        st.markdown('<div class="section-title">Sentiment Percentage</div>', unsafe_allow_html=True)
        sentiment_percentage = sentiment_counts / total * 100 if total > 0 else sentiment_counts * 0
        sentiment_percent_df = sentiment_percentage.reset_index()
        sentiment_percent_df.columns = ["Sentiment", "Percentage"]
        st.plotly_chart(bar_chart(sentiment_percent_df, "Sentiment", "Percentage", color="Sentiment"), use_container_width=True)


    # --------------------------------------------------------
    # Sentiment by Category
    # --------------------------------------------------------

    st.markdown('<div class="section-title">Sentiment by Product Category</div>', unsafe_allow_html=True)

    sentiment_category = pd.crosstab(
        sentiment_df["category"],
        sentiment_df[sentiment_column]
    )


    for sentiment in sentiment_order:

        if sentiment not in sentiment_category.columns:

            sentiment_category[sentiment] = 0


    sentiment_category = sentiment_category[
        sentiment_order
    ]


    sentiment_category_plot = sentiment_category.reset_index().melt(
        id_vars="category", var_name="Sentiment", value_name="Reviews"
    )
    st.plotly_chart(bar_chart(sentiment_category_plot, "category", "Reviews", color="Sentiment", height=340), use_container_width=True)


    # --------------------------------------------------------
    # Sentiment table
    # --------------------------------------------------------

    st.subheader(
        "Sentiment Summary"
    )

    summary = pd.DataFrame(
        {
            "Sentiment": sentiment_order,
            "Count": [
                sentiment_counts[s]
                for s in sentiment_order
            ],
            "Percentage": [
                f"{sentiment_counts[s] / total * 100:.1f}%"
                if total > 0
                else "0%"
                for s in sentiment_order
            ]
        }
    )

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 2 — TOPIC ANALYSIS
# ============================================================

with tab2:

    st.subheader(
        "💡 Topic & Review Analysis"
    )


    # --------------------------------------------------------
    # Preprocess review text
    # --------------------------------------------------------

    with st.spinner(
        "Processing customer reviews..."
    ):

        try:

            processed_text = (
                df["review_text"]
                .apply(preprocess_text)
            )

        except Exception:

            processed_text = (
                df["review_text"]
                .str.lower()
            )


    all_words = " ".join(
        processed_text
        .dropna()
        .astype(str)
    )


    # --------------------------------------------------------
    # Top words
    # --------------------------------------------------------

    if all_words.strip():

        word_frequency = (
            pd.Series(
                all_words.split()
            )
            .value_counts()
            .head(20)
        )

        st.markdown('<div class="section-title">Top 20 Words</div>', unsafe_allow_html=True)
        word_df = word_frequency.reset_index()
        word_df.columns = ["Word", "Count"]
        st.plotly_chart(bar_chart(word_df, "Count", "Word", orientation="h", height=420), use_container_width=True)

    else:

        st.info(
            "Not enough review text to generate word frequency."
        )


    # --------------------------------------------------------
    # Review length
    # --------------------------------------------------------

    st.markdown('<div class="section-title">Review Length Distribution</div>', unsafe_allow_html=True)

    df["word_count"] = (
        df["review_text"]
        .apply(
            lambda x: len(
                str(x).split()
            )
        )
    )


    # Create bins

    length_bins = pd.cut(
        df["word_count"],
        bins=[
            -1,
            10,
            25,
            50,
            100,
            250,
            500,
            float("inf")
        ],
        labels=[
            "0-10",
            "11-25",
            "26-50",
            "51-100",
            "101-250",
            "251-500",
            "500+"
        ]
    )


    length_distribution = (
        length_bins
        .value_counts()
        .sort_index()
    )


    length_df = length_distribution.reset_index()
    length_df.columns = ["Length", "Reviews"]
    st.plotly_chart(bar_chart(length_df, "Length", "Reviews"), use_container_width=True)


    # --------------------------------------------------------
    # Average review length by category
    # --------------------------------------------------------

    st.markdown('<div class="section-title">Average Review Length by Category</div>', unsafe_allow_html=True)


    category_length = (
        df.groupby("category")["word_count"]
        .mean()
        .sort_values(
            ascending=False
        )
        .round(1)
    )


    length_cat_df = category_length.reset_index()
    length_cat_df.columns = ["Category", "Average Words"]
    st.plotly_chart(bar_chart(length_cat_df, "Average Words", "Category", orientation="h"), use_container_width=True)


# ============================================================
# TAB 3 — TREND ANALYSIS
# ============================================================

with tab3:

    st.subheader(
        "📊 Feedback Trends"
    )


    trend_df = df.dropna(
        subset=["created_at"]
    ).copy()


    if trend_df.empty:

        st.info(
            "Created date information is not available."
        )

    else:

        trend_df["date"] = (
            trend_df["created_at"]
            .dt.date
        )


        # ----------------------------------------------------
        # Daily feedback volume
        # ----------------------------------------------------

        st.subheader(
            "💬 Daily Feedback Volume"
        )

        daily_feedback = (
            trend_df
            .groupby("date")
            .size()
        )


        st.line_chart(daily_feedback, use_container_width=True)


        # ----------------------------------------------------
        # Average rating
        # ----------------------------------------------------

        st.subheader(
            "⭐ Average Rating Over Time"
        )

        daily_rating = (
            trend_df
            .groupby("date")["rating"]
            .mean()
            .round(2)
        )


        st.line_chart(daily_rating, use_container_width=True)


        # ----------------------------------------------------
        # Sentiment trends
        # ----------------------------------------------------

        st.subheader(
            "😊 Sentiment Trends"
        )


        sentiment_trends = pd.crosstab(
            trend_df["date"],
            trend_df["predicted_sentiment"]
        )


        for sentiment in [
            "Positive",
            "Neutral",
            "Negative"
        ]:

            if sentiment not in sentiment_trends.columns:

                sentiment_trends[sentiment] = 0


        sentiment_trends = sentiment_trends[
            [
                "Positive",
                "Neutral",
                "Negative"
            ]
        ]


        st.line_chart(sentiment_trends, use_container_width=True)


        # ----------------------------------------------------
        # Category trends
        # ----------------------------------------------------

        st.subheader(
            "📦 Feedback Volume by Category"
        )


        category_trends = pd.crosstab(
            trend_df["date"],
            trend_df["category"]
        )


        st.line_chart(category_trends, use_container_width=True)


# ============================================================
# TAB 4 — WORD CLOUD
# ============================================================

with tab4:

    st.subheader(
        "☁️ Customer Review Word Cloud"
    )


    try:

        from wordcloud import WordCloud


        text = " ".join(
            df["review_text"]
            .dropna()
            .astype(str)
        )


        if not text.strip():

            st.info(
                "No review text available for word cloud."
            )

        else:

            wordcloud = WordCloud(
                width=1200,
                height=600,
                background_color="white",
                max_words=100,
                collocations=False
            ).generate(text)


            fig, ax = plt.subplots(
                figsize=(14, 7)
            )

            ax.imshow(
                wordcloud,
                interpolation="bilinear"
            )

            ax.axis("off")

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)


    except ImportError:

        st.warning(
            "WordCloud is not installed."
        )

        st.code(
            "pip install wordcloud"
        )


# ============================================================
# DATASET VS AI COMPARISON
# ============================================================

st.markdown("---")

st.subheader(
    "🤖 Dataset Sentiment vs AI Prediction"
)


comparison_df = df.dropna(
    subset=[
        "own_rating",
        "predicted_sentiment"
    ]
).copy()


if not comparison_df.empty:

    comparison_table = pd.crosstab(
        comparison_df["own_rating"],
        comparison_df["predicted_sentiment"]
    )


    st.dataframe(
        comparison_table,
        use_container_width=True
    )


    # --------------------------------------------------------
    # Prediction agreement
    # --------------------------------------------------------

    agreement = (
        comparison_df["own_rating"]
        ==
        comparison_df["predicted_sentiment"]
    ).mean() * 100


    st.metric(
        "Model Agreement with Dataset Sentiment",
        f"{agreement:.2f}%"
    )


else:

    st.info(
        "Dataset sentiment and AI prediction are not both "
        "available for enough records to calculate agreement."
    )
