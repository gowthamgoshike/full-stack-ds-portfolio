import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# CONNECTION CONFIG
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("📊 Enterprise Retail Analytics")
st.caption("Architecture: Streamlit (Frontend) → FastAPI (Backend) → MySQL (DB)")

# --- API HELPER ---
def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.exceptions.ConnectionError:
        st.error("API is Offline! Run 'uvicorn api_server:app --reload' in a separate terminal.")
        return None

# --- UI TABS ---
tab1, tab2 = st.tabs(["📉 Outlier Detection", "🧠 AI Predictions"])

with tab1:
    st.header("Financial Anomaly Detection")
    if st.button("Scan Transactions"):
        data = fetch_data("/analysis/outliers")
        
        if data:
            col1, col2, col3 = st.columns(3)
            col1.metric("Outliers Found", data['outlier_count'])
            col2.metric("Lower Fence", f"${data['lower_fence']:.2f}")
            col3.metric("Upper Fence", f"${data['upper_fence']:.2f}")
            
            if data['data']:
                df = pd.DataFrame(data['data'])
                st.write("### Flagged Transactions")
                st.dataframe(df)
                
                # Simple visual
                fig = px.bar(df, x='txn_id', y='amount', color='category', title="Outlier Magnitudes")
                st.plotly_chart(fig)
            else:
                st.success("No anomalies detected.")

with tab2:
    st.header("Bayesian Risk Engine")
    cat = st.selectbox("Select Category", ["Electronics", "Fashion"])
    
    if st.button("Predict Return Risk"):
        result = fetch_data(f"/prediction/return-risk?category={cat}")
        
        if result:
            prob = result['return_probability']
            st.metric("Return Probability", f"{prob:.2%}")
            
            if result['risk_verdict'] == "High Risk":
                st.error("⚠️ HIGH RISK: Investigate pricing strategy.")
            else:
                st.success("✅ SAFE: Low return volume.")