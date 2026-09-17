import streamlit as st
import pandas as pd
from utils.data import load_feedback_frame
from utils.ui import apply_theme, bar_chart, donut_chart, metric_card, page_header

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Product Category Performance",
    page_icon="📦",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS (Dark Theme Glassmorphism & Scorecard Styling)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Dark Theme App Background */
    .stApp {
        background-color: #0b0e14 !important;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Top Live Badge */
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #10b981;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .live-dot {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
    }

    /* Page Titles */
    .main-header {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 2px;
    }

    .main-subtitle {
        font-size: 13px;
        color: #8b949e;
        margin-bottom: 20px;
    }

    /* Custom Top Metric Card Container */
    .metric-card {
        background: #121721;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 18px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .metric-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    .metric-info {
        display: flex;
        flex-direction: column;
    }

    .metric-label {
        font-size: 11px;
        color: #8b949e;
        font-weight: 500;
    }

    .metric-val {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }

    /* Performance Insight Highlight Cards */
    .card-top-performer {
        background: rgba(16, 185, 129, 0.06);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 10px;
        padding: 14px;
    }

    .card-attention {
        background: rgba(245, 158, 11, 0.06);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 10px;
        padding: 14px;
    }

    .card-title {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    /* Inputs and Selectbox styling */
    .stSelectbox > div > div {
        background-color: #121721 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }

    /* Dataframe Table Container styling */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        background-color: #121721;
    }

    /* Subsections Header */
    .section-title {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        margin-top: 15px;
        margin-bottom: 12px;
    }

    /* Custom side panel / card box */
    .insight-panel {
        background: #121721;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 16px;
        height: 100%;
    }
</style>
""", unsafe_allow_html=True)
apply_theme()


# ---------------------------------------------------------
# Load Data from MySQL
# ---------------------------------------------------------
@st.cache_data
def load_feedback():
    data, error = load_feedback_frame(order="DESC")
    if error:
        st.error(error)
        return pd.DataFrame()
    return data


df = load_feedback()


# ---------------------------------------------------------
# Header Section with Live Status Badge
# ---------------------------------------------------------
page_header(
    "Product Category Performance",
    "Compare customer satisfaction, ratings and sentiment across product categories.",
    "Live data - MySQL"
)


# ---------------------------------------------------------
# Validation for Empty Data
# ---------------------------------------------------------
if df.empty:
    st.warning(
        "No feedback data is available. Please import or submit feedback first."
    )
    st.stop()


# ---------------------------------------------------------
# Data Cleaning & Preparation
# ---------------------------------------------------------
df["category"] = df["category"].fillna("Unknown")
df["review_text"] = df["review_text"].fillna("")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["own_rating"] = df["own_rating"].fillna("Unknown")
df["predicted_sentiment"] = df["predicted_sentiment"].fillna("Unknown")


# ---------------------------------------------------------
# Sidebar Filters Logic
# ---------------------------------------------------------
st.sidebar.header("🔎 Filters")

categories = sorted(df["category"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Product Categories",
    options=categories,
    default=categories
)

rating_range = st.sidebar.slider(
    "Rating Range",
    min_value=1,
    max_value=5,
    value=(1, 5)
)

sentiment_options = ["Positive", "Neutral", "Negative"]

selected_sentiments = st.sidebar.multiselect(
    "Predicted Sentiment",
    options=sentiment_options,
    default=sentiment_options
)


# ---------------------------------------------------------
# Apply Filtering to Data
# ---------------------------------------------------------
filtered_df = df.copy()

if selected_categories:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]
else:
    filtered_df = filtered_df.iloc[0:0]

filtered_df = filtered_df[
    (filtered_df["rating"] >= rating_range[0]) &
    (filtered_df["rating"] <= rating_range[1])
]

if selected_sentiments:
    filtered_df = filtered_df[filtered_df["predicted_sentiment"].isin(selected_sentiments)]

if filtered_df.empty:
    st.info("No feedback matches the selected filters.")
    st.stop()


# ---------------------------------------------------------
# Top Bar: Category Dropdown Filter + Key Metrics
# ---------------------------------------------------------
top_col1, top_col2, top_col3, top_col4, top_col5, top_col6 = st.columns([1.5, 1.2, 1.2, 1.2, 1.2, 1.2])

with top_col1:
    st.markdown("<span style='font-size: 12px; color: #8b949e;'>Select Product Category</span>", unsafe_allow_html=True)
    header_category_filter = st.selectbox(
        "Select Product Category",
        options=["All Categories"] + categories,
        label_visibility="collapsed"
    )

if header_category_filter != "All Categories":
    display_df = filtered_df[filtered_df["category"] == header_category_filter]
else:
    display_df = filtered_df.copy()

total_reviews = len(display_df)
avg_rating = display_df["rating"].mean() if total_reviews > 0 else 0

pos_pct = (len(display_df[display_df["predicted_sentiment"] == "Positive"]) / total_reviews * 100) if total_reviews > 0 else 0
neu_pct = (len(display_df[display_df["predicted_sentiment"] == "Neutral"]) / total_reviews * 100) if total_reviews > 0 else 0
neg_pct = (len(display_df[display_df["predicted_sentiment"] == "Negative"]) / total_reviews * 100) if total_reviews > 0 else 0

with top_col2:
    metric_card("Total Reviews", f"{total_reviews:,}", "Selected records", "blue")

with top_col3:
    metric_card("Average Rating", f"{avg_rating:.2f} / 5", "Selected records", "yellow")

with top_col4:
    metric_card("Positive %", f"{pos_pct:.1f}%", "Predicted sentiment", "green")

with top_col5:
    metric_card("Neutral %", f"{neu_pct:.1f}%", "Predicted sentiment", "yellow")

with top_col6:
    metric_card("Negative %", f"{neg_pct:.1f}%", "Predicted sentiment", "red")

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Top Visual Charts Row (4 Charts Grid)
# ---------------------------------------------------------
c_col1, c_col2, c_col3, c_col4 = st.columns(4)

category_perf = (
    filtered_df.groupby("category")
    .agg(
        Reviews=("feedback_id", "count"),
        Average_Rating=("rating", "mean")
    )
    .reset_index()
)

with c_col1:
    st.markdown("##### Average Rating")
    chart1_data = category_perf.rename(columns={"category": "Category", "Average_Rating": "Average Rating"})
    st.plotly_chart(bar_chart(chart1_data, "Category", "Average Rating", height=260), use_container_width=True)

with c_col2:
    st.markdown("##### Review Volume by Category")
    chart2_data = category_perf.rename(columns={"category": "Category"})
    st.plotly_chart(bar_chart(chart2_data, "Reviews", "Category", orientation="h", height=260), use_container_width=True)

with c_col3:
    st.markdown("##### Sentiment Distribution")
    sentiment_cat = pd.crosstab(filtered_df["category"], filtered_df["predicted_sentiment"])
    for sent in ["Positive", "Neutral", "Negative"]:
        if sent not in sentiment_cat.columns:
            sentiment_cat[sent] = 0
    sentiment_cat_plot = sentiment_cat[["Positive", "Neutral", "Negative"]].reset_index().melt(
        id_vars="category", var_name="Sentiment", value_name="Reviews"
    )
    st.plotly_chart(bar_chart(sentiment_cat_plot, "category", "Reviews", color="Sentiment", height=260), use_container_width=True)

with c_col4:
    st.markdown("##### Rating Distribution")
    rating_cat = pd.crosstab(filtered_df["category"], filtered_df["rating"])
    rating_cat_plot = rating_cat.reset_index().melt(id_vars="category", var_name="Rating", value_name="Reviews")
    st.plotly_chart(bar_chart(rating_cat_plot, "category", "Reviews", color="Rating", height=260), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Category Scorecard & Performance Insights
# ---------------------------------------------------------
score_col1, score_col2, score_col3, score_col4, score_col5 = st.columns([2.2, 1, 1, 1.2, 1.4])

# Category aggregation data setup
pos_counts = filtered_df[filtered_df["predicted_sentiment"] == "Positive"].groupby("category").size().reset_index(name="Positive")
neu_counts = filtered_df[filtered_df["predicted_sentiment"] == "Neutral"].groupby("category").size().reset_index(name="Neutral")
neg_counts = filtered_df[filtered_df["predicted_sentiment"] == "Negative"].groupby("category").size().reset_index(name="Negative")

scorecard = category_perf.merge(pos_counts, on="category", how="left")
scorecard = scorecard.merge(neu_counts, on="category", how="left")
scorecard = scorecard.merge(neg_counts, on="category", how="left").fillna(0)

scorecard["Positive %"] = (scorecard["Positive"] / scorecard["Reviews"] * 100).round(1)
scorecard["Neutral %"] = (scorecard["Neutral"] / scorecard["Reviews"] * 100).round(1)
scorecard["Negative %"] = (scorecard["Negative"] / scorecard["Reviews"] * 100).round(1)
scorecard["Avg Rating"] = scorecard["Average_Rating"].round(1)

with score_col1:
    st.markdown("<div class='section-title'>Category Performance Scorecard</div>", unsafe_allow_html=True)
    scorecard_display = scorecard[["category", "Reviews", "Avg Rating", "Positive %", "Neutral %", "Negative"]].copy()
    scorecard_display.columns = ["Category", "Reviews", "Avg Rating", "Positive %", "Neutral %", "Negative Reviews"]
    st.dataframe(scorecard_display, use_container_width=True, hide_index=True, height=210)

# Computing metrics for summary boxes
top_performer = scorecard.sort_values(by=["Avg Rating", "Reviews"], ascending=False).iloc[0] if not scorecard.empty else None
attn_required = scorecard.sort_values(by=["Negative %", "Reviews"], ascending=[False, False]).iloc[0] if not scorecard.empty else None

with score_col2:
    if top_performer is not None:
        st.markdown(f"""
            <div class="card-top-performer">
                <div class="card-title" style="color: #10b981;">🏆 Top Performing Category</div>
                <div style="font-size: 16px; font-weight: 700; color: #ffffff;">{top_performer['category']}</div>
                <div style="font-size: 12px; color: #10b981; margin-top: 2px;"><b>{top_performer['Avg Rating']}</b> rating</div>
                <div style="font-size: 11px; color: #8b949e; margin-top: 8px;"><b>{top_performer['Reviews']}</b> reviews</div>
                <div style="font-size: 11px; color: #10b981;"><b>{top_performer['Positive %']}%</b> Positive</div>
            </div>
        """, unsafe_allow_html=True)

with score_col3:
    if attn_required is not None:
        st.markdown(f"""
            <div class="card-attention">
                <div class="card-title" style="color: #f59e0b;">⚠️ Requiring Attention</div>
                <div style="font-size: 16px; font-weight: 700; color: #ffffff;">{attn_required['category']}</div>
                <div style="font-size: 12px; color: #f59e0b; margin-top: 2px;"><b>{attn_required['Avg Rating']}</b> rating</div>
                <div style="font-size: 11px; color: #ef4444; margin-top: 8px;"><b>{attn_required['Negative %']}%</b> Negative</div>
                <div style="font-size: 11px; color: #8b949e;"><b>{int(attn_required['Negative'])}</b> negative reviews</div>
            </div>
        """, unsafe_allow_html=True)

with score_col4:
    st.markdown("""
        <div class="insight-panel">
            <div style="font-size: 13px; font-weight: 600; color: #ffffff; margin-bottom: 8px;">Category Rating Insights</div>
            <div style="font-size: 11px; color: #9ca3af; line-height: 1.4;">
                • Categories with highest average ratings demonstrate strong overall satisfaction.<br><br>
                • Higher concentration of 5-star reviews correlates directly with automated positive predictions.
            </div>
        </div>
    """, unsafe_allow_html=True)

with score_col5:
    st.markdown("<div style='font-size: 13px; font-weight: 600; color: #ffffff; margin-bottom: 8px;'>Categories Requiring Attention</div>", unsafe_allow_html=True)
    attn_df = scorecard.sort_values(by="Negative %", ascending=False)[["category", "Avg Rating", "Negative %", "Negative"]].head(3)
    attn_df.columns = ["Category", "Average Rating", "Negative %", "Negative Count"]
    st.dataframe(attn_df, use_container_width=True, hide_index=True, height=160)

st.markdown("<br><hr style='border-color: rgba(255, 255, 255, 0.08);'><br>", unsafe_allow_html=True)


# ---------------------------------------------------------
# Category Deep Dive Section
# ---------------------------------------------------------
st.markdown("<div class='section-title'>Category Deep Dive</div>", unsafe_allow_html=True)

selected_category = st.selectbox(
    "Select a category to view detailed feedback",
    options=categories,
    key="deep_dive_selectbox"
)

category_df = filtered_df[filtered_df["category"] == selected_category].copy()

deep_col1, deep_col2, deep_col3, deep_col4 = st.columns([1.5, 1.2, 1.2, 2.5])

with deep_col1:
    st.markdown(f"#### {selected_category}")
    c_tot = len(category_df)
    c_avg = category_df["rating"].mean() if c_tot > 0 else 0
    c_pos = (len(category_df[category_df["predicted_sentiment"] == "Positive"]) / c_tot * 100) if c_tot > 0 else 0

    st.markdown(f"""
        <div style="display: flex; gap: 15px; margin-top: 10px; margin-bottom: 15px;">
            <div>
                <div style="font-size: 10px; color: #8b949e;">Total Reviews</div>
                <div style="font-size: 18px; font-weight: 700;">{c_tot:,}</div>
            </div>
            <div>
                <div style="font-size: 10px; color: #8b949e;">Avg Rating</div>
                <div style="font-size: 18px; font-weight: 700;">{c_avg:.2f} / 5</div>
            </div>
            <div>
                <div style="font-size: 10px; color: #8b949e;">Positive %</div>
                <div style="font-size: 18px; font-weight: 700; color: #10b981;">{c_pos:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    c_breakdown = category_perf.set_index("category")["Reviews"]
    st.bar_chart(c_breakdown, use_container_width=True)

with deep_col2:
    st.markdown("##### Sentiment Prediction Agreement")
    matching_preds = len(category_df[category_df["own_rating"].astype(str).str.lower() == category_df["predicted_sentiment"].astype(str).str.lower()])
    agreement_pct = (matching_preds / c_tot * 100) if c_tot > 0 else 0

    st.markdown(f"""
        <div class="insight-panel">
            <div style="font-size: 11px; color: #8b949e;">Total comparable reviews</div>
            <div style="font-size: 16px; font-weight: 700;">{c_tot:,}</div>
            <div style="font-size: 11px; color: #8b949e; margin-top: 8px;">Matching predictions</div>
            <div style="font-size: 16px; font-weight: 700; color: #10b981;">{matching_preds:,}</div>
            <div style="font-size: 11px; color: #8b949e; margin-top: 8px;">Agreement %</div>
            <div style="font-size: 16px; font-weight: 700; color: #3b82f6;">{agreement_pct:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with deep_col3:
    st.markdown("##### Sentiment Distribution")
    s_dist = category_df["predicted_sentiment"].value_counts()
    s_dist = s_dist.reindex(["Positive", "Neutral", "Negative"], fill_value=0)
    st.plotly_chart(donut_chart(s_dist.index, s_dist.values, height=230), use_container_width=True)

with deep_col4:
    st.markdown(f"##### Recent Category Reviews")

    feedback_display = category_df[
        [
            "review_header",
            "review_text",
            "rating",
            "own_rating",
            "predicted_sentiment",
            "created_at"
        ]
    ].copy()

    feedback_display.columns = [
        "Review Header",
        "Truncated Review Text",
        "Rating",
        "Customer Sentiment",
        "Predicted Sentiment",
        "Created At"
    ]

    st.dataframe(
        feedback_display.head(20),
        use_container_width=True,
        hide_index=True,
        height=220
    )


# ---------------------------------------------------------
# Rating Trend Analysis Over Time
# ---------------------------------------------------------
if (category_df["created_at"].notna().any() and category_df["rating"].notna().any()):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📈 Average Rating Over Time")

    trend_df = category_df.dropna(subset=["created_at", "rating"]).copy()
    trend_df["date"] = trend_df["created_at"].dt.date
    daily_rating = trend_df.groupby("date")["rating"].mean()

    st.line_chart(daily_rating, use_container_width=True)
