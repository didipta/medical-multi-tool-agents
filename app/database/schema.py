TABLE_SCHEMAS = {
    "heart_patients": """
        CREATE TABLE IF NOT EXISTS heart_patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            sex INTEGER,
            cp INTEGER,
            trestbps REAL,
            chol REAL,
            fbs INTEGER,
            restecg INTEGER,
            thalach REAL,
            exang INTEGER,
            oldpeak REAL,
            slope INTEGER,
            ca INTEGER,
            thal INTEGER,
            target INTEGER
        );
    """,
    "cancer_patients": """
        CREATE TABLE IF NOT EXISTS cancer_patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender INTEGER,
            bmi REAL,
            smoking INTEGER,
            genetic_risk INTEGER,
            physical_activity REAL,
            alcohol_intake REAL,
            cancer_history INTEGER,
            diagnosis INTEGER
        );
    """,
    "diabetes_patients": """
        CREATE TABLE IF NOT EXISTS diabetes_patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregnancies INTEGER,
            glucose REAL,
            blood_pressure REAL,
            skin_thickness REAL,
            insulin REAL,
            bmi REAL,
            diabetes_pedigree_function REAL,
            age INTEGER,
            outcome INTEGER
        );
    """
}