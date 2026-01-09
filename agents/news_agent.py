from crewai import Agent, LLM
from crewai_tools import SerperDevTool

serper_tool = SerperDevTool()

news_agent = Agent(
    role="Financial News Researcher",
    goal="Identify the most impactful recent news headlines for {stock} and determine market sentiment.",
    backstory="You are an expert financial journalist. You scan the web for news that affects stock prices, filtering out noise to find meaningful signals.",
    tools=[serper_tool],
    verbose=True
)
