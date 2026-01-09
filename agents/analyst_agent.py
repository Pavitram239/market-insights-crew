from crewai import Agent, LLM
from tools.stock_research import get_stock_price

llm = LLM(
    model = "groq/llama-3.3-70b-versatile",
    temperature=0
)

analyst_agent = Agent(
    role = "financial analyst",
    goal=("Perform in-depth evaluations of publicly traded stocks using real-time data."
          "Identifying trends, performance insights, and key financial signals to support decision-making."
          ),
    backstory = (
        "You are a veteran financial analyst with deep expertise in interpreting stock market data, "
        "technical trends, fundamentals. You specialize in producing well structured reports that evaluate "
        "stock performance using live market indicators."
    ),
    llm = llm,
    tools = [get_stock_price],
    verbose = True
)