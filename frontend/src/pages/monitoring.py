from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from dashboard_data import MONITORING_FIGURES, PSI_SNAPSHOT, TARGET_DRIFT
from layout import render_header

PROJECT_ROOT = Path(__file__).resolve().parents[3]

MONITORING_SECTIONS = [
    ("performance", "Performance"),
    ("drift", "Drift"),
    ("shap", "SHAP"),
    ("calibracion", "Calibración"),
]


def render_image_grid(paths: list[str]) -> None:
    cols = st.columns(2)
    for i, path in enumerate(paths):
        with cols[i % 2]:
            st.image(str(PROJECT_ROOT / path), use_container_width=True)


render_header()
st.subheader("Monitoreo")

psi_col, target_col = st.columns(2)

with psi_col:
    st.subheader("Drift de Datos (PSI)")
    st.dataframe(PSI_SNAPSHOT, use_container_width=True, hide_index=True)
    st.caption("Snapshot del último periodo monitoreado (2026-06)")

with target_col:
    st.subheader("Drift del Target")
    periodos_td = [p for p, _, _ in TARGET_DRIFT]
    bad_rate_td = [b for _, b, _ in TARGET_DRIFT]
    pd_td = [p for _, _, p in TARGET_DRIFT]

    fig_target = go.Figure()
    fig_target.add_scatter(name="Bad Rate", x=periodos_td, y=bad_rate_td, mode="lines+markers", line_color="#e67e22")
    fig_target.add_scatter(name="PD", x=periodos_td, y=pd_td, mode="lines+markers", line_color="#3498db")
    fig_target.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig_target, use_container_width=True)

for key, titulo in MONITORING_SECTIONS:
    st.subheader(titulo)
    render_image_grid(MONITORING_FIGURES[key])
