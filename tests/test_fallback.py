import pytest
from unittest.mock import MagicMock
from app.utils.fallback_answers import get_fallback_medical_answer
from app.utils.llm_factory import get_gemini_llm, get_openai_llm, get_resilient_llm
from app.agents.medical_agent import ResilientMedicalAgent


def test_fallback_answers_cardiology():
    ans = get_fallback_medical_answer("What is the average cholesterol or heart rate?")
    assert "Cardiovascular" in ans or "heart" in ans.lower()
    assert "Blood Pressure" in ans or "Cholesterol" in ans


def test_fallback_answers_diabetes():
    ans = get_fallback_medical_answer("What is the average glucose level for diabetes patients?")
    assert "Diabetes" in ans
    assert "Fasting Blood Glucose" in ans


def test_fallback_answers_cancer():
    ans = get_fallback_medical_answer("What is the risk of cancer from smoking?")
    assert "Oncology" in ans or "Cancer" in ans
    assert "Risk Factors" in ans


def test_fallback_answers_general():
    ans = get_fallback_medical_answer("I have a fever and headache.")
    assert "Medical Assistant" in ans
    assert "Clinical Guidance" in ans


def test_llm_factory_gemini_instantiation():
    llm = get_gemini_llm()
    assert llm is not None
    assert "gemini" in llm.model.lower()


def test_llm_factory_openai_instantiation():
    llm = get_openai_llm()
    assert llm is not None
    assert "gpt" in llm.model_name.lower()


def test_resilient_llm_chain():
    llm = get_resilient_llm()
    assert llm is not None


def test_resilient_medical_agent_fallback_on_failure():
    # Mock an agent executor that raises an exception
    mock_executor = MagicMock()
    mock_executor.invoke.side_effect = RuntimeError("API Rate Limit Exceeded")

    resilient_agent = ResilientMedicalAgent(
        agent_executor=mock_executor,
        tools=[],
        prompt=MagicMock()
    )

    # Should not raise exception, but return clean fallback output
    result = resilient_agent.invoke({"input": "What are the symptoms of diabetes?"})
    assert isinstance(result, dict)
    assert "output" in result
    assert "Diabetes" in result["output"]
    assert "RuntimeError" not in result["output"]
