import streamlit as st
from PIL import Image
import os
import pandas as pd
import re

# Page configuration
st.set_page_config(layout="wide", page_title="📈 Trading Strategy Dashboard")

# ---------- Custom CSS ----------
st.markdown("""
    <style>
        .main { background-color: #f9f9f9; padding: 10px 30px; }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
        }
        .st-expanderHeader {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- User Input in Sidebar ----------
with st.sidebar:
    st.header("🔐 User Details (Required)")
    with st.form(key='user_form'):
        user_name = st.text_input("Full Name", placeholder="Enter your name")
        user_email = st.text_input("Email Address", placeholder="Enter your email")
        submitted = st.form_submit_button("Submit")
        
    if submitted and user_name and user_email:
        st.sidebar.success("✅ Details submitted successfully!")

    if not submitted:
        st.info("ℹ️ Please fill out the form and press Submit.")
        st.stop()

    if not user_name or not user_email:
        st.warning("⚠️ Both Name and Email are required to proceed.")
        st.stop()
        
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    if not re.match(email_pattern, user_email.strip()):
        st.error("❌ Invalid Email Format. Please enter a valid email like `example@domain.com`.")
        st.stop()

# ---------- Save user info ----------
def save_user_info(name, email, file_path="user_info.csv"):
    if name and email:
        df = pd.DataFrame([[name.strip(), email.strip()]], columns=["Name", "Email"])
        
        # Check if the directory exists and create it if not
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        
        if os.path.exists(file_path):
            existing_df = pd.read_csv(file_path)
            # Only append if the user is not already in the file
            if not ((existing_df["Name"] == name) & (existing_df["Email"] == email)).any():
                df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, index=False)

# Save user details locally
save_user_info(user_name, user_email, file_path="user_info.csv")

# ---------- Welcome Header ----------
st.title("📊 Infosys Stock Analysis")
st.markdown(f"""
**👋 Welcome, `{user_name}`!**

Dive into detailed technical analysis of Infosys stock — explore patterns, signals, and strategy performance through interactive, data-driven visualizations.
""")


# ---------- About Section ----------
with st.expander("📘 About This Strategy", expanded=True):
    st.markdown("""
    **Stock Analyzed**: Infosys Ltd (INFY.NS)  \n
    **Timeframe**: April 1, 2021 – March 31, 2025 \n  
    **Data Interval**: Daily  \n
    **Strategy Type**: Momentum & Mean Reversion \n  
    **Technical Indicators Used**: RSI, MACD, Bollinger Bands, Support & Resistance, Custom Signal Strategy  \n
    ---
    This dashboard leverages classic technical analysis tools and price action patterns to uncover actionable trading insights. \n  
    📊 Use it to explore market behavior, spot opportunities, and evaluate strategy performance. \n
    ---
    ⚠️ **Note**: This is an evolving project. Features and accuracy are continuously being improved.
    """)


# ---------- Tab Section ----------
tab1, tab2 = st.tabs(["📈 Technical Analysis", "📊 Strategy Performance Summary"])

# ---------- Chart Display Function ----------
with tab1:
    st.subheader("📈 Technical Indicators and Signals")
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

# ---------- Chart Info ----------
plot_dir = "plots"
charts_info = [
    ("1️⃣ Closing Price Trend", "closing_price.png",
     ''' Pattern Observed: Cycles of Trending Periods Followed by Consolidation

Explanation: "The closing price chart reveals distinct periods of upward or downward trends, interspersed with periods of sideways consolidation where the price moves within a range. The magnitude and duration of trends vary significantly."''',
     '''Trend Identification and Support/Resistance Levels

Trend Following: "Identify prevailing trends (upward or downward) and consider trend-following strategies, such as buying pullbacks in an uptrend or selling bounces in a downtrend. Use tools like moving averages to confirm trends."
Range Trading: "During consolidation periods, look for support and resistance levels. Buy near support and sell near resistance, with appropriate risk management."'''),

    ("2️⃣ Daily Returns", "daily_return.png",
     "Multiple spikes indicate volatile sessions, including sharp negative returns.",
     "High volatility implies high uncertainty — important to manage risk."),

    ("3️⃣ Cumulative Returns", "cumulative_return.png",
     '''Overall Upward Trajectory with Periods of Drawdown

Explanation: "The cumulative returns chart demonstrates the long-term growth of an investment in Infosys, highlighting periods of positive returns and periods of drawdown (losses). The slope of the line indicates the rate of return."''',
     '''Long-Term Performance Assessment and Drawdown Management

Investment Horizon: "Use this chart to assess the overall performance of Infosys over a specific investment horizon. Consider your investment goals and time frame when interpreting the results."
Risk Tolerance: "Analyze the magnitude and duration of drawdowns to understand the potential risks involved in investing in Infosys. Ensure your risk tolerance aligns with the historical volatility."'''),

    ("4️⃣ Indicator vs Price Movement", "dual_axis_plot.png",
     '''What it shows: This chart combines the price of Infosys (blue line, left y-axis) with its trading volume (orange bars, right y-axis) over time.

🔍 Pattern: Volume Spikes Often Correlate with Significant Price Movements

Explanation: Observe that significant increases in trading volume (tall orange bars) often coincide with notable price changes (sharp upward or downward movements in the blue line). This suggests that volume plays a role in confirming the strength of price trends.''',
     '''Confirmation of Price Action and Identification of Strong Moves

Volume Confirmation: High volume during a price breakout above resistance or below support can lend more credibility to the move. Low volume during a price movement might indicate a lack of conviction.
Potential Reversals: Divergence between price and volume (e.g., price making new highs on decreasing volume) can sometimes signal a weakening trend and a potential reversal.'''),

    ("5️⃣ MACD Trend Momentum", "macd.png",
     '''Crossovers of MACD and Signal Line Signal Potential Momentum Shifts

Explanation: "The MACD (Moving Average Convergence Divergence) oscillates above and below the zero line. Crossovers of the MACD line (blue) and the signal line (orange) provide potential signals of changes in price momentum. Divergence between the MACD and price can also be significant."''',
     ''' Momentum Trading and Trend Confirmation

Crossover Signals: "A MACD line crossing above the signal line is a bullish signal, suggesting potential upward momentum. Conversely, a MACD line crossing below the signal line is a bearish signal."
Divergence: "Look for divergence: if the price is making new highs, but the MACD is not, it could signal a weakening uptrend. The opposite is true for downtrends."'''),

    ("6️⃣ Bollinger Band Analysis", "bollinger_band.png",
     '''Price Tendency to Revert from Band Extremes

Explanation: "Historically, Infosys's price often encounters resistance or support when touching or briefly exceeding the upper or lower Bollinger Bands. This suggests a tendency for the price to be 'pulled back' towards the moving average after reaching these statistically significant boundaries."
''',
     '''High-Probability Mean Reversion and Breakout Monitoring

Mean Reversion Strategy: "Traders can watch for potential short-term trading opportunities when the price reaches these band extremes, anticipating a reversion back towards the 50-day SMA. Confirmation signals should be used to increase the probability of successful mean reversion trades."
Breakout Potential: "Conversely, sustained price movement outside the bands, especially when accompanied by widening band width, can signal the start of a strong trend or breakout. This warrants close monitoring for potential trend-following entries."'''),

    ("7️⃣ Support and Resistance Zones", "support_resistance.png",
     ''' Price Consistently Bouncing Off Support and Facing Rejection at Resistance

Explanation: The chart shows numerous instances where the price drops to a support level and subsequently bounces upwards. Conversely, the price often rises to a resistance level and then declines. These levels appear to act as temporary floors and ceilings for price movement.''',
     ''' Identifying Potential Entry and Exit Points

Trading Ranges: The identified support and resistance levels can help define potential trading ranges. Traders might look to buy near support and sell near resistance.
Breakout Potential: Monitor these levels for potential breakouts. A sustained move above a resistance level could signal the start of an uptrend, while a break below support could indicate a downtrend. Increased volume on a breakout can add confirmation.'''),

    ("8️⃣ Signal-Based Strategy Overview", "signal_base.png",
     '''What it shows: This chart compares the cumulative return of a trading strategy (green line) against the cumulative return of the market (blue dashed line) over time. Both start at a normalized value of 1.0.

🔍 Pattern: Underperformance of the Strategy Compared to the Market with Higher Volatility

Explanation: The green line (Strategy) generally stays below the blue dashed line (Market), indicating the strategy has underperformed the market over the observed period. Additionally, the fluctuations in the strategy's cumulative return appear more pronounced than those of the market, suggesting higher volatility. The strategy experiences significant drawdowns, especially in late 2021, mid-2022, and throughout 2024.''',
     '''Strategy Evaluation and Risk Assessment

Performance Analysis: The chart clearly illustrates the strategy's inability to generate returns comparable to the overall market. This raises questions about the strategy's effectiveness during this period.
Risk Management: The higher volatility and larger drawdowns of the strategy, as visually depicted, highlight a higher level of risk associated with its implementation compared to simply holding the market. This aligns with the negative Sharpe Ratio and higher Max Drawdown of the strategy as indicated in your "performance_metrics.txt" file.'''),
    
    ("9️⃣ RSI Momentum Oscillator", "rsi.png",
 '''RSI Oscillates Between Overbought and Oversold Levels

Explanation: "The Relative Strength Index (RSI) measures the speed and change of price movements, oscillating between 0 and 100. Readings above 70 are typically considered overbought, while readings below 30 are considered oversold."   
"''',
 '''Overbought/Oversold Conditions and Potential Reversals

Reversal Signals: "When the RSI enters overbought territory (above 70), it suggests the price may be due for a pullback. When it enters oversold territory (below 30), it suggests a potential price bounce."
Confirmation: "Use RSI in conjunction with other indicators to confirm potential reversals. Divergence between the RSI and price can also provide strong signals.""'''),
    
    ("🔟 Volatility Compression and Expansion", "volatile_analysis.png",
 '''Volatility Clusters and Mean Reversion

Explanation: "The volatility chart shows periods of clustered high volatility followed by periods of relative calm. Volatility tends to revert to its mean over time, though the mean level can shift.""''',
 '''Risk Assessment and Options Trading

Risk Management: "Use this chart to assess the current and historical volatility of Infosys. High volatility implies higher risk, while low volatility suggests lower risk. Adjust position sizes accordingly."
Options Strategies: "Options traders use volatility information to make decisions on buying or selling options. For example, they may buy options when volatility is low (expecting it to rise) and sell options when volatility is high (expecting it to decline).""'''),
    
    ("1️⃣1️⃣ Combined Technical Indicators", "sma.png",
 '''Crossovers of Short-Term and Long-Term SMAs Indicate Trend Changes

Explanation: "This chart shows the relationship between the closing price and two Simple Moving Averages (SMAs) – the 50-day and the 200-day. Crossovers between these SMAs are widely watched as potential trend change signals.""''',
 '''Trend Following and Crossover Strategies

Golden Cross/Death Cross: "A 'golden cross' (50-day SMA crossing above the 200-day SMA) is considered a bullish signal, suggesting a potential uptrend. A 'death cross' (50-day SMA crossing below the 200-day SMA) is a bearish signal."
Dynamic Support/Resistance: "SMAs can also act as dynamic support in an uptrend or resistance in a downtrend. Traders may look for buying opportunities near a rising SMA or selling opportunities near a falling SMA.""''')
]

# ---------- Render Charts ----------
for title, filename, pattern, interpretation in charts_info:
    display_chart(title, os.path.join(plot_dir, filename), pattern, interpretation)

# ---------- Performance Summary ----------
with tab2:
    st.subheader("📊 Strategy Performance Summary")
    with st.expander("📊 Strategy Performance Summary", expanded=True):
        perf_txt_path = os.path.join(plot_dir, "performance_metrics.txt")
        if os.path.exists(perf_txt_path):
            with open(perf_txt_path, "r") as f:
                performance = f.read()
            st.code(performance, language="markdown")
        else:
            st.warning("⚠️ Strategy performance summary text not found.")

# ---------- CTA ----------
st.balloons()
st.success("✅ Dashboard Loaded Successfully! Dive into the charts to discover market behavior & trading opportunities.")
