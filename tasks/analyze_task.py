from crewai import Task
from pydantic import BaseModel, Field
from agents.analyst_agent import analyst_agent

class StockResearch(BaseModel):
    ticker: str = Field(description="The stock ticker symbol")
    price: float = Field(description="The current market price")
    daily_change_pct: float = Field(description="Percentage change since opening")
    volume: int = Field(description="Current trading volume")
    high_low: str = Field(description="The daily High and Low range")
    key_observation: str = Field(description="One concise sentence on the trend")

get_stock_analysis_task = Task(
    description=(
        "Analyze the recent performance of the stock: {stock}. use the live stock information tool to retrieve"
        "current price, percentage change, trading volume, and other market data. Provide a summary of how the stock "
        "is performing today and highlight any key observations from the data."
    ),
    expected_output=(
        "A clear, bullet-pointed summary of :\n"
        "- Current stock price\n"
        "- Daily price change and percentage\n"
        "- Volume and volatility\n"
        "- Any immediate trends or observations"
    ),
    agent=analyst_agent,
    output_pydantic=StockResearch
)