import streamlit as st


def render_header() -> None:
    title_col, badge_col = st.columns([6, 1])
    with title_col:
        st.title("Credit Risk Project – Give Me Credit")
        st.caption("Sistema de Machine Learning de extremo a extremo para predicción de riesgo crediticio")
    with badge_col:
        st.markdown(
            "<span style='background-color:#2ecc71;color:#0b1220;"
            "padding:4px 10px;border-radius:12px;font-weight:600;'>Production</span>",
            unsafe_allow_html=True,
        )
