import streamlit as st
import pandas as pd
from utils.data import load_feedback_frame
from utils.ui import apply_theme, bar_chart, donut_chart, metric_card, page_header

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

apply_theme()

df, load_error = load_feedback_frame(order="DESC")

if load_error:
    st.error(load_error)
    st.stop()

if df.empty:
    st.warning("No feedback data available.")
    st.stop()

# ---------------------------------------------------------
# Data Cleaning & Pre-processing
# ---------------------------------------------------------
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["category"] = df["category"].fillna("Unknown")
df["own_rating"] = df["own_rating"].fillna("Neutral")

# ---------------------------------------------------------
# Top Header Block
# ---------------------------------------------------------
page_header(
    "Dashboard",
    "Monitor customer feedback, sentiment and product category performance.",
    "Live data - MySQL"
)

# ---------------------------------------------------------
# Calculations for KPI Cards
# ---------------------------------------------------------
total_reviews = len(df)
avg_rating = df["rating"].mean() if total_reviews > 0 else 0

positive_cnt = (df["own_rating"] == "Positive").sum()
neutral_cnt = (df["own_rating"] == "Neutral").sum()
negative_cnt = (df["own_rating"] == "Negative").sum()

pos_pct = (positive_cnt / total_reviews * 100) if total_reviews > 0 else 0
neu_pct = (neutral_cnt / total_reviews * 100) if total_reviews > 0 else 0
neg_pct = (negative_cnt / total_reviews * 100) if total_reviews > 0 else 0

# ---------------------------------------------------------
# Top KPI Metric Cards Grid
# ---------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    metric_card("Total Reviews", f"{total_reviews:,}", "Overall feedback records", "blue")

with col2:
    metric_card("Average Rating", f"{avg_rating:.1f} / 5", "Across all categories", "yellow")

with col3:
    metric_card("Positive Sentiment", f"{pos_pct:.1f}%", f"{positive_cnt:,} positive reviews", "green")

with col4:
    metric_card("Neutral Sentiment", f"{neu_pct:.1f}%", f"{neutral_cnt:,} neutral reviews", "yellow")

with col5:
    metric_card("Negative Sentiment", f"{neg_pct:.1f}%", f"{negative_cnt:,} negative reviews", "red")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Middle Grid: Sentiment, Rating, Category Charts
# ---------------------------------------------------------
mid_col1, mid_col2, mid_col3 = st.columns(3)

with mid_col1:
    st.markdown('<div class="section-title">Sentiment Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Database data: feedback.own_rating</div>', unsafe_allow_html=True)
    
    sentiment_counts = (
        df["own_rating"]
        .value_counts()
        .reindex(["Positive", "Neutral", "Negative"], fill_value=0)
    )
    st.plotly_chart(donut_chart(sentiment_counts.index, sentiment_counts.values), use_container_width=True)

with mid_col2:
    st.markdown('<div class="section-title">Rating Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Data: feedback.rating</div>', unsafe_allow_html=True)
    
    rating_counts = (
        df["rating"]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
        .sort_index()
    )
    rating_df = rating_counts.reset_index()
    rating_df.columns = ["Rating", "Reviews"]
    st.plotly_chart(bar_chart(rating_df, "Rating", "Reviews", height=300), use_container_width=True)

with mid_col3:
    st.markdown('<div class="section-title">Reviews by Product Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Total feedback count by category</div>', unsafe_allow_html=True)
    
    category_counts = df["category"].value_counts()
    category_df = category_counts.reset_index()
    category_df.columns = ["Category", "Reviews"]
    st.plotly_chart(bar_chart(category_df, "Reviews", "Category", orientation="h", height=300), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Lower Middle Grid: Category Breakdown & Business Insights
# ---------------------------------------------------------
bot_col1, bot_col2, bot_col3 = st.columns([1.5, 1.5, 1.2])

with bot_col1:
    st.markdown('<div class="section-title">Sentiment by Product Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Database data: feedback.own_rating</div>', unsafe_allow_html=True)
    
    cat_sentiment = pd.crosstab(df["category"], df["own_rating"])
    for s_col in ["Positive", "Neutral", "Negative"]:
        if s_col not in cat_sentiment.columns:
            cat_sentiment[s_col] = 0
    cat_sentiment_plot = cat_sentiment[["Positive", "Neutral", "Negative"]].reset_index().melt(
        id_vars="category", var_name="Sentiment", value_name="Reviews"
    )
    st.plotly_chart(bar_chart(cat_sentiment_plot, "category", "Reviews", color="Sentiment", height=300), use_container_width=True)

with bot_col2:
    st.markdown('<div class="section-title">Average Rating by Category</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">AVG(feedback.rating)</div>', unsafe_allow_html=True)
    
    cat_avg_rating = df.groupby("category")["rating"].mean().sort_values(ascending=False)
    avg_df = cat_avg_rating.reset_index()
    avg_df.columns = ["Category", "Average Rating"]
    st.plotly_chart(bar_chart(avg_df, "Average Rating", "Category", orientation="h", height=300), use_container_width=True)

with bot_col3:
    st.markdown('<div class="section-title">Business Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Automatically generated insights</div>', unsafe_allow_html=True)

    # Calculation logic for insights
    most_reviewed_cat = category_counts.index[0] if len(category_counts) > 0 else "N/A"
    most_reviewed_val = category_counts.iloc[0] if len(category_counts) > 0 else 0

    highest_rated_cat = cat_avg_rating.index[0] if len(cat_avg_rating) > 0 else "N/A"
    highest_rated_val = cat_avg_rating.iloc[0] if len(cat_avg_rating) > 0 else 0

    neg_by_cat = df[df["own_rating"] == "Negative"]["category"].value_counts()
    needs_attn_cat = neg_by_cat.index[0] if len(neg_by_cat) > 0 else "N/A"

    dom_sentiment = sentiment_counts.index[0] if len(sentiment_counts) > 0 else "Positive"
    dom_sentiment_pct = pos_pct if dom_sentiment == "Positive" else (neu_pct if dom_sentiment == "Neutral" else neg_pct)

    st.markdown(f"""
        <div class="panel-box">
            <div class="insight-item">
                <div class="insight-icon">📱</div>
                <div>
                    <div class="insight-label">Most Reviewed</div>
                    <div class="insight-val">{most_reviewed_cat}</div>
                    <div class="insight-detail">{most_reviewed_val:,} reviews</div>
                </div>
            </div>
            <div class="insight-item">
                <div class="insight-icon">⭐</div>
                <div>
                    <div class="insight-label">Highest Rated</div>
                    <div class="insight-val">{highest_rated_cat}</div>
                    <div class="insight-detail">{highest_rated_val:.2f} / 5</div>
                </div>
            </div>
            <div class="insight-item">
                <div class="insight-icon">⚠️</div>
                <div>
                    <div class="insight-label">Needs Attention</div>
                    <div class="insight-val">{needs_attn_cat}</div>
                    <div class="insight-detail">Highest negative feedback</div>
                </div>
            </div>
            <div class="insight-item">
                <div class="insight-icon">😊</div>
                <div>
                    <div class="insight-label">Dominant Sentiment</div>
                    <div class="insight-val">{dom_sentiment}</div>
                    <div class="insight-detail">{dom_sentiment_pct:.1f}% of reviews</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Recent Feedback Table Section
# ---------------------------------------------------------
st.markdown('<div class="section-title">Recent Feedback</div>', unsafe_allow_html=True)

recent_df = df.head(10).copy()

display_columns = [
    "unique_id",
    "category",
    "review_header",
    "rating",
    "own_rating"
]

recent_display = recent_df[display_columns].copy()

recent_display.columns = [
    "Unique ID",
    "Category",
    "Review Header",
    "Rating",
    "Sentiment"
]

recent_display["Rating"] = recent_display["Rating"].apply(lambda x: f"{x:.1f} / 5" if pd.notna(x) else "N/A")

st.dataframe(
    recent_display,
    use_container_width=True,
    hide_index=True,
    height=320
)
