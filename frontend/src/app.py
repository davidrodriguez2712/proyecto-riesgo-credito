import plotly.graph_objects as go
import requests
import streamlit as st

from api_client import predict
from config import RISK_BAND_COLORS
from dashboard_data import (
    BEST_MODEL,
    DATASET_INFO,
    FEATURE_IMPORTANCE_TOP10,
    MODEL_COMPARISON,
    MONITORING_AUC_GINI,
    PSI_SNAPSHOT,
    SCORE_DISTRIBUTION,
    TARGET_DRIFT,
)

st.set_page_config(
    page_title="Credit Risk Project - Give Me Credit",
    page_icon=":shield:",
    layout="wide",
)

WORKFLOW_STAGES = [
    {
        "nombre": "EDA - Exploratory Data Analysis",
        "detalle": ["Overview de datos", "Análisis de missings", "Detección de outliers", "Information Value"],
    },
    {
        "nombre": "Feature Engineering",
        "detalle": ["Encoding WOE", "Binning", "Manejo de outliers", "Selección de features"],
    },
    {
        "nombre": "Model Training",
        "detalle": ["Baseline de 6 modelos", "Tuning con Optuna", "Selección de campeón"],
    },
    {
        "nombre": "Model Evaluation",
        "detalle": ["Validación en test set", "Deciles / KS / Lift", "Gestión de portafolio"],
    },
    {
        "nombre": "Monitoring",
        "detalle": ["Data drift (PSI)", "Target drift", "AUC/Gini en el tiempo"],
    },
]

with st.sidebar:
    st.markdown("### CREDIT RISK\nML SYSTEM")
    st.markdown("---")
    st.markdown("**Overview**")
    st.markdown("**Project Flow**")
    for i, stage in enumerate(WORKFLOW_STAGES, start=1):
        st.markdown(f"{i}. {stage['nombre']} — :white_check_mark: Completado")
    st.markdown("---")
    st.markdown("**Predictions**")
    st.markdown("- Make Prediction")
    st.markdown("---")
    st.markdown("**Documentation**")
    st.markdown("- Project Report (PPT)")

title_col, badge_col = st.columns([6, 1])
with title_col:
    st.title("Credit Risk Project – Give Me Credit (Kaggle)")
    st.caption("End-to-End ML System for Credit Risk Prediction")
with badge_col:
    st.markdown(
        "<span style='background-color:#2ecc71;color:#0b1220;"
        "padding:4px 10px;border-radius:12px;font-weight:600;'>Production</span>",
        unsafe_allow_html=True,
    )

overview_section = st.container()
with overview_section:
    st.subheader("Project Overview")
    desc_col, download_col = st.columns([5, 1])
    with desc_col:
        st.write(
            "Este proyecto predice la probabilidad de morosidad grave (90+ días de atraso) "
            "usando datos históricos de riesgo crediticio del dataset Give Me Some Credit."
        )
    with download_col:
        st.button("Download Project PPT", disabled=True, help="Próximamente")

    card_1, card_2, card_3, card_4, card_5 = st.columns(5)
    with card_1:
        st.metric("Business Goal", "Estimar riesgo crediticio")
    with card_2:
        st.metric("Target Variable", DATASET_INFO["target"])
    with card_3:
        st.metric("Dataset", f"{DATASET_INFO['poblacion_train']:,} clientes · {DATASET_INFO['n_features']} features")
    with card_4:
        st.metric("Models Evaluated", f"{DATASET_INFO['n_modelos_evaluados']} modelos")
    with card_5:
        st.metric("Best Model", f"{BEST_MODEL['nombre']}", f"AUC (CV) {BEST_MODEL['auc_cv']}")

workflow_section = st.container()
with workflow_section:
    st.subheader("Project Workflow – 5 Stages")
    stage_cols = st.columns(5)
    for col, stage in zip(stage_cols, WORKFLOW_STAGES):
        with col:
            with st.container(border=True):
                st.markdown(f"**{stage['nombre']}**")
                for item in stage["detalle"]:
                    st.markdown(f"- {item}")
                st.markdown(":white_check_mark: **Completado**")

performance_section = st.container()
with performance_section:
    perf_col, auc_col = st.columns(2)

    with perf_col:
        st.subheader("Model Performance Summary")
        modelos = [m["modelo"] for m in MODEL_COMPARISON]
        aucs = [m["auc_cv"] for m in MODEL_COMPARISON]
        ginis = [round(2 * m["auc_cv"] - 1, 3) for m in MODEL_COMPARISON]

        fig_perf = go.Figure()
        fig_perf.add_bar(name="AUC", x=modelos, y=aucs, marker_color="#3498db")
        fig_perf.add_bar(name="Gini", x=modelos, y=ginis, marker_color="#2ecc71")
        fig_perf.update_layout(barmode="group", template="plotly_dark", height=400)
        st.plotly_chart(fig_perf, use_container_width=True)
        st.caption(f"Best Model: {BEST_MODEL['nombre']} (AUC CV: {BEST_MODEL['auc_cv']})")

    with auc_col:
        st.subheader("AUC Over Time (OOT)")
        periodos = [p for p, _, _ in MONITORING_AUC_GINI["mensual"]]
        aucs_mensual = [a for _, a, _ in MONITORING_AUC_GINI["mensual"]]
        ginis_mensual = [g for _, _, g in MONITORING_AUC_GINI["mensual"]]

        fig_auc = go.Figure()
        fig_auc.add_scatter(name="AUC", x=periodos, y=aucs_mensual, mode="lines+markers", line_color="#3498db")
        fig_auc.add_scatter(name="Gini", x=periodos, y=ginis_mensual, mode="lines+markers", line_color="#2ecc71")
        fig_auc.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_auc, use_container_width=True)
        st.caption("Stable performance over time")

    fi_col, score_col = st.columns(2)
    with fi_col:
        st.subheader("Feature Importance (Top 10)")
        if FEATURE_IMPORTANCE_TOP10 is None:
            st.info("Próximamente — pendiente de exportar datos reales del notebook.")
        else:
            st.write(FEATURE_IMPORTANCE_TOP10)
    with score_col:
        st.subheader("Score Distribution")
        if SCORE_DISTRIBUTION is None:
            st.info("Próximamente — pendiente de exportar datos reales del notebook.")
        else:
            st.write(SCORE_DISTRIBUTION)

drift_section = st.container()
with drift_section:
    psi_col, target_col = st.columns(2)

    with psi_col:
        st.subheader("Data Drift (PSI)")
        st.dataframe(PSI_SNAPSHOT, use_container_width=True, hide_index=True)
        st.caption("Snapshot del último periodo monitoreado (2026-06)")

    with target_col:
        st.subheader("Target Drift")
        periodos_td = [p for p, _, _ in TARGET_DRIFT]
        bad_rate_td = [b for _, b, _ in TARGET_DRIFT]
        pd_td = [p for _, _, p in TARGET_DRIFT]

        fig_target = go.Figure()
        fig_target.add_scatter(name="Bad Rate", x=periodos_td, y=bad_rate_td, mode="lines+markers", line_color="#e67e22")
        fig_target.add_scatter(name="PD", x=periodos_td, y=pd_td, mode="lines+markers", line_color="#3498db")
        fig_target.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_target, use_container_width=True)

prediction_section = st.container()
with prediction_section:
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
