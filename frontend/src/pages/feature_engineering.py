from pathlib import Path

import streamlit as st

from dashboard_data import (
    FE_FIGURES,
    FEATURE_ENGINEERING_EVALUATION,
    FEATURE_SELECTION_RULES,
    PREPROCESSING_PIPELINE,
    VIF_TABLE,
)
from layout import render_header

PROJECT_ROOT = Path(__file__).resolve().parents[1]

render_header()
st.subheader("Feature Engineering")

st.write(
    "Pipeline de preprocessing aplicado antes de entrenar los modelos, en orden de ejecución:"
)

for i, paso in enumerate(PREPROCESSING_PIPELINE, start=1):
    with st.container(border=True):
        st.markdown(f"**{i}. {paso['paso']}**")
        st.markdown(paso["detalle"])

st.subheader("Selección de features")
st.dataframe(FEATURE_SELECTION_RULES, use_container_width=True, hide_index=True)
st.caption("ROC AUC, Gini y % missing univariado por feature, con la regla de decisión aplicada.")

st.subheader("Evaluación de la transformación por feature")
st.dataframe(FEATURE_ENGINEERING_EVALUATION, use_container_width=True, hide_index=True)
st.caption("Función de suavizado (logarithmic/polynomial) y AUC train/val obtenidos con esa transformación.")

st.subheader("Multicolinealidad (VIF)")
st.dataframe(VIF_TABLE, use_container_width=True, hide_index=True)
st.caption("VIF calculado sobre las variables ya transformadas a log-odds; todas por debajo del umbral de colinealidad (10).")

st.subheader("Relación Logit vs valores de la feature")
st.image(str(PROJECT_ROOT / FE_FIGURES["logit_vs_feature_values"]), use_container_width=True)
