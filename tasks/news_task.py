# Create a new file: tasks/news_task.py
from crewai import Task
from pydantic import BaseModel, Field
from agents.news_agent import news_agent

class NewsSentiment(BaseModel):
    sentiment_score: str = Field(description="Bullish, Bearish, or Neutral")
    top_headline: str = Field(description="The most important news title")
    summary: str = Field(description="A 1-sentence summary of the overall news tone")

get_news_task = Task(
    description="Search for the latest news on {stock} from the last 24 hours. Analyze if the news is positive or negative for the stock price.",
    expected_output="A structured sentiment report based on the latest headlines.",
    agent=news_agent,
    output_pydantic=NewsSentiment
)