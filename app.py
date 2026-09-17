import streamlit as st
from utils.ui import apply_theme

st.set_page_config(
    page_title="Retail Feedback Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_theme()

# --------------------------------------------------
# Custom CSS for Modern Dark Theme Styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Global Page Styling */
    .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Hero Section Card */
    .hero-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-top: 10px;
        margin-bottom: 24px;
    }

    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(56, 139, 253, 0.15);
        border: 1px solid rgba(56, 139, 253, 0.4);
        color: #58a6ff;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 12px;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #8b949e;
        line-height: 1.6;
        max-width: 700px;
        margin-bottom: 24px;
    }

    /* Feature Grid Styling */
    .feature-card {
        background: #161b22;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px;
        height: 100%;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .feature-icon {
        font-size: 24px;
        margin-bottom: 12px;
    }

    .feature-title {
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .feature-desc {
        font-size: 13px;
        color: #8b949e;
        line-height: 1.5;
    }

    /* Info Callout Box */
    .info-callout {
        background: rgba(56, 139, 253, 0.1);
        border-left: 4px solid #388bfd;
        border-radius: 6px;
        padding: 14px 18px;
        color: #58a6ff;
        font-size: 14px;
        font-weight: 500;
        margin-top: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


# --------------------------------------------------
# Authentication Check
# --------------------------------------------------

if not st.session_state.authenticated:

    st.markdown(
        """
        <div class="hero-card">
            <span class="hero-badge">🔒 Authentication Required</span>
            <div class="hero-title">Retail Customer Feedback Analyzer</div>
            <div class="hero-subtitle">
                Turn customer feedback into actionable insights. Analyze reviews, track satisfaction ratings, 
                monitor AI sentiment, and discover product category performance with data-driven intelligence.
            </div>
            <div class="info-callout">
                💡 Please log in via the sidebar menu to access the analytics workspace.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Customer Analytics</div>
                <div class="feature-desc">Monitor rating distributions and overall customer feedback patterns in real-time.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">AI Sentiment Analysis</div>
                <div class="feature-desc">Automatically categorize feedback sentiment and evaluate customer satisfaction.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📦</div>
                <div class="feature-title">Product Intelligence</div>
                <div class="feature-desc">Compare category performance to identify top performers and areas needing attention.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.markdown(
        """
        <div class="hero-card">
            <span class="hero-badge">⚡ Platform Active</span>
            <div class="hero-title">Retail Customer Feedback Analyzer</div>
            <div class="hero-subtitle">
                Welcome to your customer intelligence platform. Use the navigation sidebar on the left 
                to explore dashboards, analyze sentiment, manage feedback entries, and review performance metrics.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Dashboard</div>
                <div class="feature-desc">View high-level KPIs, sentiment splits, and category ratings.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📋</div>
                <div class="feature-title">Feedback Table</div>
                <div class="feature-desc">Filter, search, export, and inspect detailed feedback entries.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🏷️</div>
                <div class="feature-title">Categories</div>
                <div class="feature-desc">Evaluate category-level metrics and individual product performance.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">Admin Controls</div>
                <div class="feature-desc">Manage system cache, data export, and session settings.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
