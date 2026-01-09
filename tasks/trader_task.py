from crewai import Task
from pydantic import BaseModel, Field
from agents.trader_agent import trader_agent

class TradingRecommendation(BaseModel):
    recommendation: str = Field(description="The final signal: BUY, SELL, or HOLD")
    current_price: str = Field(description="The latest price with currency")
    daily_change_pct: float = Field(description="The daily percentage change")
    market_observation: str = Field(description="One sentence on volume or activity")
    justification: str = Field(description="Concise reasoning for the signal")


trader_decision_task = Task(
    description=(
        "Use live market data and stock performance indicators for {stock} to make a strategic trading decision."
        "Assess key factors such as current price, daily change percentage, volume trends, and recent momentum. "
        "Based on your analysis, recommend whether to **Buy**, **Sell**, or **Hold** the stock. "
    ),
    expected_output=(
        "A clear and confident trading recommendation (Buy / Sell / Hold), supported by:\n"
        "- Current stock price and daily change\n"
        "- volume and market activity observation\n"
        "- Justification for the trading action based on technical signals or risk-reward outlook\n"
    ),
    agent=trader_agent,
    output_pydantic=TradingRecommendation
)