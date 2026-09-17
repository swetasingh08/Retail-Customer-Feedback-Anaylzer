import streamlit as st
import hashlib
from database.db import get_connection
from utils.ui import apply_theme

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Admin Login",
    page_icon="🔐",
    layout="wide"
)

# ============================================================
# CUSTOM DARK UI (MATCHING DESIGN REFERENCE)
# ============================================================

st.markdown(
    """
    <style>
    /* App Background */
    .stApp {
        background-color: #0b0e14 !important;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Left Hero Branding Section */
    .brand-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #06b6d4, #3b82f6);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }

    .brand-title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.15;
    }

    .brand-subtitle {
        font-size: 16px;
        font-weight: 600;
        color: #e2e8f0;
        margin-top: 12px;
        margin-bottom: 8px;
    }

    .brand-description {
        font-size: 13px;
        color: #8b949e;
        line-height: 1.5;
        margin-bottom: 24px;
    }

    /* Pipeline Process Steps */
    .pipeline-flow {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        color: #6e7681;
        margin-bottom: 20px;
    }

    .pipeline-step {
        color: #8b949e;
    }

    /* Feature Highlights List */
    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 16px;
    }

    .feature-icon {
        width: 32px;
        height: 32px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
    }

    .feature-title {
        font-size: 13px;
        font-weight: 600;
        color: #ffffff;
    }

    .feature-text {
        font-size: 12px;
        color: #8b949e;
    }

    /* Right Glassmorphism Card Container */
    .login-box {
        background: rgba(22, 27, 34, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
    }

    .card-header-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
    }

    .card-header-sub {
        font-size: 13px;
        color: #8b949e;
        text-align: center;
        margin-bottom: 24px;
    }

    /* Form Inputs and Button Customizations */
    div[data-baseweb="input"] {
        background-color: #0d1117 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #3b82f6 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    }

    /* Footer Branding */
    .footer-text {
        text-align: center;
        font-size: 11px;
        color: #484f58;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
apply_theme()

# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ============================================================
# PASSWORD HASH
# ============================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(email, password):
    connection = get_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                user_id,
                name,
                email,
                password_hash,
                role
            FROM users
            WHERE email = %s
            LIMIT 1
        """

        cursor.execute(
            query,
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user is None:
            return None

        hashed_password = hash_password(password)

        if hashed_password == user["password_hash"]:
            return user

        return None

    except Exception as e:
        try:
            connection.close()
        except Exception:
            pass

        st.error(
            f"Database authentication error: {e}"
        )

        return None

# ============================================================
# ALREADY AUTHENTICATED OR LOGIN SPLIT LAYOUT
# ============================================================

col_left, col_right = st.columns([1.2, 1], gap="large")

# --- LEFT HERO BRANDING SECTION ---
with col_left:
    st.markdown("""
        <div class="brand-logo">🌊</div>
        <div class="brand-title">Retail Feedback<br>Analyzer</div>
        
        <div class="pipeline-flow">
            <span class="pipeline-step">Customer Reviews</span> ➔ 
            <span class="pipeline-step">Sentiment Analysis</span> ➔ 
            <span class="pipeline-step">Analytics</span> ➔ 
            <span class="pipeline-step">Business Insights</span>
        </div>

        <div class="brand-subtitle">Turn customer feedback into actionable insights.</div>
        <div class="brand-description">
            Analyze customer reviews, understand sentiment, monitor ratings and discover product category performance with data-driven intelligence.
        </div>

        <div class="feature-item">
            <div class="feature-icon">📊</div>
            <div>
                <div class="feature-title">Customer Analytics</div>
                <div class="feature-text">Analyze feedback and rating patterns.</div>
            </div>
        </div>

        <div class="feature-item">
            <div class="feature-icon">🧠</div>
            <div>
                <div class="feature-title">AI Sentiment Analysis</div>
                <div class="feature-text">Automatically classify customer sentiment.</div>
            </div>
        </div>

        <div class="feature-item">
            <div class="feature-icon">📦</div>
            <div>
                <div class="feature-title">Product Intelligence</div>
                <div class="feature-text">Compare performance across product categories.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- RIGHT CARD SECTION ---
with col_right:
    if st.session_state.authenticated:
        st.markdown("""
            <div class="login-box">
                <div class="card-header-title">Welcome Back</div>
                <div class="card-header-sub">You are currently logged in as administrator</div>
        """, unsafe_allow_html=True)

        st.success(f"Signed in as **{st.session_state.user_name}**")
        st.write(f"**Role:** `{st.session_state.user_role}`")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📥 Export Data", use_container_width=True):
            st.info("Export functionality can be connected to the All Feedback page.")

        if st.button("🧹 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Application cache cleared successfully.")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 Logout", type="primary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.session_state.user_role = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
            <div class="login-box">
                <div class="card-header-title">Welcome Back</div>
                <div class="card-header-sub">Sign in to your analytics workspace</div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email Address",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            submitted = st.form_submit_button(
                "Sign In to Dashboard",
                use_container_width=True
            )

            if submitted:
                if not email.strip():
                    st.error("Please enter your email.")
                elif not password:
                    st.error("Please enter your password.")
                else:
                    with st.spinner("Authenticating..."):
                        user = authenticate_user(
                            email.strip(),
                            password
                        )

                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user["user_id"]
                        st.session_state.user_name = user["name"]
                        st.session_state.user_role = user["role"]

                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")

        st.markdown("</div>", unsafe_allow_html=True)

# Footer Line
st.markdown("""
    <div class="footer-text">
        Retail Feedback Analyzer | Customer Intelligence Platform
    </div>
""", unsafe_allow_html=True)
