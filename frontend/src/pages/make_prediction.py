import base64

import requests
import streamlit as st

from api_client import predict
from config import RISK_BAND_COLORS
from layout import render_header

render_header()
st.subheader("Realizar Predicción")

with st.form("prediction_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        revolving_utilization = st.number_input(
            "Utilización Rotativa de Líneas No Aseguradas", min_value=0.0, value=0.5, step=0.01, format="%.4f"
        )
        age = st.number_input("Edad", min_value=18, max_value=110, value=35, step=1)
        past_due_30_59 = st.number_input(
            "N° de Veces con 30-59 Días de Atraso", min_value=0, value=0, step=1
        )
        debt_ratio = st.number_input("Ratio de Endeudamiento", min_value=0.0, value=0.3, step=0.01, format="%.4f")
        monthly_income = st.number_input("Ingreso Mensual", min_value=0.0, value=5000.0, step=100.0)
    with col_b:
        open_credit_lines = st.number_input(
            "N° de Líneas de Crédito y Préstamos Abiertos", min_value=0, value=5, step=1
        )
        times_90_days_late = st.number_input("N° de Veces con 90 Días de Atraso", min_value=0, value=0, step=1)
        real_estate_loans = st.number_input(
            "N° de Préstamos o Líneas Hipotecarias", min_value=0, value=1, step=1
        )
        past_due_60_89 = st.number_input(
            "N° de Veces con 60-89 Días de Atraso", min_value=0, value=0, step=1
        )
        dependents = st.number_input("N° de Dependientes", min_value=0.0, value=0.0, step=1.0)

    submitted = st.form_submit_button("Calcular Probabilidad")

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

st.subheader("Resultado de la Predicción")
result = st.session_state.get("prediction_result")
if result is None:
    st.info("Completa el formulario y presiona 'Calcular Probabilidad' para ver el resultado.")
else:
    pd_estimada = result["pd_estimada"]
    banda = result["banda_riesgo"]
    color = RISK_BAND_COLORS.get(banda, "#888888")
    st.markdown(f"<h1 style='color:{color}'>{pd_estimada:.2%}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"Nivel de Riesgo: <span style='color:{color};font-weight:600'>{banda}</span>",
        unsafe_allow_html=True,
    )
    st.progress(min(pd_estimada, 1.0))
    st.caption(f"Modelo: {result['version_modelo']}")

if result is not None:
    st.subheader("¿Qué impulsó esta predicción?")

    waterfall_png = base64.b64decode(result["shap_waterfall_png_base64"])
    st.image(waterfall_png, use_container_width=True)
    st.caption(
        "Waterfall SHAP oficial (shap.plots.waterfall) — contribución de cada feature al log-odds "
        "de la predicción, partiendo del valor base del modelo (E[f(X)]) hasta el valor final (f(x))."
    )
