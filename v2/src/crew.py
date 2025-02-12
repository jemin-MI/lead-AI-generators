
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import yaml

llm = LLM(model='ollama/llama3.2:3b', base_url='http://192.168.1.225:11434')

@CrewBase
class SalesLead:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def motive_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['motive_agent'],
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

    @agent
    def sector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sector_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def sector_filter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sector_filter_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def service_category_finder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["service_category_finder_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def technology_finder_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["technology_finder_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def project_complexity_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["project_complexity_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def email_priority_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_priority_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def country_priority_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["country_priority_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def urgency_pricing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["urgency_pricing_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @agent
    def provider_type_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["provider_type_agent"],
            allow_delegation=False,
            verbose=True,
            llm=llm

        )

    @task
    def analyze_motive(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_motive"],
            agent=self.motive_agent()
        )

    @task
    def sector_analyze(self) -> Task:
        return Task(
            config=self.tasks_config["sector_analyze"],
            agent=self.sector_agent()
        )

    @task
    def sector_filter(self) -> Task:
        return Task(
            config=self.tasks_config["sector_filter"],
            agent=self.sector_filter_agent()
        )

    @task
    def service_category_finder(self) -> Task:
        return Task(
            config=self.tasks_config["service_category_finder"],
            agent=self.service_category_finder_agent()
        )

    @task
    def technology_finder(self) -> Task:
        return Task(
            config=self.tasks_config["technology_finder"],
            agent=self.technology_finder_agent()
        )

    @task
    def project_complexity_finder(self) -> Task:
        return Task(
            config=self.tasks_config["project_complexity_finder"],
            agent=self.project_complexity_agent()
        )

    @task
    def email_priority_finder(self) -> Task:
        return Task(
            config=self.tasks_config["email_priority_finder"],
            agent=self.email_priority_agent()
        )

    @task
    def location_priority_finder(self) -> Task:
        return Task(
            config=self.tasks_config["location_priority_finder"],
            agent=self.country_priority_agent()
        )

    @task
    def urgency_pricing_finder(self) -> Task:
        return Task(
            config=self.tasks_config["urgency_pricing_finder"],
            agent=self.urgency_pricing_agent()
        )

    @task
    def company_type_finder(self) -> Task:
        return Task(
            config=self.tasks_config["company_type_finder"],
            agent=self.provider_type_agent()
        )

    # @crew
    # def crew(self) -> Crew:
    #     print("hello hit")
    #     crew = Crew(agents=[], tasks=[])
    #     result = crew.kickoff(inputs={'query':"hello i need developer for software dev"})
    #
    #     print("Agent Response:", result)

# sales_lead = SalesLead()
# sales_lead.crew()