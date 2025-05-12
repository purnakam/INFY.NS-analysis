import streamlit as st
from PIL import Image
import os

# Dashboard Setup
st.set_page_config(layout="wide", page_title="📈 Trading Strategy Dashboard")

st.title("📊 Trading Strategy Dashboard with Storytelling")
st.markdown("Explore technical signals, patterns, and performance through data-driven visualizations.")

# ℹ️ Overview Section
with st.expander("📘 About This Strategy", expanded=True):
    st.markdown("""
    **Stock**:  Infosys Ltd\n
    **Timeframe**:  April 1, 2021 - March 31, 2025\n 
    **Data Interval**: Daily  \n
    **Strategy Focus**: Momentum & Mean Reversion Combination  \n
    **Indicators Used**: MACD, Bollinger Bands, Support/Resistance, Custom Signal Generator  \n
    ---
    This dashboard combines classic technical indicators with basic price action to extract tradeable insights.  
    📌 Use it to analyze behavior, detect patterns, and evaluate performance.  \n
    ---
    🚧 **Note**: This project is a work in progress. Continuous improvements are being made.
    """)

# Function to display image + insights
def display_chart(title, image_path, pattern, interpretation):
    with st.container():
        st.subheader(title)
        col1, col2 = st.columns([2, 3])

        if os.path.exists(image_path):
            with col1:
                st.image(Image.open(image_path), use_container_width=True)
        else:
            with col1:
                st.warning(f"⚠️ Image not found: `{image_path}`")

        with col2:
            st.markdown(f"**🔍 Pattern Observed:** {pattern}")
            st.markdown(f"**💡 Interpretation:** {interpretation}")
        st.markdown("—" * 30)

# Plot directory
plot_dir = "plots"

# Chart Sections
charts_info = [
    ("1️⃣ Closing Price Trend", "closing_price.png",
     "Uptrend with higher highs and higher lows followed by a slight correction.",
     "Sustained buying interest. Correction could offer a pullback entry opportunity."),

    ("2️⃣ Daily Returns", "daily_return.png",
     "Multiple spikes indicate volatile sessions, including sharp negative returns.",
     "High volatility implies high uncertainty — important to manage risk."),

    ("3️⃣ Cumulative Returns", "cumulative_return.png",
     "An initial consistent climb followed by a plateauing region.",
     "Strong during trending periods, but underperforms in sideways markets."),

    ("4️⃣ Indicator vs Price Movement", "dual_axis_plot.png",
     "Momentum or volume spikes are aligned with sharp price actions.",
     "Spikes suggest strong moves; helpful for breakout traders to validate entry signals."),

    ("5️⃣ MACD Trend Momentum", "macd.png",
     "Bullish crossovers (MACD > Signal) precede up moves; bearish ones predict dips.",
     "Momentum trading friendly; filter false signals in low volatility."),

    ("6️⃣ Bollinger Band Analysis", "bollinger_band.png",
     "Price often reverts when it hits the upper or lower band.",
     "Use for mean reversion trades. Expanding bands = breakout watch."),

    ("7️⃣ Support and Resistance Zones", "support_resistance.png",
     "Multiple bounces off support and rejection at resistance levels.",
     "Helps define risk-reward zones, stop-loss areas."),

    ("8️⃣ Signal-Based Strategy Overview", "signal_base.png",
     "Buy/Sell markers align with directional price turns. Some signals fail during choppy movement.",
     "Decent predictive behavior; needs confirmation filter in sideways markets.")
]

# Loop through all charts
for title, filename, pattern, interpretation in charts_info:
    display_chart(title, os.path.join(plot_dir, filename), pattern, interpretation)

# 📈 Strategy Performance Summary
with st.expander("📊 Strategy Performance Summary", expanded=True):
    perf_txt_path = os.path.join(plot_dir, "performance_metrics.txt")
    if os.path.exists(perf_txt_path):
        with open(perf_txt_path, "r") as f:
            performance = f.read()
        st.code(performance, language="markdown")
    else:
        st.warning("⚠️ Strategy performance summary text not found.")

# 🎯 Call to Action
st.balloons()
st.success("✅ Dashboard Loaded Successfully! Dive into the charts to discover market behavior & trading opportunities.")
