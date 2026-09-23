# -*- coding: utf-8 -*-
"""TastyBox Channel Explorer — an interactive, trap-driven widget for the
Customer Analytics in-class exercise. Students toggle time horizon,
acquisition cost, comparison metric, and segment split to work through four
guided business questions, each with a naive-answer / reveal structure."""

import re

import streamlit as st
import plotly.graph_objects as go


def md_to_html(text: str) -> str:
    """Minimal markdown -> HTML for the reveal boxes: **bold** and \\n\\n paragraphs."""
    paragraphs = text.strip().split("\n\n")
    html_paragraphs = []
    for p in paragraphs:
        p = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", p)
        html_paragraphs.append(f"<p style='margin:0 0 10px;'>{p}</p>")
    return "".join(html_paragraphs)

from data import DATA, CHANNEL_ORDER, COLORS, MARGIN, MONTHS, BUSINESS_QUESTIONS

# ------------------------------------------------------------------
# Page + brand styling (matches the deck's navy/teal system)
# ------------------------------------------------------------------
st.set_page_config(page_title="TastyBox Channel Explorer", layout="wide")

NAVY = "#13233B"
TEAL = "#0E7C7B"
TEXT = "#3A4552"
GRAY = "#8592A0"
CARD_FILL = "#F3F5F7"
CARD_BORDER = "#E1E6EA"
WARM = "#FBF1E6"

st.markdown(
    f"""
    <style>
    .stApp {{ background: #FFFFFF; }}
    html, body, [class*="css"] {{ font-family: Calibri, "Segoe UI", Arial, sans-serif; color: {TEXT}; }}
    .eyebrow {{
        font-size: 12px; font-weight: 700; letter-spacing: 1.5px;
        color: {TEAL}; text-transform: uppercase; margin-bottom: 4px;
    }}
    h1.tb-title {{
        font-family: Georgia, "Times New Roman", serif; color: {NAVY};
        font-size: 34px; font-weight: 700; margin: 0 0 6px;
    }}
    .tb-subtitle {{ font-size: 15px; color: {TEXT}; max-width: 900px; line-height: 1.5; margin-bottom: 18px; }}
    .rank-card {{
        display: flex; align-items: center; gap: 12px;
        background: #fff; border: 1px solid {CARD_BORDER}; border-radius: 6px;
        padding: 10px 14px; margin-bottom: 8px;
    }}
    .rank-num {{
        width: 26px; height: 26px; border-radius: 50%; background: {NAVY}; color: #fff;
        display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; flex-shrink: 0;
    }}
    .rank-name {{ font-weight: 700; color: {NAVY}; font-size: 14.5px; }}
    .rank-sub {{ font-size: 11.5px; color: {GRAY}; }}
    .rank-value {{ font-family: Georgia, serif; font-weight: 700; font-size: 17px; color: {NAVY}; margin-left: auto; white-space: nowrap; }}
    .insight-box {{
        margin-top: 10px; padding: 14px 16px; border-radius: 6px;
        background: {WARM}; border: 1px solid {CARD_BORDER};
        font-size: 14.5px; line-height: 1.5; color: {NAVY};
    }}
    .stat-tile {{
        background: {CARD_FILL}; border: 1px solid {CARD_BORDER}; border-radius: 6px;
        padding: 12px 16px; text-align: center;
    }}
    .stat-tile .num {{ font-family: Georgia, serif; font-size: 22px; font-weight: 700; color: {NAVY}; }}
    .stat-tile .lbl {{ font-size: 11px; color: {GRAY}; text-transform: uppercase; letter-spacing: 0.5px; }}
    footer.tb-footer {{ margin-top: 28px; font-size: 11.5px; color: {GRAY}; font-style: italic; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Customer Analytics &middot; TastyBox Case</div>', unsafe_allow_html=True)
st.markdown('<h1 class="tb-title">TastyBox Channel Explorer</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="tb-subtitle">Five acquisition channels, twelve months of retention data. '
    "You're advising on next year's channel budget — toggle the controls below to work "
    "through four decisions where the obvious first read turns out to be wrong.</div>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Controls
# ------------------------------------------------------------------
ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2, 1.3, 1.6, 1.3])

with ctrl1:
    month = st.slider("Data through month", min_value=1, max_value=MONTHS, value=MONTHS, key="month")
with ctrl2:
    include_cac = st.toggle("Include acquisition cost", value=False, key="include_cac")
with ctrl3:
    metric_view = st.radio(
        "Comparison metric",
        ["Per-customer CLV", "Customers Acquired", "Total Value Created"],
        horizontal=True,
        key="metric_view",
    )
with ctrl4:
    split_segment = st.toggle("Split by segment", value=False, key="split_segment")

st.divider()

# ------------------------------------------------------------------
# Left: cumulative value chart. Right: live ranking.
# ------------------------------------------------------------------
left, right = st.columns([1.6, 1])

def channel_value_at(name, m, net):
    v = DATA[name]["blended_clv"][m - 1]
    return v - DATA[name]["cac"] if net else v

with left:
    fig = go.Figure()
    for name in CHANNEL_ORDER:
        y = DATA[name]["blended_clv"][:]
        if include_cac:
            y = [v - DATA[name]["cac"] for v in y]
        fig.add_trace(
            go.Scatter(
                x=list(range(1, MONTHS + 1)),
                y=y,
                mode="lines+markers",
                name=name,
                line=dict(color=COLORS[name], width=2.5),
                marker=dict(size=4),
                hovertemplate=f"{name}<br>Month %{{x}}: $%{{y:.2f}}<extra></extra>",
            )
        )
        if split_segment:
            for seg in DATA[name]["segments"]:
                y_seg = seg["clv"][:]
                if include_cac:
                    y_seg = [v - DATA[name]["cac"] for v in y_seg]
                fig.add_trace(
                    go.Scatter(
                        x=list(range(1, MONTHS + 1)),
                        y=y_seg,
                        mode="lines",
                        name=f"{name} — {seg['name']}",
                        line=dict(color=COLORS[name], width=1.3, dash="dot"),
                        opacity=0.55,
                        showlegend=False,
                        hovertemplate=f"{name} ({seg['name']})<br>Month %{{x}}: $%{{y:.2f}}<extra></extra>",
                    )
                )
    fig.add_vline(x=month, line_width=1.5, line_dash="dash", line_color=TEAL)
    ylabel = "Net value (CLV − CAC) per customer" if include_cac else "Cumulative CLV per acquired customer"
    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35, font=dict(size=11)),
        xaxis=dict(title="Month since acquisition", gridcolor="#F0F2F4", dtick=1),
        yaxis=dict(title=ylabel, gridcolor="#F0F2F4", tickprefix="$"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=TEXT, size=12),
    )
    st.plotly_chart(fig, use_container_width=True)
    if split_segment:
        st.markdown(
            '<div style="font-size:11.5px; color:#8592A0; margin-top:-8px;">'
            "Dotted lines = each channel&rsquo;s two sub-segments (New-to-brand / Existing). "
            "Hover a dotted line to see which.</div>",
            unsafe_allow_html=True,
        )

with right:
    st.markdown(f'<div class="eyebrow" style="margin-top:8px;">Ranking at month {month}</div>', unsafe_allow_html=True)
    ranking = sorted(CHANNEL_ORDER, key=lambda k: -channel_value_at(k, month, include_cac))
    for i, name in enumerate(ranking):
        val = channel_value_at(name, month, include_cac)
        sub = f"CAC ${DATA[name]['cac']}" if include_cac else f"{DATA[name]['acquired']} acquired"
        st.markdown(
            f"""<div class="rank-card">
                <div class="rank-num">{i+1}</div>
                <div><div class="rank-name">{name}</div><div class="rank-sub">{sub}</div></div>
                <div class="rank-value">${val:,.2f}</div>
            </div>""",
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------
# Comparison metric bar chart (drives Trap 3)
# ------------------------------------------------------------------
st.markdown(f'<div class="eyebrow" style="margin-top:18px;">Channel comparison &middot; {metric_view}</div>', unsafe_allow_html=True)

if metric_view == "Customers Acquired":
    values = {k: DATA[k]["acquired"] for k in CHANNEL_ORDER}
    fmt = lambda v: f"{v:,.0f}"
elif metric_view == "Total Value Created":
    values = {k: DATA[k]["blended_clv"][-1] * DATA[k]["acquired"] for k in CHANNEL_ORDER}
    fmt = lambda v: f"${v:,.0f}"
else:
    values = {k: DATA[k]["blended_clv"][-1] for k in CHANNEL_ORDER}
    fmt = lambda v: f"${v:,.2f}"

bar_order = sorted(CHANNEL_ORDER, key=lambda k: -values[k])
bar_fig = go.Figure(
    go.Bar(
        x=[values[k] for k in bar_order],
        y=bar_order,
        orientation="h",
        marker_color=[COLORS[k] for k in bar_order],
        text=[fmt(values[k]) for k in bar_order],
        textposition="outside",
    )
)
bar_fig.update_layout(
    height=260,
    margin=dict(l=10, r=60, t=10, b=10),
    xaxis=dict(gridcolor="#F0F2F4", title=metric_view),
    yaxis=dict(autorange="reversed"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color=TEXT, size=12),
    showlegend=False,
)
st.plotly_chart(bar_fig, use_container_width=True)

st.divider()

# ------------------------------------------------------------------
# Guided business questions
# ------------------------------------------------------------------
st.markdown('<div class="eyebrow">In-Class Exercise</div>', unsafe_allow_html=True)
st.markdown('<h2 style="font-family: Georgia, serif; color:#13233B; margin-top:0;">Four Questions, Four Traps</h2>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:14.5px; color:#3A4552; max-width:900px;">Work through these with your group. '
    "For each one: write down your answer from the setup description alone, "
    "<i>then</i> try the suggested toggle before revealing the trap.</p>",
    unsafe_allow_html=True,
)

for q in BUSINESS_QUESTIONS:
    with st.expander(q["title"]):
        st.markdown(q["setup"])
        st.markdown(f"*Try this: {q['trap_hint']}*")
        if st.button("Reveal the trap", key=f"reveal_{q['id']}"):
            st.markdown(f'<div class="insight-box">{md_to_html(q["reveal"])}</div>', unsafe_allow_html=True)

st.markdown(
    f'<footer class="tb-footer">Margin = ${MARGIN}/active customer/month. '
    "All figures are simplified teaching data, internally consistent, not real TastyBox financials.</footer>",
    unsafe_allow_html=True,
)
