import os
from joblib import load
import pandas as pd

# Base directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")

# Load models
model_old = load(os.path.join(ARTIFACTS_DIR, "artifacts_model_old.joblib"))
model_young = load(os.path.join(ARTIFACTS_DIR, "artifacts_model_young.joblib"))

# Load scalers
scaler_old = load(os.path.join(ARTIFACTS_DIR, "artifacts_scaler_old.joblib"))
scaler_young = load(os.path.join(ARTIFACTS_DIR, "artifacts_scaler_young.joblib"))


def cal_normalized_risk_score(medical_history: str) -> int:
    # risk scores dictionary
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }

    # lowercasing for consistency
    medical_history = medical_history.lower()

    # split on " & " into at most 2 diseases
    diseases = medical_history.split(" & ")

    # ensure always 2 entries
    if len(diseases) == 1:
        diseases.append("none")

    # map each disease to risk score
    disease1_score = risk_scores.get(diseases[0], 0)
    disease2_score = risk_scores.get(diseases[1], 0)

    # total risk score
    total_risk_score = disease1_score + disease2_score

    return total_risk_score

def handle_scaling(age, df):
    if age<=25:
        scaler_object=scaler_young
    else:
        scaler_object=scaler_old
    
    cols_to_scale=scaler_object['cols_to_scale']
    scaler=scaler_object['scaler']

    df["income_level"]=0
    df[cols_to_scale]=scaler.transform(df[cols_to_scale])
    df.drop("income_level", axis=1, inplace=True)
    return df

def preprocessing_input(input_dict):
    expected_cols = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan',
       'genetical_risk', 'total_risk_score', 'gender_Male', 'region_Northwest',
       'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
       'bmi_category_Obesity', 'bmi_category_Overweight',
       'bmi_category_Underweight', 'smoking_status_Occasional',
       'smoking_status_Regular', 'employment_status_Salaried',
       'employment_status_Self-Employed'
    ]

    # Start with all zeros
    df = pd.DataFrame(0, columns=expected_cols, index=[0])

    for key, val in input_dict.items():

        # ---------------- numeric features ----------------
        if key == "Age":
            df["age"] = val

        elif key == "Dependents":
            df["number_of_dependants"] = val

        elif key == "Income (Lakhs)":
            df["income_lakhs"] = val

        elif key == "Total Risk Score":
            df["total_risk_score"] = val

        elif key=="Genetical Risk":
            df["genetical_risk"]=val

        # ---------------- gender ----------------
        elif key == "Gender":
            if val == "Male":
                df["gender_Male"] = 1

        # ---------------- region ----------------
        elif key == "Region":
            if val == "Northwest":
                df["region_Northwest"] = 1
            elif val == "Southeast":
                df["region_Southeast"] = 1
            elif val == "Southwest":
                df["region_Southwest"] = 1

        # ---------------- marital status ----------------
        elif key == "Marital Status":
            if val == "Unmarried":
                df["marital_status_Unmarried"] = 1

        # ---------------- bmi category ----------------
        elif key == "BMI Category":
            if val == "Obesity":
                df["bmi_category_Obesity"] = 1
            elif val == "Overweight":
                df["bmi_category_Overweight"] = 1
            elif val == "Underweight":
                df["bmi_category_Underweight"] = 1

        # ---------------- smoking status ----------------
        elif key == "Smoking Status":
            if val == "Occasional":
                df["smoking_status_Occasional"] = 1
            elif val == "Regular":
                df["smoking_status_Regular"] = 1

        # ---------------- employment status ----------------
        elif key == "Employment Status":
            if val == "Salaried":
                df["employment_status_Salaried"] = 1
            elif val == "Self-Employed":
                df["employment_status_Self-Employed"] = 1

        # ---------------- insurance plan ----------------
        elif key == "Insurance Plan":
            if val == "Bronze":
                df["insurance_plan"] = 0
            elif val == "Silver":
                df["insurance_plan"] = 1
            elif val == "Gold":
                df["insurance_plan"] = 2
            else:
                df["insurance_plan"] = 0  # Default

    df["total_risk_score"]=cal_normalized_risk_score(input_dict["Medical History"])

    df=handle_scaling(input_dict["Age"], df)

    return df

def predict(input_dict):
    input_df=preprocessing_input(input_dict)
    if(input_df["age"].iloc[0]<=25):
        prediction=model_young.predict(input_df)
    else:
        prediction=model_old.predict(input_df)

    return  int(prediction[0])