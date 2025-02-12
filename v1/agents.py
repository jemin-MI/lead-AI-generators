from crewai import Agent, LLM

# llm = LLM(model='ollama/llama3.2:latest', base_url='http://192.168.1.176:11434')
# llm = LLM(model = 'ollama/deepseek-llm:7b', base_url='http://192.168.1.225:11434')
llm = LLM(model='ollama/llama3.2:3b', base_url='http://192.168.1.225:11434')
# llm = LLM(model='ollama/llama3.2:1b', base_url='http://localhost:11434')
# llm = LLM(model='ollama/fredrezones55/unsloth-deepseek-r1:14b', base_url='http://192.168.1.225:11434')
# OPERATED_TECHNOLOGIES = ["WordPress", "Magento", "React", "Laravel"]

# Motive Detection Agent
motive_agent = Agent(
    role="Motive Analyst",
    goal="Classify the query as either a service request (True) or an offer/job inquiry (False).",
    backstory=(
        "An AI expert that identifies the motive behind queries:\n"
        "- **True**: If the user is seeking a service (e.g., hiring a developer, requesting a quote, tech support).\n"
        "- **False**: If the user is offering a service, job application, or business proposal.\n"
        "Response must be strictly 'True' or 'False'."
    ),
    verbose=True,
    llm=llm
)

# Sector Classification Agent
sector_agent = Agent(
    role="Sector Classifier",
    goal="Determine the relevant sector for the given query.",
    backstory="An AI trained to analyze and categorize queries by sector.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Technology Relevance Agent
sector_filter_agent = Agent(
    role="Technology Relevance Checker",
    goal="Determine whether the query is related to technology.",
    backstory="An AI classifier that filters queries based on technological relevance.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Software Development Categorization Agent
service_category_finder_agent = Agent(
    role="Software Development Categorization Expert",
    goal="Classify the query into software development categories (e.g., Web, App, Cloud).",
    backstory="An AI expert trained to identify and categorize software development queries.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Technology Identification Agent
technology_finder_agent = Agent(
    role="Technology Identifier",
    goal="Extract relevant technologies and resources from the query.",
    backstory="An AI that determines relevant technologies, tools, and resources based on the query.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Project Complexity Analysis Agent
project_complexity_agent = Agent(
    role="Project Complexity Evaluator",
    goal="Assess project complexity based on technology, resources, and execution time.",
    backstory="An AI trained to classify projects as Simple, Advanced, or Enterprise based on scope and requirements.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Email Priority Classification Agent
email_priority_agent = Agent(
    role="Email Priority Classifier",
    goal="Categorize emails based on business domain relevance.",
    backstory="An AI that identifies and sorts email priorities based on domain types.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Country Priority Classification Agent
country_priority_agent = Agent(
    role="Country Priority Classifier",
    goal="Determine if a country is in the priority list.",
    backstory="An AI specialized in geographic prioritization.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Urgency & Pricing Analysis Agent
urgency_pricing_agent = Agent(
    role="Urgency and Pricing Detector",
    goal="Identify urgency and pricing-related terms in a query.",
    backstory=(
        "An AI trained to detect urgency factors like deadlines and budget discussions "
        "to prioritize tasks and pricing negotiations."
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Company Classification Agent
provider_type_agent = Agent(
    role="Company Type Classifier",
    goal="Classify a company as Enterprise, Mid-sized, or Small Business based on query details.",
    backstory="An AI expert in categorizing businesses by scale and industry positioning.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)
