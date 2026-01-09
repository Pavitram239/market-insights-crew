import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
import streamlit as st
from crew import stock_crew

st.set_page_config(page_title="Stock Analysis (CrewAI)", page_icon="📈", layout="centered")
st.title("📈 Multi-Agent Stock Analysis")
st.write("Enter a stock ticker to analyze using the CrewAI agents.")

ticker = st.text_input("Ticker", value="AAPL").strip().upper()
run_button = st.button("Run Analysis")

# In app.py
if run_button:
    with st.spinner(f"Agent Crew is analyzing {ticker}..."):
        try:
            result = stock_crew.kickoff(inputs={"stock": ticker})
            
            # 1. Access the structured data from your agents
            analysis_data = result.tasks_output[0].pydantic
            news_data = result.tasks_output[1].pydantic
            trade_data = result.tasks_output[2].pydantic

            st.subheader("📰 Market Sentiment")
            col_news1, col_news2 = st.columns([1, 2])
            
            with col_news1:
                st.metric("Sentiment", news_data.sentiment_score)
                
            with col_news2:
                st.info(f"**Top Story:** {news_data.top_headline}")
                st.caption(news_data.summary)

            # 2. Prepare the data as a dictionary of STRINGS
            # This is the "Surgical Fix" for the ArrowInvalid error
            report_data = {
                "Metric": ["Price", "Daily Change", "Day Range", "Signal", "Justification"],
                "Details": [
                    str(analysis_data.price),           # Force to string
                    f"{analysis_data.daily_change_pct}%", 
                    str(analysis_data.high_low),        # This was causing your '263.23 - 258.45' error
                    str(trade_data.recommendation),
                    str(trade_data.justification)
                ]
            }

            # 3. Create a DataFrame and ensure ALL columns are strings
            import pandas as pd
            df = pd.DataFrame(report_data).astype(str) # Final safety check

            st.subheader(f"Strategy: {trade_data.recommendation}")
            st.table(df) # Arrow will now handle this correctly

        except Exception as e:
            st.error(f"Error: {e}")