from agents import  sector_agent, sector_filter_agent, technology_finder_agent,\
    project_complexity_agent, service_category_finder_agent, country_priority_agent,\
    email_priority_agent, motive_agent,urgency_pricing_agent,provider_type_agent

from crewai import Task


def analyze_motive(query):
    return Task(
        description=(
            f"Analyze the given query to determine its motive.\n"
            f"- Query: {query}\n"
            "\n"
            "### Guidelines for Classification:\n"
            "- Return 'False' if the motive is about:\n"
            "  - Seeking a job or asking for employment opportunities in company \n"
            "  - Offering personal or company services to us.\n"
            "  - Description of service and its pricing to provide us.\n"
            
            "\n"
            "- Return 'True' if the query is about:\n"
            "  - To Hire a developer for a personal/company project or job.\n"
            "  - Seeking technical support or consulting for an existing personal project.\n"
            "  - Looking for project-based assistance, including outsourcing work.\n"
            "  - Inquiring about developing or building a new software.\n"
            "  - Asking for call request except job seeking.\n"

            "\n"
            "### Important Notes:\n"
            "- The response must strictly be either 'True' or 'False' (without explanations or additional text).\n"
            "- Carefully distinguish between job-seekers and employers/clients to avoid misclassification.\n"
        ),
        agent=motive_agent,
        expected_output="Return only 'True' or 'False' based on the motive (no additional text or explanation)."
    )



def sector_analyze(query, selected_sector):
    return Task(
        description=f"Analyze the query and determine its sector. Query: {query}",
        agent=sector_agent,
        expected_output=f"Return a sector name from the query if it matches any value in {selected_sector}. If a match is found, return the exact sector name from {selected_sector}. Otherwise, return an abstracted sector name."
    )

def sector_filter(query, selected_sector):
    return Task(
        description=f"Analyze the input query and determine if it contains or mentions a matched sector from {selected_sector}. If matched or find, return only a boolean value of True; otherwise, return only False.",
        agent=sector_filter_agent,
        expected_output="Return Boolean values 'True' or 'False'."
    )

def service_category_finder(query):
    return Task(
        description=f"Identify the software development category mentioned or implied in the query: '{query}'. "
                    "Example categories include Web Development, App Development, Cloud Hosting, etc.",
        agent=service_category_finder_agent,
        expected_output="Return a name of relevant category name only."
    )

def technology_finder(query,category):
    return Task(
        description=f"Extract relevant technologies from the given query: '{query}' if it pertains to the '{category}' category. "
                    "If the query is related to job postings, job applications, or hiring, return 'None'. "
                    "If no specific technology is mentioned in the query, return 'None'.",
        agent=technology_finder_agent,
        expected_output="Return a list of relevant technology names only if explicitly mentioned in the query (without any extra description). If no technologies are found or the query is job-related, return 'None'." )

def project_complexity_finder(query, resource, technology):
    return Task(
        description=f"Analyze the complexity of the project based on the query: '{query}', category: '{resource}', "
                    f"and technology: '{technology}'. Classify the project into one of the following levels:\n"
                    "1. Simple: Small to medium-sized projects with basic functionality (e.g., Personal websites, small business sites).\n"
                    "2. Advanced: Medium to large projects with custom UI and integrations (e.g., E-commerce, SaaS).\n"
                    "3. Enterprise: Large-scale, complex projects requiring enterprise integrations (e.g., AWS, Kubernetes, ERP systems).",
        agent=project_complexity_agent,
        expected_output="Return one of the complexity levels only (Note: without any extra description): 'Simple', 'Advanced', or 'Enterprise' ."
    # expected_output = "Return one of the complexity levels: 'Low', 'Medium', or 'High' along with an estimated time period for completing the project."
)

def email_priority_finder(email):
    return Task(
        description=(
            f"Determine the priority level based on the email domain.\n"
            f"- Email: {email}\n"
            "- If the email belongs to a business domain, return 'Prior'.\n"
            "- Otherwise, return 'Nonprior'."
        ),
        agent=email_priority_agent,
        expected_output="Return either 'Prior' or 'Nonprior' with no additional details."
    )

def location_priority_finder(country, country_list):
    return Task(
        description=(
            f"Determine the priority level based on the country.\n"
            f"- Country: {country}\n"
            f"- If the country is in {country_list}, return 'Prior'.\n"
            "- Otherwise, return 'Nonprior'."
        ),
        agent=country_priority_agent,
        expected_output="Return either 'Prior' or 'Nonprior' with no additional details."
    )

def urgency_pricing_finder(query):
    return Task(
        description=(
            f"Analyze the given query and determine its urgency level based on the following conditions:\n\n"
            f"1️⃣ **High:** If the query explicitly mentions both urgency (e.g., deadlines, ASAP, urgent) and pricing (e.g., budget, cost, payment).\n"
            f"2️⃣ **Medium:** If the query does not mention urgency or pricing but contains other relevant details.\n"
            f"3️⃣ **Low:** If the query provides minimal or vague information with no mention of urgency or pricing.\n\n"
            f"- Query: {query}\n\n"
            f"Return only 'High', 'Medium', or 'Low' with no additional details."
        ),
        agent=urgency_pricing_agent,
        expected_output="Return only 'High', 'Medium', or 'Low' based on the query details."
    )

def company_type_finder(query):
    return Task(
        description=(
            f"Analyze the given query to determine the type of provider (company, startup, or agency) based on its size and details.\n\n"
            f"1️⃣ **Enterprise:** If the query explicitly mentions a large-scale company, corporation, or multinational firm.\n"
            f"2️⃣ **Mid-sized:** If the query refers to a medium-sized company, mid-level firm, or established agency.\n"
            f"3️⃣ **Small Business:** If the query describes a startup, small business, or individual service provider.\n"
            f"4️⃣ **Unknown:** If no clear company size or type is mentioned.\n\n"
            f"- Query: {query}\n\n"
            f"Return only 'Enterprise', 'Mid-sized', 'Small Business', or 'Unknown' with no additional details."
        ),
        agent=provider_type_agent,
        expected_output="Return only 'Enterprise', 'Mid-sized', 'Small Business', or 'Unknown' based on the query details."
    )





