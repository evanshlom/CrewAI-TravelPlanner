from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_anthropic import ChatAnthropic
from .tools.search_tools import search_tool, search_stadium_events, search_hotel_deals, search_flights
import os

@CrewBase
class AllegiantTravelCrew():
    """Allegiant Travel Planning Crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    @agent
    def travel_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_researcher'],
            tools=[search_tool, search_flights, search_hotel_deals],
            llm=self.llm
        )
    
    @agent
    def event_coordinator(self) -> Agent:
        return Agent(
            config=self.agents_config['event_coordinator'],
            tools=[search_tool, search_stadium_events],
            llm=self.llm
        )
    
    @agent
    def budget_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['budget_optimizer'],
            tools=[search_tool],
            llm=self.llm
        )
    
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.travel_researcher()
        )
    
    @task
    def event_task(self) -> Task:
        return Task(
            config=self.tasks_config['event_task'],
            agent=self.event_coordinator()
        )
    
    @task
    def optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['optimization_task'],
            agent=self.budget_optimizer(),
            context=[self.research_task(), self.event_task()]
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )