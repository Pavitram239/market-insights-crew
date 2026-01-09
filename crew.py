from crewai import Crew, Process

from tasks.analyze_task import get_stock_analysis_task
from tasks.trader_task import trader_decision_task
from tasks.news_task import get_news_task
from agents.analyst_agent import analyst_agent
from agents.trader_agent import trader_agent
from agents.news_agent import news_agent

stock_crew = Crew(
    agents = [analyst_agent, news_agent,trader_agent],
    tasks = [get_stock_analysis_task, get_news_task,trader_decision_task],
    process=Process.sequential,
    memory=False,
    verbose = True
)
