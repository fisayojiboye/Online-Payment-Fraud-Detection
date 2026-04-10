# 🛡️ FraudGuard - AI-Powered Online Payment Fraud Detection

**Detecting Fraudulent Transactions in Real-Time with Machine Learning**

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-5C5C5C?style=for-the-badge&logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![ROC-AUC](https://img.shields.io/badge/ROC--AUC-0.9997-brightgreen)

### 🌐 **Live Demo**
**[Try FraudGuard Now →](https://fisayojiboye-f9ggy4zwhw5ixuefy6442q.streamlit.app/)**

---

### 📌 Overview

In today's digital world, online payments have become incredibly convenient — but they also come with rising fraud risks. Scammers are constantly finding new ways to steal money through fake transfers, account takeovers, and money laundering.

**FraudGuard** is an intelligent, real-time fraud detection system I built to help solve this problem. 

Using the full **PaySim synthetic dataset** containing **6.36 million transactions**, I developed a powerful machine learning model that can instantly analyze a transaction and predict whether it is fraudulent or legitimate.

The system doesn't just give a "Yes/No" answer — it also explains **why** it made that decision (e.g., "Extremely large amount + TRANSFER type + unusual balance drop"). This level of transparency is very important in real-world financial applications.

The highlight of the project is a clean, professional, and user-friendly **Streamlit web application** that allows anyone (bank analysts, fintech professionals, or recruiters) to test different transaction scenarios and see the AI in action.

---

### ✨ Key Highlights

- ✅ Trained on the **full 6.36 million rows** (not a sample)
- ✅ Final model: **XGBoost** with exceptional performance
- ✅ ROC-AUC: **0.9997** | Fraud Recall: **95.8%**
- ✅ Smart feature engineering (`high_risk_score`, balance error detection, amount categories)
- ✅ Interactive Streamlit app with clear explanations
- ✅ Model hosted on Google Drive for smooth deployment
- ✅ Fully deployed and accessible to the world

---

### 📊 Model Performance

| Metric                | Score       | Interpretation                  |
|-----------------------|-------------|---------------------------------|
| ROC-AUC               | **0.9997**  | Excellent discrimination        |
| Fraud Recall          | **95.8%**   | Catches 95.8% of all frauds     |
| Fraud Precision       | 71.5%       | Good balance with false alarms  |
| Overall Accuracy      | 99.95%      | Very high on imbalanced data    |

---

### 🛠️ Feature Engineering

I created several powerful features that significantly improved model performance:

- **`high_risk_score`**: Combines high-risk transaction type (TRANSFER/CASH_OUT) + large amount
- **`is_high_risk_type`**: Flags TRANSFER and CASH_OUT transactions
- **`is_large_amount`**: Identifies transactions above $1 million
- **Balance mismatch features**: Detects impossible balance changes between old and new balances
- **`amount_category`**: Categorizes transactions into Very Small, Small, Medium, Large, Very Large
- **`hour`**: Extracted from the step variable to capture time-based patterns

These engineered features became the strongest predictors in the final model.

---

### 🧠 How It Works

1. **User inputs** transaction details (amount, type, sender & receiver balances, etc.)
2. The app automatically creates powerful engineered features
3. XGBoost model calculates the **fraud probability**
4. System compares probability with optimized threshold and gives clear result + explanation

**Most important signals the model looks for:**
- Very large transaction amounts
- TRANSFER or CASH_OUT transaction types  
- Sudden sharp drop in sender’s balance
- Combination of high-risk features

---

### 💼 Business Impact

This project has strong real-world applicability in:

- **Fintech & Digital Banking**: Real-time fraud prevention during transactions
- **Payment Gateways**: Reducing chargebacks and financial losses
- **Risk Management Teams**: Providing explainable AI decisions for compliance
- **Customer Trust**: Minimizing false positives so legitimate transactions are not blocked

By achieving **95.8% fraud recall**, the system can help organizations significantly reduce fraud-related losses while maintaining a smooth customer experience.

---

### 🛠️ Tech Stack

- **Language**: Python
- **Machine Learning**: XGBoost (final model)
- **Web Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Model Deployment**: Google Drive + pickle
- **Hosting**: Streamlit Community Cloud

---

### 🚀 How to Run Locally

```bash
git clone https://github.com/fisayojiboye/Online-Payment-Fraud-Detection.git
cd Online-Payment-Fraud-Detection
pip install -r requirements.txt
streamlit run app.py
```

---

### 🔮 Future Improvements

* Add SHAP values for detailed feature explanations
* Build a FastAPI backend for real-time integration
* Implement user login and transaction history
* Add more advanced features (transaction velocity, device info, etc.)
* Containerize with Docker for scalable deployment

---

### 👤 About the Author
Fisayo Ajiboye
Data Scientist
I am a passionate Data Scientist with strong expertise in building end-to-end machine learning solutions, particularly in the financial domain. This project showcases my ability to handle large-scale imbalanced datasets, perform deep feature engineering, optimize high-performance models (XGBoost), and deploy production-ready applications using modern tools like Streamlit.
My focus is on developing practical, explainable, and impactful AI systems that solve real business problems — from fraud detection to predictive analytics.
I am always open to collaboration, new opportunities, and discussions on data science and machine learning.
Connect with me:

💼LinkedIn: http://www.linkedin.com/in/oluwafisayomi-ajiboye-8a4902124
💻GitHub: https://github.com/fisayojiboye
✍️Medium: https://medium.com/@oluwafisayomiajiboye/%EF%B8%8Fi-built-an-ai-fraud-detection-app-that-catches-95-8-of-fraud-heres-how-1acab771c904

⭐ Feel free to test the live demo and share your feedback!

