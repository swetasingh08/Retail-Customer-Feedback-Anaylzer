import html

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


COLORS = {
    "bg": "#0b1118",
    "panel": "#121923",
    "panel_2": "#182231",
    "border": "rgba(148, 163, 184, 0.18)",
    "text": "#f8fafc",
    "muted": "#94a3b8",
    "blue": "#4ea8de",
    "green": "#5ad48a",
    "yellow": "#f6c85f",
    "red": "#ee6a63",
    "purple": "#8b5cf6",
}

SENTIMENT_COLORS = {
    "Positive": COLORS["green"],
    "Neutral": COLORS["yellow"],
    "Negative": COLORS["red"],
}


def apply_theme():
    st.markdown(
        f"""
        <style>
        :root {{
            --app-bg: {COLORS["bg"]};
            --panel: {COLORS["panel"]};
            --panel-2: {COLORS["panel_2"]};
            --border: {COLORS["border"]};
            --text: {COLORS["text"]};
            --muted: {COLORS["muted"]};
            --blue: {COLORS["blue"]};
            --green: {COLORS["green"]};
            --yellow: {COLORS["yellow"]};
            --red: {COLORS["red"]};
        }}

        .stApp {{
            background:
                radial-gradient(circle at 18% 8%, rgba(78, 168, 222, 0.11), transparent 28rem),
                radial-gradient(circle at 86% 18%, rgba(139, 92, 246, 0.10), transparent 30rem),
                linear-gradient(135deg, #101722 0%, #080d13 100%) !important;
            color: var(--text);
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}

        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(18, 25, 35, 0.96), rgba(11, 17, 24, 0.98)) !important;
            border-right: 1px solid var(--border);
        }}

        section[data-testid="stSidebar"] * {{
            color: #dbe7f5 !important;
        }}

        .block-container {{
            padding-top: 1.7rem;
            padding-bottom: 2rem;
        }}

        h1, h2, h3, h4, h5, h6, p, label, span {{
            letter-spacing: 0 !important;
        }}

        div[data-testid="stMetric"],
        div[data-testid="stDataFrame"],
        div[data-testid="stPlotlyChart"],
        div[data-testid="stForm"],
        .glass-card {{
            background: linear-gradient(145deg, rgba(24, 34, 49, 0.92), rgba(14, 20, 29, 0.95)) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.24) !important;
        }}

        div[data-testid="stMetric"] {{
            padding: 1rem 1.1rem !important;
            min-height: 104px;
        }}

        div[data-testid="stMetricLabel"] p {{
            color: var(--muted) !important;
            font-size: 0.84rem !important;
        }}

        div[data-testid="stMetricValue"] {{
            color: var(--text) !important;
            font-weight: 800 !important;
        }}

        .stButton > button,
        .stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, #34c7f4 0%, #7c5cff 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 8px !important;
            color: white !important;
            font-weight: 700 !important;
            min-height: 2.6rem;
        }}

        .stTextInput input,
        .stTextArea textarea,
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] {{
            background: rgba(10, 16, 24, 0.9) !important;
            border: 1px solid rgba(148, 163, 184, 0.24) !important;
            border-radius: 8px !important;
            color: var(--text) !important;
        }}

        .page-kicker {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.25rem 0.6rem;
            border: 1px solid rgba(90, 212, 138, 0.24);
            border-radius: 999px;
            background: rgba(90, 212, 138, 0.12);
            color: #88efaa;
            font-size: 0.74rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }}

        .page-title {{
            font-size: clamp(1.75rem, 3vw, 2.35rem);
            line-height: 1.05;
            font-weight: 850;
            color: white;
            margin: 0;
        }}

        .page-subtitle {{
            color: var(--muted);
            font-size: 0.98rem;
            margin: 0.35rem 0 1.4rem;
        }}

        .section-title {{
            color: white;
            font-size: 1rem;
            font-weight: 780;
            margin: 0.4rem 0 0.2rem;
        }}

        .section-subtitle {{
            color: var(--muted);
            font-size: 0.78rem;
            margin-bottom: 0.7rem;
        }}

        .mini-card {{
            background: linear-gradient(145deg, rgba(24, 34, 49, 0.94), rgba(14, 20, 29, 0.97));
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 1rem;
            min-height: 100px;
        }}

        .mini-label {{
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 650;
        }}

        .mini-value {{
            color: white;
            font-size: 1.55rem;
            font-weight: 850;
            margin-top: 0.2rem;
        }}

        .positive {{ color: var(--green) !important; }}
        .neutral {{ color: var(--yellow) !important; }}
        .negative {{ color: var(--red) !important; }}

        .hero-shell {{
            min-height: calc(100vh - 7rem);
            display: grid;
            align-items: center;
        }}

        .brand-logo {{
            width: 56px;
            height: 56px;
            border-radius: 14px;
            display: grid;
            place-items: center;
            font-size: 1.75rem;
            background: linear-gradient(135deg, rgba(52, 199, 244, 0.55), rgba(124, 92, 255, 0.58));
            border: 1px solid rgba(255, 255, 255, 0.14);
            box-shadow: 0 0 34px rgba(52, 199, 244, 0.24);
            margin-bottom: 1.35rem;
        }}

        .flow-text {{
            color: #7d8897;
            font-size: 0.76rem;
            margin: 1.2rem 0 1.5rem;
        }}

        .feature-row {{
            display: flex;
            gap: 0.85rem;
            align-items: flex-start;
            margin: 1rem 0;
        }}

        .feature-icon {{
            width: 38px;
            height: 38px;
            border-radius: 8px;
            display: grid;
            place-items: center;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }}

        .feature-title {{
            color: white;
            font-weight: 780;
        }}

        .feature-copy {{
            color: var(--muted);
            font-size: 0.88rem;
        }}

        .login-card {{
            max-width: 440px;
            margin: 2.5rem auto 0;
            padding: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle, kicker=None):
    if kicker:
        st.markdown(f'<div class="page-kicker">{html.escape(kicker)}</div>', unsafe_allow_html=True)
    st.markdown(f'<h1 class="page-title">{html.escape(title)}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-subtitle">{html.escape(subtitle)}</p>', unsafe_allow_html=True)


def metric_card(label, value, subtext="", tone="blue"):
    color = COLORS.get(tone, COLORS["blue"])
    st.markdown(
        f"""
        <div class="mini-card" style="border-color: color-mix(in srgb, {color} 42%, transparent);">
            <div class="mini-label">{html.escape(label)}</div>
            <div class="mini-value">{html.escape(str(value))}</div>
            <div style="color:{COLORS["muted"]};font-size:.78rem;margin-top:.2rem;">{html.escape(str(subtext))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_layout(fig, height=300):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=COLORS["text"],
        margin=dict(l=12, r=12, t=20, b=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        colorway=[COLORS["green"], COLORS["yellow"], COLORS["red"], COLORS["blue"], COLORS["purple"]],
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,.13)", zerolinecolor="rgba(148,163,184,.18)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,.13)", zerolinecolor="rgba(148,163,184,.18)")
    return fig


def bar_chart(data_frame, x, y, color=None, orientation="v", height=300, labels=None):
    fig = px.bar(
        data_frame,
        x=x,
        y=y,
        color=color,
        orientation=orientation,
        labels=labels,
        color_discrete_map=SENTIMENT_COLORS,
    )
    fig.update_traces(marker_line_width=0, opacity=0.92)
    return plotly_layout(fig, height)


def donut_chart(labels, values, height=300):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.58,
                marker=dict(colors=[SENTIMENT_COLORS.get(label, COLORS["blue"]) for label in labels]),
                textinfo="percent",
            )
        ]
    )
    return plotly_layout(fig, height)
