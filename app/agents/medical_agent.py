"""Medical Multi-Tool Agent.

Initializes the orchestrating medical agent with access to SQLite databases
(Heart Disease, Cancer, Diabetes) and Medical Web Search.
Features Google Gemini & OpenAI models with automatic multi-tier fallback
and graceful degradation to prevent error modals or crashes.
"""

from typing import Any, Dict
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.tools.heart_disease_tool import HeartDiseaseDBTool
from app.tools.cancer_tool import CancerDBTool
from app.tools.diabetes_tool import DiabetesDBTool
from app.tools.web_search_tool import MedicalWebSearchTool

from app.utils.llm_factory import get_resilient_llm, get_openai_llm, get_gemini_llm
from app.utils.fallback_answers import get_fallback_medical_answer
from app.utils.logger import logger


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


class ResilientMedicalAgent:
    """Wrapper around AgentExecutor with multi-tier model fallbacks and guaranteed fallback answers."""

    def __init__(self, agent_executor: AgentExecutor, tools: list, prompt: ChatPromptTemplate):
        self.agent_executor = agent_executor
        self.tools = tools
        self.prompt = prompt

    def invoke(self, input_dict: Dict[str, Any]) -> Dict[str, str]:
        """Invokes the agent with primary execution, fallback models, and graceful fallback answer degradation."""
        user_input = input_dict.get("input", "")

        # 1. Try Primary Resilient Agent
        try:
            result = self.agent_executor.invoke(input_dict)
            output = result.get("output", "").strip()
            if output:
                return {"output": output}
        except Exception as primary_error:
            logger.warning(
                f"Primary agent execution encountered an issue: {primary_error}. Attempting secondary fallback agent..."
            )

        # 2. Try Secondary Model Agent (Gemini or OpenAI directly if fallback chain needs isolated invocation)
        for fallback_fn in [get_gemini_llm, get_openai_llm]:
            try:
                fb_llm = fallback_fn(temperature=0)
                if fb_llm is not None:
                    fb_agent = create_tool_calling_agent(fb_llm, self.tools, self.prompt)
                    fb_executor = AgentExecutor(
                        agent=fb_agent,
                        tools=self.tools,
                        verbose=False,
                        handle_parsing_errors=True,
                        max_iterations=3
                    )
                    fb_result = fb_executor.invoke(input_dict)
                    fb_output = fb_result.get("output", "").strip()
                    if fb_output:
                        logger.info("Secondary fallback agent resolved the query successfully.")
                        return {"output": fb_output}
            except Exception as fb_error:
                logger.warning(f"Secondary fallback attempt failed: {fb_error}")
                continue

        # 3. Graceful Medical Fallback Answer (Guaranteed, no crash or error modal)
        logger.info("Providing structured medical fallback response.")
        fallback_text = get_fallback_medical_answer(user_input)
        return {"output": fallback_text}


def initialize_medical_agent() -> ResilientMedicalAgent:
    """Initializes the medical multi-tool agent system."""
    tools = [
        HeartDiseaseDBTool,
        CancerDBTool,
        DiabetesDBTool,
        MedicalWebSearchTool
    ]

    llm = get_resilient_llm(temperature=0)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=False,
        handle_parsing_errors=True,
        max_iterations=5
    )

    return ResilientMedicalAgent(agent_executor=agent_executor, tools=tools, prompt=prompt)