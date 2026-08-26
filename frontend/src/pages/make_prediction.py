import requests
import streamlit as st

from api_client import predict
from config import RISK_BAND_COLORS
from dashboard_data import BEST_MODEL, DATASET_INFO
from layout import render_header

render_header()
st.subheader("Make Prediction")

with st.form("prediction_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        revolving_utilization = st.number_input(
            "Revolving Utilization Of Unsecured Lines", min_value=0.0, value=0.5, step=0.01, format="%.4f"
        )
        age = st.number_input("Age", min_value=18, max_value=110, value=35, step=1)
        past_due_30_59 = st.number_input(
            "Number Of Time 30-59 Days Past Due Not Worse", min_value=0, value=0, step=1
        )
        debt_ratio = st.number_input("Debt Ratio", min_value=0.0, value=0.3, step=0.01, format="%.4f")
        monthly_income = st.number_input("Monthly Income", min_value=0.0, value=5000.0, step=100.0)
    with col_b:
        open_credit_lines = st.number_input(
            "Number Of Open Credit Lines And Loans", min_value=0, value=5, step=1
        )
        times_90_days_late = st.number_input("Number Of Times 90 Days Late", min_value=0, value=0, step=1)
        real_estate_loans = st.number_input(
            "Number Real Estate Loans Or Lines", min_value=0, value=1, step=1
        )
        past_due_60_89 = st.number_input(
            "Number Of Time 60-89 Days Past Due Not Worse", min_value=0, value=0, step=1
        )
        dependents = st.number_input("Number Of Dependents", min_value=0.0, value=0.0, step=1.0)

    submitted = st.form_submit_button("Predict Probability")

if submitted:
    payload = {
        "RevolvingUtilizationOfUnsecuredLines": revolving_utilization,
        "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": past_due_30_59,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": monthly_income,
        "NumberOfOpenCreditLinesAndLoans": open_credit_lines,
        "NumberOfTimes90DaysLate": times_90_days_late,
        "NumberRealEstateLoansOrLines": real_estate_loans,
        "NumberOfTime60-89DaysPastDueNotWorse": past_due_60_89,
        "NumberOfDependents": dependents,
    }
    try:
        with st.spinner("Calculando probabilidad..."):
            result = predict(payload)
        st.session_state["prediction_result"] = result
    except requests.RequestException as exc:
        st.session_state["prediction_result"] = None
        st.error(f"No se pudo obtener la predicción del backend: {exc}")

result_col, key_info_col = st.columns(2)

with result_col:
    st.subheader("Prediction Result")
    result = st.session_state.get("prediction_result")
    if result is None:
        st.info("Completa el formulario y presiona 'Predict Probability' para ver el resultado.")
    else:
        pd_estimada = result["pd_estimada"]
        banda = result["banda_riesgo"]
        color = RISK_BAND_COLORS.get(banda, "#888888")
        st.markdown(f"<h1 style='color:{color}'>{pd_estimada:.2%}</h1>", unsafe_allow_html=True)
        st.markdown(
            f"Risk Score: <span style='color:{color};font-weight:600'>{banda}</span>",
            unsafe_allow_html=True,
        )
        st.progress(min(pd_estimada, 1.0))
        st.caption(f"Modelo: {result['version_modelo']}")

with key_info_col:
    st.subheader("Key Information")
    st.markdown(f"**Model Type:** {BEST_MODEL['nombre']}")
    st.markdown(f"**Target:** {DATASET_INFO['target']}")
    st.markdown("**Evaluation Metric:** AUC")
    st.markdown(f"**Best AUC (CV):** {BEST_MODEL['auc_cv']}")
    st.markdown(f"**Default Rate (Train):** {DATASET_INFO['default_rate_train']:.2%}")
    st.markdown(f"**Población (Train):** {DATASET_INFO['poblacion_train']:,}")
