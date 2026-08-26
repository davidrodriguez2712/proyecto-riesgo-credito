import streamlit as st

from dashboard_data import (
    BEST_MODEL,
    DATASET_INFO,
    MODEL_SELECTION_NOTE,
    PORTFOLIO_MANAGEMENT,
    PREPROCESSING_PIPELINE,
)
from layout import render_header

render_header()

WORKFLOW_STAGES = [
    {
        "nombre": "EDA - Análisis Exploratorio de Datos",
        "detalle": ["Overview de datos", "Análisis de missings", "Detección de outliers", "Information Value"],
    },
    {
        "nombre": "Feature Engineering",
        "detalle": ["Log-Odds Rolling Smoothing", "Binning", "Manejo de outliers", "Selección de features"],
    },
    {
        "nombre": "Entrenamiento del Modelo",
        "detalle": ["Baseline de 6 modelos", "Tuning con Optuna", "Selección de campeón"],
    },
    {
        "nombre": "Evaluación del Modelo",
        "detalle": ["Validación en test set", "Deciles / KS / Lift", "Gestión de portafolio"],
    },
    {
        "nombre": "Monitoreo",
        "detalle": ["Data drift (PSI)", "Target drift", "AUC/Gini en el tiempo"],
    },
]

st.subheader("Resumen del Proyecto")
desc_col, download_col = st.columns([5, 1])
with desc_col:
    st.write(
        "Este proyecto predice la probabilidad de morosidad grave (90+ días de atraso) "
        "usando datos históricos de riesgo crediticio del dataset Give Me Credit."
    )
with download_col:
    st.button("Download Project PPT", disabled=True, help="Próximamente")

card_1, card_2, card_3, card_4, card_5 = st.columns(5)
with card_1:
    with st.container(border=True):
        st.markdown("**Objetivo de Negocio**")
        st.markdown("Estimar el riesgo crediticio para apoyar decisiones de originación y reducir pérdidas.")
with card_2:
    with st.container(border=True):
        st.markdown("**Variable Objetivo**")
        st.markdown(f"`{DATASET_INFO['target']}` (1 = Default, 0 = No Default)")
with card_3:
    with st.container(border=True):
        st.markdown("**Dataset**")
        st.markdown(f"{DATASET_INFO['poblacion_train']:,} clientes (train) · {DATASET_INFO['n_features']} features")
with card_4:
    with st.container(border=True):
        st.markdown("**Modelos Evaluados**")
        st.markdown(f"{DATASET_INFO['n_modelos_evaluados']} modelos comparados")
with card_5:
    with st.container(border=True):
        st.markdown("**Mejor Modelo**")
        st.markdown(f"{BEST_MODEL['nombre']} — AUC (CV) {BEST_MODEL['auc_cv']}")

st.subheader("Flujo del Proyecto – 5 Etapas")
stage_cols = st.columns(5)
for col, stage in zip(stage_cols, WORKFLOW_STAGES):
    with col:
        with st.container(border=True):
            st.markdown(f"**{stage['nombre']}**")
            for item in stage["detalle"]:
                st.markdown(f"- {item}")
            st.markdown(":white_check_mark: **Completado**")

highlight_fe, highlight_econ = st.columns(2)

with highlight_fe:
    st.subheader("Pipeline de Preprocessing")
    for paso in PREPROCESSING_PIPELINE:
        st.markdown(f"- **{paso['paso']}**")
    st.caption("Ver detalle completo en la página Feature Engineering.")

with highlight_econ:
    st.subheader("Clasificación Económica")
    econ_resumen = [
        {"Segmento": fila["segmento"], "ROA %": fila["roa_pct"], "Utilidad Neta": fila["utilidad_neta"]}
        for fila in PORTFOLIO_MANAGEMENT
    ]
    st.dataframe(econ_resumen, use_container_width=True, hide_index=True)
    st.caption("Gestión de portafolio con la que se validaron los thresholds de banda. Ver detalle en Evaluación del Modelo.")

st.subheader("¿Por qué CatBoost?")
st.info(MODEL_SELECTION_NOTE)
