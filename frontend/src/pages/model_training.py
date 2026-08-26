import plotly.graph_objects as go
import streamlit as st

from dashboard_data import BEST_MODEL, CALIBRATION_CURVE, FEATURE_IMPORTANCE_TOP10, MODEL_COMPARISON, MONITORING_AUC_GINI
from layout import render_header

render_header()
st.subheader("Entrenamiento del Modelo")

perf_col, auc_col = st.columns(2)

with perf_col:
    st.subheader("Resumen de Desempeño del Modelo")
    modelos = [m["modelo"] for m in MODEL_COMPARISON]
    aucs = [m["auc_cv"] for m in MODEL_COMPARISON]
    ginis = [round(2 * m["auc_cv"] - 1, 3) for m in MODEL_COMPARISON]

    fig_perf = go.Figure()
    fig_perf.add_bar(name="AUC", x=modelos, y=aucs, marker_color="#3498db")
    fig_perf.add_bar(name="Gini", x=modelos, y=ginis, marker_color="#2ecc71")
    fig_perf.update_layout(barmode="group", template="plotly_dark", height=400)
    st.plotly_chart(fig_perf, use_container_width=True)
    st.caption(f"Mejor Modelo: {BEST_MODEL['nombre']} (AUC CV: {BEST_MODEL['auc_cv']})")

with auc_col:
    st.subheader("AUC en el Tiempo (OOT)")
    periodos = [p for p, _, _ in MONITORING_AUC_GINI["mensual"]]
    aucs_mensual = [a for _, a, _ in MONITORING_AUC_GINI["mensual"]]
    ginis_mensual = [g for _, _, g in MONITORING_AUC_GINI["mensual"]]

    fig_auc = go.Figure()
    fig_auc.add_scatter(name="AUC", x=periodos, y=aucs_mensual, mode="lines+markers", line_color="#3498db")
    fig_auc.add_scatter(name="Gini", x=periodos, y=ginis_mensual, mode="lines+markers", line_color="#2ecc71")
    fig_auc.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_auc, use_container_width=True)
    st.caption("Desempeño estable en el tiempo")

fi_col, cal_col = st.columns(2)
with fi_col:
    st.subheader("Importancia de Variables (Top 10)")
    if FEATURE_IMPORTANCE_TOP10 is None:
        st.info("Próximamente — pendiente de exportar datos reales del notebook.")
    else:
        features = [d["feature"] for d in FEATURE_IMPORTANCE_TOP10][::-1]
        importances = [d["importance"] for d in FEATURE_IMPORTANCE_TOP10][::-1]

        fig_fi = go.Figure(go.Bar(x=importances, y=features, orientation="h", marker_color="#9b59b6"))
        fig_fi.update_layout(template="plotly_dark", height=400, xaxis_title="Mean |SHAP value|")
        st.plotly_chart(fig_fi, use_container_width=True)
        st.caption("Ver el gráfico SHAP original del notebook en la página Evaluación del Modelo.")
with cal_col:
    st.subheader("Curva de Calibración")
    if CALIBRATION_CURVE is None:
        st.info("Próximamente — pendiente de exportar datos reales del notebook.")
    else:
        pred_probs = [b["mean_predicted"] for b in CALIBRATION_CURVE]
        observed = [b["fraction_positives"] for b in CALIBRATION_CURVE]

        fig_cal = go.Figure()
        fig_cal.add_scatter(
            name="Modelo", x=pred_probs, y=observed, mode="lines+markers", line_color="#e67e22"
        )
        fig_cal.add_scatter(
            name="Perfectamente calibrado", x=[0, 1], y=[0, 1], mode="lines",
            line=dict(dash="dash", color="#7f8c8d"),
        )
        fig_cal.update_layout(
            template="plotly_dark", height=400,
            xaxis_title="Predicted probability (mean per bin)",
            yaxis_title="Observed fraction of positives",
        )
        st.plotly_chart(fig_cal, use_container_width=True)
