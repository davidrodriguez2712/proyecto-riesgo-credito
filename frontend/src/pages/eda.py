from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from dashboard_data import (
    EDA_FIGURES,
    EDA_INFORMATION_VALUE,
    EDA_MISSING,
    EDA_OUTLIERS_IQR,
    EDA_OVERVIEW,
    EDA_PSI_TRAIN_TEST,
    EDA_TARGET_SUMMARY,
)
from layout import render_header

PROJECT_ROOT = Path(__file__).resolve().parents[3]

render_header()
st.subheader("EDA - Exploratory Data Analysis")

st.subheader("Overview")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Filas", f"{EDA_OVERVIEW['filas']:,}")
m2.metric("Columnas", EDA_OVERVIEW["columnas"])
m3.metric("Missing (celdas)", f"{EDA_OVERVIEW['missing_global']:,}")
m4.metric("Features con missing", EDA_OVERVIEW["features_con_missing"])
m5.metric("Filas duplicadas", EDA_OVERVIEW["filas_duplicadas"])

target_col, missing_col = st.columns(2)

with target_col:
    st.subheader("Target Balance")
    fig_target = go.Figure(
        go.Bar(
            x=["No Default (0)", "Default (1)"],
            y=[EDA_TARGET_SUMMARY["negative_rate"], EDA_TARGET_SUMMARY["positive_rate"]],
            marker_color=["#2ecc71", "#e74c3c"],
            text=[f"{EDA_TARGET_SUMMARY['negative_rate']:.2%}", f"{EDA_TARGET_SUMMARY['positive_rate']:.2%}"],
            textposition="outside",
        )
    )
    fig_target.update_layout(template="plotly_dark", height=350, yaxis_tickformat=".0%")
    st.plotly_chart(fig_target, use_container_width=True)
    st.caption(f"Ratio de desbalanceo: {EDA_TARGET_SUMMARY['imbalance_rate']} — {EDA_TARGET_SUMMARY['nivel_desbalance']}")

with missing_col:
    st.subheader("Missing Values")
    fig_missing = go.Figure(
        go.Bar(
            x=[d["missing_pct"] for d in EDA_MISSING],
            y=[d["feature"] for d in EDA_MISSING],
            orientation="h",
            marker_color="#f1c40f",
        )
    )
    fig_missing.update_layout(template="plotly_dark", height=350, xaxis_title="% missing")
    st.plotly_chart(fig_missing, use_container_width=True)
    st.caption("Únicas dos features con nulos en el dataset.")

iv_col, out_col = st.columns(2)

with iv_col:
    st.subheader("Information Value")
    features_iv = [d["feature"] for d in EDA_INFORMATION_VALUE][::-1]
    ivs = [d["iv"] for d in EDA_INFORMATION_VALUE][::-1]
    fig_iv = go.Figure(go.Bar(x=ivs, y=features_iv, orientation="h", marker_color="#3498db"))
    fig_iv.update_layout(template="plotly_dark", height=400, xaxis_title="Information Value")
    st.plotly_chart(fig_iv, use_container_width=True)
    st.caption("IV > 0.3 (RevolvingUtilization) indica poder predictivo muy fuerte; age es fuerte/medio.")

with out_col:
    st.subheader("Outliers (IQR) por variable")
    features_out = [d["feature"] for d in EDA_OUTLIERS_IQR][::-1]
    pct_out = [d["pct_fuera_rango"] for d in EDA_OUTLIERS_IQR][::-1]
    fig_out = go.Figure(go.Bar(x=pct_out, y=features_out, orientation="h", marker_color="#e67e22"))
    fig_out.update_layout(template="plotly_dark", height=400, xaxis_title="% de registros fuera de rango")
    st.plotly_chart(fig_out, use_container_width=True)

st.subheader("Distribuciones y correlaciones")
fig_dist_col, fig_corr_col = st.columns(2)
with fig_dist_col:
    st.image(str(PROJECT_ROOT / EDA_FIGURES["distribucion_numericas"]), use_container_width=True)
with fig_corr_col:
    st.image(str(PROJECT_ROOT / EDA_FIGURES["correlaciones"]), use_container_width=True)

fig_target_col, fig_missing_col = st.columns(2)
with fig_target_col:
    st.image(str(PROJECT_ROOT / EDA_FIGURES["analisis_target"]), use_container_width=True)
with fig_missing_col:
    st.image(str(PROJECT_ROOT / EDA_FIGURES["missing_graph"]), use_container_width=True)

st.subheader("PSI Train vs Test")
st.dataframe(EDA_PSI_TRAIN_TEST, use_container_width=True, hide_index=True)
