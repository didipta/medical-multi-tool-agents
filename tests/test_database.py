import sqlite3
import pytest
from app.config.settings import settings

def test_heart_database_exists():
    assert settings.HEART_DB_PATH.exists(), "Heart disease DB file does not exist."
    conn = sqlite3.connect(settings.HEART_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM heart_patients;")
    count = cursor.fetchone()[0]
    conn.close()
    assert count >= 0

def test_diabetes_database_exists():
    assert settings.DIABETES_DB_PATH.exists(), "Diabetes DB file does not exist."
    conn = sqlite3.connect(settings.DIABETES_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM diabetes_patients;")
    count = cursor.fetchone()[0]
    conn.close()
    assert count >= 0