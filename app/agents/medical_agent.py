from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from app.config.settings import settings
from app.tools import (
    HeartDiseaseDBTool,
    CancerDBTool,
    DiabetesDBTool,
    MedicalWebSearchTool
)

SYSTEM_PROMPT = """You are an advanced Medical AI Assistant designed to answer both data-specific analytical questions and broad medical knowledge queries.

You have access to 4 specialized tools:
1. HeartDiseaseDBTool: Queries the Heart Disease SQLite database (patients, cholesterol, heart rate, age, trestbps, target).
2. CancerDBTool: Queries the Cancer SQLite database (patient records, BMI, genetic risk, smoking, cancer history, diagnosis).
3. DiabetesDBTool: Queries the Diabetes SQLite database (glucose, insulin, pregnancies, BMI, blood pressure, outcome).
4. MedicalWebSearchTool: Searches the web for general medical facts, symptom definitions, clinical guidance, treatments, and cures.

Routing Rules:
- When questions mention numbers, averages, statistics, distributions, or records from patients/datasets -> Use the appropriate database tool.
- When questions ask "What is...", "What are the symptoms of...", "How to prevent...", or general medical questions -> Use MedicalWebSearchTool.
- Provide clear, synthesis-driven, and objective final answers based solely on tool outputs.
"""

def initialize_medical_agent() -> AgentExecutor:
    tools = [
        HeartDiseaseDBTool,
        CancerDBTool,
        DiabetesDBTool,
        MedicalWebSearchTool
    ]

    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0,
        api_key=settings.OPENAI_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)