import streamlit as st
import numpy as np
import pickle
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="UTI Risk Calculator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load Model and Config ---
@st.cache_resource
def load_model():
    """Loads the model configuration from a pickle file."""
    model_path = os.path.join(os.path.dirname(__file__), 'model_config.pkl')
    try:
        with open(model_path, 'rb') as f:
            config = pickle.load(f)
        return config
    except FileNotFoundError:
        st.error(f"Error: The model file 'model_config.pkl' was not found in the directory.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")
        return None

config = load_model()
if config:
    model_coefficients = config.get("modelCoefficients", {})
    standardization = config.get("standardization", {})

# --- UI Sidebar ---
st.sidebar.title("👨‍⚕️ Patient Parameters")
st.sidebar.markdown("Input the patient's clinical data to predict UTI risk.")

age = st.sidebar.slider("Age", 18, 90, 55)
sex = st.sidebar.selectbox("Sex", ("Female", "Male"), index=0)
bmi = st.sidebar.slider("BMI (Body Mass Index)", 15.0, 40.0, 24.3, 0.1)
npar = st.sidebar.slider("NPAR (a clinical marker)", 0.0, 5.0, 1.2, 0.1)
wbc = st.sidebar.slider("WBC Count (×10^9/L)", 3.0, 20.0, 8.5, 0.1)
urine_leukocyte = st.sidebar.selectbox("Urine Leukocyte Esterase", ("Negative", "Positive"), index=0)
urinary_nitrite = st.sidebar.selectbox("Urinary Nitrite", ("Negative", "Positive"), index=0)
hydronephrosis = st.sidebar.selectbox("Hydronephrosis", ("No", "Yes"), index=0)

# --- Main Page ---
st.title("🔬 Dynamic UTI Risk Prediction Model")
st.markdown("This tool uses a LASSO regression model to predict the risk of Urinary Tract Infection (UTI) based on clinical parameters.")
st.markdown("---")

# --- Calculation Logic ---
if config and st.sidebar.button("Calculate Risk", type="primary"):
    # Convert categorical inputs to numeric
    sex_val = 1 if sex == "Male" else 0
    urine_leukocyte_val = 1 if urine_leukocyte == "Positive" else 0
    urinary_nitrite_val = 1 if urinary_nitrite == "Positive" else 0
    hydronephrosis_val = 1 if hydronephrosis == "Yes" else 0

    # Standardize continuous variables
    std_age = (age - standardization['age']['mean']) / standardization['age']['std']
    std_bmi = (bmi - standardization['BMI']['mean']) / standardization['BMI']['std']
    std_npar = (npar - standardization['NPAR']['mean']) / standardization['NPAR']['std']
    std_wbc = (wbc - standardization['whitebloodcellcount']['mean']) / standardization['whitebloodcellcount']['std']
    
    # Calculate logit using model coefficients
    logit = (model_coefficients['intercept'] +
             (model_coefficients['age'] * std_age) +
             (model_coefficients['sex'] * sex_val) +
             (model_coefficients['BMI'] * std_bmi) +
             (model_coefficients['NPAR'] * std_npar) +
             (model_coefficients['urineleukocyteesterase'] * urine_leukocyte_val) +
             (model_coefficients['urinarynitrite'] * urinary_nitrite_val) +
             (model_coefficients['hydronephrosis'] * hydronephrosis_val) +
             (model_coefficients['whitebloodcellcount'] * std_wbc))

    # Calculate probability using the sigmoid function
    probability = 1 / (1 + np.exp(-logit))
    prob_percent = probability * 100

    # Determine Risk Category
    if probability < 0.3:
        risk_category = "Low Risk"
        color = "green"
        interpretation = "Patient has a low probability of UTI. Monitor and follow up if symptoms persist or worsen."
    elif probability < 0.6:
        risk_category = "Moderate Risk"
        color = "orange"
        interpretation = "Patient has a moderate probability of UTI. Consider further diagnostic testing and close monitoring."
    else:
        risk_category = "High Risk"
        color = "red"
        interpretation = "Patient has a high probability of UTI. Prompt clinical assessment, diagnosis, and treatment are recommended."
        
    # --- Display Results ---
    st.header("Risk Assessment Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="UTI Risk Probability",
            value=f"{prob_percent:.1f}%",
            delta=risk_category,
            delta_color="normal" 
        )
    
    with col2:
        st.markdown(f"**Risk Category:**")
        st.markdown(f"<h3 style='color:{color};'>{risk_category}</h3>", unsafe_allow_html=True)
        
    st.progress(probability)
    
    st.subheader("Clinical Interpretation")
    st.info(interpretation)
    
else:
    st.info("Please input patient data in the left panel and click 'Calculate Risk' to view the prediction.")

st.markdown("---")
st.markdown("© 2025 Dynamic UTI Risk Calculator. For research and educational purposes only.")
st.markdown("**Disclaimer:** This calculator is not a substitute for professional clinical judgment.") 