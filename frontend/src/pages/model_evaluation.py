import streamlit as st

from dashboard_data import DECILE_KS_LIFT, PORTFOLIO_MANAGEMENT
from layout import render_header

render_header()
st.subheader("Model Evaluation")

st.write(
    "Estos análisis sustentan los thresholds de banda de riesgo usados en producción "
    "(`clasificar_cliente()` del backend): Bajo Riesgo (PD ≤ 0.0121), Medio Riesgo (PD ≤ 0.031), "
    "Alto Riesgo (PD ≤ 0.167) y Muy Alto Riesgo (PD > 0.167)."
)

st.subheader("Deciles / KS / Lift por banda de riesgo")
st.dataframe(DECILE_KS_LIFT, use_container_width=True, hide_index=True)

st.subheader("Gestión de Portafolio (clasificación económica)")
st.dataframe(PORTFOLIO_MANAGEMENT, use_container_width=True, hide_index=True)
st.caption(
    "Saldo, participación, tasa activa, spread, provisiones, utilidad neta y ROA por segmento de riesgo — "
    "con este análisis se validó dónde cortar cada banda."
)
