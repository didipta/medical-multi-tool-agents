import pytest
from app.tools.diabetes_tool import DiabetesDBTool
from app.tools.web_search_tool import MedicalWebSearchTool

def test_diabetes_tool_invocation():
    query = "How many total patients are in the diabetes dataset?"
    response = DiabetesDBTool.invoke(query)
    assert isinstance(response, str)
    assert len(response) > 0

def test_web_search_tool_invocation():
    query = "What is type 2 diabetes?"
    response = MedicalWebSearchTool.invoke(query)
    assert isinstance(response, str)
    assert len(response) > 0