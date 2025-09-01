import streamlit as st
from healthcare_premium_prediction_helper import predict

st.set_page_config(page_title="Health Insurance Prediction", layout="wide")

# --- Custom CSS for styling ---
st.markdown("""
    <style>
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #e0f7fa, #f1f8e9);
    }

    /* Titles */
    h1 {
        color: #004d40 !important;
        text-align: center;
    }
    h4 {
        text-align: center;
        color: #555 !important;
    }

    /* Card-style boxes */
    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: rgba(255,255,255,0.0); /* transparent */
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05); /* soft shadow */
        margin-bottom: 20px;
    }

    /* Labels */
    label {
        color: #00695c !important;
        font-weight: bold;
    }

    /* Predict button */
    .stButton>button {
        background: linear-gradient(90deg, #43a047, #1e88e5);
        color: white;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1e88e5, #43a047);
    }
    </style>
""", unsafe_allow_html=True)


# --- Header ---
st.title("🏥 Health Insurance Prediction App")
st.markdown("<h4>Answer a few questions and predict your insurance outcome</h4>", unsafe_allow_html=True)
st.markdown("---")


# ================= Numeric Features =================

# --- Row 1 (Age, Dependents, Income) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    age = st.number_input("🎂 Age", min_value=18, max_value=100, value=31, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    dependents = st.number_input("👨‍👩‍👧 Number of Dependents", min_value=0, max_value=5, value=2, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    income = st.number_input("💰 Annual Income (Lakhs)", min_value=1.0, max_value=100.0, value=17.0, step=0.5)
    st.markdown("</div>", unsafe_allow_html=True)


# ================= Categorical + Extra Numeric =================

# --- Row 2 (Genetical Risk, Gender, Region) ---
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    genetical_risk = st.number_input("🧬 Genetical Risk", min_value=0, max_value=5, value=0, step=1)
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    gender = st.selectbox("👤 Gender", ["Male", "Female"])
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    region = st.selectbox("🌍 Region", ["Northwest", "Southeast", "Northeast", "Southwest"])
    st.markdown("</div>", unsafe_allow_html=True)


# --- Row 3 (Marital, BMI, Smoking) ---
col7, col8, col9 = st.columns(3)
with col7:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    marital_status = st.selectbox("💍 Marital Status", ["Unmarried", "Married"])
    st.markdown("</div>", unsafe_allow_html=True)

with col8:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    bmi_category = st.selectbox("⚖️ BMI Category", ["Normal", "Obesity", "Overweight", "Underweight"])
    st.markdown("</div>", unsafe_allow_html=True)

with col9:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    smoking_status = st.selectbox("🚬 Smoking Status", ["No Smoking", "Regular", "Occasional"])
    st.markdown("</div>", unsafe_allow_html=True)


# --- Row 4 (Employment, Medical History, Insurance Plan) ---
col10, col11, col12 = st.columns(3)
with col10:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    employment_status = st.selectbox("💼 Employment Status", ["Salaried", "Self-Employed", "Freelancer"])
    st.markdown("</div>", unsafe_allow_html=True)

with col11:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    medical_history = st.selectbox("🩺 Medical History", [
        "No Disease", "Diabetes", "High blood pressure", "Thyroid", "Heart disease",
        "Diabetes & High blood pressure", "High blood pressure & Heart disease",
        "Diabetes & Thyroid", "Diabetes & Heart disease"
    ])
    st.markdown("</div>", unsafe_allow_html=True)

with col12:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    insurance_plan = st.selectbox("📋 Insurance Plan", ["Bronze", "Silver", "Gold"])
    st.markdown("</div>", unsafe_allow_html=True)


st.markdown("---")

# --- Centered Predict Button ---
colA, colB, colC = st.columns([1,2,1])
with colB:
    predict_btn = st.button("🔮 Predict", use_container_width=True)

# --- Input Dictionary ---
input_dict = {
    "Age": age,
    "Dependents": dependents,
    "Income (Lakhs)": income,
    "Genetical Risk": genetical_risk,
    "Gender": gender,
    "Region": region,
    "Marital Status": marital_status,
    "BMI Category": bmi_category,
    "Smoking Status": smoking_status,
    "Employment Status": employment_status,
    "Medical History": medical_history,
    "Insurance Plan": insurance_plan
}

if predict_btn:
    st.success("✅ Prediction completed!")
    prediction=predict(input_dict)
    st.success(f"💰 Predicted Premium: {prediction:.2f}")
