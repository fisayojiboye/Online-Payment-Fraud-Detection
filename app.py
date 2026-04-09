import streamlit as st
import pandas as pd
from datetime import datetime
import os
import gdown
import pickle

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="FraudGuard - Payment Fraud Detector",
    page_icon="🛡️",
    layout="centered"
)

# ====================== LOAD MODEL ======================
MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    url = "https://drive.google.com/uc?id=1n0KyMQakt7WPDFQHa0wrpFning2H_8PM"
    gdown.download(url, MODEL_PATH, quiet=False)

@st.cache_resource
def load_model():
    try:
        with open(MODEL_PATH, "rb") as f:
            package = pickle.load(f)
        return package['model'], package.get('optimal_threshold', 0.35)
    except:
        st.error("Model file not found or corrupted.")
        return None, None

model, threshold = load_model()

# ====================== HEADER ======================
st.title("🛡️ FraudGuard")
st.markdown("""
    ### Intelligent AI-Powered Fraud Detection System
    **Detect fraudulent online payments in real-time**
""")
st.caption("XGBoost Model • ROC-AUC: 0.9997 • Fraud Recall: 95.8%")
st.markdown("---")

# ====================== SIDEBAR ======================
with st.sidebar:
    st.header("About This Tool")
    st.info("""
        This AI model analyzes online payment transactions and predicts 
        the likelihood of fraud. It was trained on 6.36 million transactions.
    """)
    st.markdown("### How it Works")
    st.write("1. Enter transaction details")
    st.write("2. AI calculates risk features")
    st.write("3. Model returns fraud probability")
    st.write("4. Decision made based on threshold (35%)")

# ====================== INPUT SECTION ======================
st.subheader("Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    step = st.number_input("Step (Time Unit)", min_value=0, value=5, step=1)
    amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=1250000.0, step=1000.0)
    oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=1500000.0, step=1000.0)
    newbalanceOrg = st.number_input("New Balance (Sender)", min_value=0.0, value=250000.0, step=1000.0)

with col2:
    oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=0.0, step=1000.0)
    newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=1250000.0, step=1000.0)
    transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"])
    hour = st.slider("Hour of the Day", 0, 23, 4)

# Calculate derived features
is_high_risk_type = 1 if transaction_type in ["TRANSFER", "CASH_OUT"] else 0
is_large_amount = 1 if amount > 1000000 else 0
high_risk_score = is_high_risk_type + is_large_amount

amount_category = (
    "Very Large" if amount > 2000000 else
    "Large" if amount > 1000000 else
    "Medium" if amount > 100000 else
    "Small"
)

# ====================== PREDICTION BUTTON ======================
if st.button("🔍 Check for Fraud", type="primary", use_container_width=True):
    if model is None:
        st.error("Model not loaded. Please check your model file.")
    else:
        input_data = {
            'step': step,
            'amount': amount,
            'oldbalanceOrg': oldbalanceOrg,
            'newbalanceOrig': newbalanceOrg,
            'oldbalanceDest': oldbalanceDest,
            'newbalanceDest': newbalanceDest,
            'is_high_risk_type': is_high_risk_type,
            'is_large_amount': is_large_amount,
            'high_risk_score': high_risk_score,
            'hour': hour,
            'type': transaction_type,
            'amount_category': amount_category
        }
        
        # Create DataFrame and add dummy variables
        input_df = pd.DataFrame([input_data])
        
        input_df['type_CASH_OUT'] = 1 if transaction_type == 'CASH_OUT' else 0
        input_df['type_DEBIT'] = 1 if transaction_type == 'DEBIT' else 0
        input_df['type_PAYMENT'] = 1 if transaction_type == 'PAYMENT' else 0
        input_df['type_TRANSFER'] = 1 if transaction_type == 'TRANSFER' else 0
        
        cat = amount_category
        input_df['amount_category_Small'] = 1 if cat == 'Small' else 0
        input_df['amount_category_Medium'] = 1 if cat == 'Medium' else 0
        input_df['amount_category_Large'] = 1 if cat == 'Large' else 0
        input_df['amount_category_Very Large'] = 1 if cat == 'Very Large' else 0
        
        final_columns = [
            'step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 
            'oldbalanceDest', 'newbalanceDest', 'is_high_risk_type', 
            'is_large_amount', 'high_risk_score', 'hour',
            'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT', 'type_TRANSFER',
            'amount_category_Small', 'amount_category_Medium', 
            'amount_category_Large', 'amount_category_Very Large'
        ]
        
        input_df = input_df[final_columns]
        
        # Make prediction
        prob = model.predict_proba(input_df)[:, 1][0]
        is_fraud = prob >= threshold
        
        # Display result
        if is_fraud:
            st.error(f"🚨 **HIGH RISK FRAUD DETECTED!**")
            st.metric("Fraud Probability", f"{prob*100:.2f}%")
        else:
            st.success(f"✅ **Transaction appears legitimate**")
            st.metric("Fraud Probability", f"{prob*100:.2f}%")

        st.caption(f"Decision threshold used: {threshold}")

        st.info(f"**Decision Threshold**: {threshold*100:.1f}% • Model Confidence: {'High' if abs(prob-0.5) > 0.3 else 'Medium'}")


        # NEW: "Why was this flagged?" Explanation Box
        st.subheader("Why was this decision made?")
        
        reasons = []
        if high_risk_score == 2:
            reasons.append("• High Risk Transaction Type + Very Large Amount")
        elif high_risk_score == 1:
            reasons.append("• Either High Risk Type OR Large Amount")
        if amount > 1000000:
            reasons.append("• Extremely large transaction amount")
        if transaction_type in ["TRANSFER", "CASH_OUT"]:
            reasons.append(f"• Transaction type is {transaction_type} (highest risk types)")
        if (oldbalanceOrg - newbalanceOrg) > amount * 1.5:
            reasons.append("• Unusual drop in sender's balance")
        
        if reasons:
            for reason in reasons:
                st.write(reason)
        else:
            st.write("• No strong risk indicators detected")

st.markdown("---")
st.caption("Built as part of Online Payment Fraud Detection Project | XGBoost Model")