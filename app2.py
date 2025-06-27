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

# --- Custom CSS for Progress Bar and Colors ---
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #76b852, #f5a623, #d0021b);
    }
    .risk-low { color: #28a745; }
    .risk-moderate { color: #ffc107; }
    .risk-high { color: #dc3545; }
    .header-card {
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


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

# --- Header ---
st.markdown('<div class="header-card"><h1 style="text-align: center;">Dynamic UTI Risk Prediction Model</h1></div>', unsafe_allow_html=True)

# --- UI Sidebar ---
with st.sidebar:
    st.title("👨‍⚕️ Patient Parameters")
    st.markdown("Input the patient's clinical data to predict UTI risk.")

    age = st.slider("Age", 18, 90, 55)
    sex = st.selectbox("Sex", ("Female", "Male"), index=0)
    bmi = st.slider("BMI (Body Mass Index)", 15.0, 40.0, 24.3, 0.1)
    npar = st.slider("NPAR (a clinical marker)", 0.0, 5.0, 1.2, 0.1)
    wbc = st.slider("WBC Count (×10^9/L)", 3.0, 20.0, 8.5, 0.1)
    urine_leukocyte = st.selectbox("Urine Leukocyte Esterase", ("Negative", "Positive"), index=0)
    urinary_nitrite = st.selectbox("Urinary Nitrite", ("Negative", "Positive"), index=0)
    hydronephrosis = st.selectbox("Hydronephrosis", ("No", "Yes"), index=0)
    
    calculate_button = st.button("Calculate Risk", type="primary", use_container_width=True)

# --- Main Page Tabs ---
tab1, tab2 = st.tabs(["Risk Assessment", "Model Performance"])

with tab1:
    # --- Calculation Logic ---
    if config and calculate_button:
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
            risk_class = "risk-low"
            interpretation = "Patient has a low probability of UTI. Monitor and follow up if symptoms persist or worsen."
        elif probability < 0.6:
            risk_category = "Moderate Risk"
            risk_class = "risk-moderate"
            interpretation = "Patient has a moderate probability of UTI. Consider further diagnostic testing and close monitoring."
        else:
            risk_category = "High Risk"
            risk_class = "risk-high"
            interpretation = "Patient has a high probability of UTI. Prompt clinical assessment, diagnosis, and treatment are recommended."
            
        # --- Display Results ---
        st.header("Risk Assessment Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="UTI Risk Probability", value=f"{prob_percent:.1f}%")
        
        with col2:
            st.markdown(f"**Risk Category:**")
            st.markdown(f'<h3 class="{risk_class}">{risk_category}</h3>', unsafe_allow_html=True)
            
        st.progress(probability)
        
        st.subheader("Clinical Interpretation")
        st.info(interpretation)
        
    else:
        st.info("Please input patient data in the left panel and click 'Calculate Risk' to view the prediction.")

with tab2:
    st.header("Model Performance Metrics")
    st.markdown("The model has been validated and shows good discrimination in the validation set.")
    
    perf_data = {
        "Metric": ["AUC", "Accuracy", "Sensitivity", "Specificity"],
        "Validation Set (95% CI)": ["0.8013 (0.767-0.835)", "0.7600", "0.7353", "0.7622"]
    }
    st.table(perf_data)
    
    st.subheader("About this Calculator")
    st.info("""
    - **Model:** This calculator uses a LASSO logistic regression model.
    - **Development:** The model was developed from clinical data, involving steps of data collection, preprocessing, model training, and validation.
    - **Disclaimer:** This tool is intended for clinical reference and educational purposes only. It should not replace professional clinical judgment or standard diagnostic procedures.
    """)

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Dynamic UTI Risk Calculator") 