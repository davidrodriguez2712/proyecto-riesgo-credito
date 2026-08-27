from pathlib import Path

import streamlit as st

from dashboard_data import DECILE_KS_LIFT, MODEL_EVALUATION_FIGURES, PORTFOLIO_MANAGEMENT
from layout import render_header

PROJECT_ROOT = Path(__file__).resolve().parents[1]

render_header()
st.subheader("Evaluación del Modelo")

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

st.subheader("Interpretabilidad (SHAP)")

shap_col_1, shap_col_2 = st.columns(2)
with shap_col_1:
    st.image(str(PROJECT_ROOT / MODEL_EVALUATION_FIGURES["shap_importance"]), use_container_width=True)
    st.caption("SHAP importance — gráfico original de 04_model_evaluation.ipynb")
with shap_col_2:
    st.image(str(PROJECT_ROOT / MODEL_EVALUATION_FIGURES["shap_individual_importance"]), use_container_width=True)
    st.caption("SHAP individual importance — gráfico original de 04_model_evaluation.ipynb")

dist_col, rel_col = st.columns(2)
with dist_col:
    st.image(str(PROJECT_ROOT / MODEL_EVALUATION_FIGURES["dist_buenos_malos_decil"]), use_container_width=True)
    st.caption("Distribución de buenos/malos por decil — gráfico original de 04_model_evaluation.ipynb")
with rel_col:
    st.image(str(PROJECT_ROOT / MODEL_EVALUATION_FIGURES["relacion_shap_features_values"]), use_container_width=True)
    st.caption("Relación SHAP vs valores de features — gráfico original de 04_model_evaluation.ipynb")
