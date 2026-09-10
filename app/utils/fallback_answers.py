"""Fallback Medical Answer Engine.

Provides context-aware, structured medical responses when models, tools,
or external services encounter errors or rate limits, preventing raw error
modals or unhandled exceptions from appearing to the user.
"""

from typing import Optional
from app.utils.logger import logger


def get_fallback_medical_answer(query: str, error: Optional[Exception] = None) -> str:
    """Generates a structured, professional medical fallback response based on query context.

    Args:
        query: The user's original query.
        error: Optional exception that triggered the fallback.

    Returns:
        A formatted, empathetic, and informative medical answer.
    """
    if error:
        logger.warning(f"Fallback answer activated due to: {error}")

    q_lower = query.lower()

    # Context: Heart Disease / Cardiology
    if any(k in q_lower for k in ["heart", "cholesterol", "trestbps", "thalach", "blood pressure", "cardio", "chest pain", "angina"]):
        return (
            "### Medical Guidance: Cardiovascular Health\n\n"
            "Live analytical database records are currently operating in fallback mode. Here is standard clinical guidance regarding cardiovascular health:\n\n"
            "**Key Indicators & Normal Ranges:**\n"
            "- **Resting Blood Pressure:** Normal is typically < 120/80 mmHg.\n"
            "- **Total Cholesterol:** Desirable level is generally below 200 mg/dL.\n"
            "- **Heart Rate (Resting):** Normal adult resting rate is between 60-100 beats per minute (bpm).\n\n"
            "**General Recommendations:**\n"
            "- Maintain regular aerobic physical activity (at least 150 minutes per week).\n"
            "- Follow a heart-healthy diet low in saturated fats and sodium (e.g., Mediterranean diet).\n"
            "- If you experience symptoms like persistent chest pressure, shortness of breath, or palpitations, consult a doctor immediately.\n\n"
            "*Note: This information is for educational purposes. For diagnostic decisions or personalized treatment, please consult a certified cardiologist.*"
        )

    # Context: Diabetes / Endocrine
    if any(k in q_lower for k in ["diabetes", "glucose", "insulin", "blood sugar", "hba1c", "pregnancies"]):
        return (
            "### Medical Guidance: Diabetes Management & Glucose Regulation\n\n"
            "Live analytical database records are currently operating in fallback mode. Here is standard clinical guidance on diabetes parameters:\n\n"
            "**Key Diagnostic Parameters:**\n"
            "- **Fasting Blood Glucose:** Normal is 70-99 mg/dL; Prediabetes is 100-125 mg/dL; Diabetes is 126 mg/dL or higher.\n"
            "- **HbA1c:** Normal is < 5.7%; Prediabetes is 5.7%-6.4%; Diabetes is 6.5% or above.\n"
            "- **BMI:** Normal range is typically 18.5 - 24.9 kg/m².\n\n"
            "**Key Management Strategies:**\n"
            "- Balanced carbohydrate intake and portion control with low glycemic index foods.\n"
            "- Regular monitoring of blood sugar levels and adherence to prescribed medications/insulin.\n"
            "- Consistent exercise to improve insulin sensitivity.\n\n"
            "*Note: This information is for educational purposes. Please consult an endocrinologist or primary care physician for individualized medical care.*"
        )

    # Context: Cancer / Oncology
    if any(k in q_lower for k in ["cancer", "tumor", "oncology", "malignan", "biopsy", "genetic risk", "chemo"]):
        return (
            "### Medical Guidance: Oncology & Cancer Awareness\n\n"
            "Live analytical database records are currently operating in fallback mode. Here is essential medical guidance on cancer risk factors and awareness:\n\n"
            "**Key Risk Factors & Metrics:**\n"
            "- **Lifestyle Factors:** Smoking, high alcohol consumption, and physical inactivity significantly elevate risk across multiple cancer types.\n"
            "- **Genetic Risk:** Family history and specific gene mutations (e.g., BRCA) may warrant specialized early screening.\n"
            "- **BMI & Diet:** Obesity is associated with increased incidence of several malignancies.\n\n"
            "**Important Clinical Guidelines:**\n"
            "- Early detection through routine screening (mammograms, colonoscopies, Pap smears, skin checks) dramatically improves outcomes.\n"
            "- Any unexplained weight loss, persistent lumps, or chronic changes should be evaluated by a healthcare specialist promptly.\n\n"
            "*Note: This information is for educational guidance only. Always discuss cancer screenings and diagnosis with a certified oncologist or physician.*"
        )

    # General Medical & Symptom Fallback
    return (
        "### Medical Assistant: Clinical Information\n\n"
        "I am currently providing structured medical knowledge in fallback mode.\n\n"
        "**Clinical Guidance:**\n"
        "- Medical conditions and patient statistics require careful clinical interpretation.\n"
        "- When evaluating symptoms, doctors consider full medical history, vital signs, and diagnostic laboratory tests.\n"
        "- For any acute symptoms, sudden onset of pain, or emergency conditions, please seek immediate emergency medical care.\n\n"
        "**Suggested Action:**\n"
        "- If you are looking for specific patient dataset metrics, please ensure database connectivity is active.\n"
        "- For specific medical questions, you can ask about symptoms, prevention, or standard treatments for any condition.\n\n"
        "*Disclaimer: This AI system provides medical information for educational purposes and is not a substitute for professional medical advice, diagnosis, or treatment.*"
    )
