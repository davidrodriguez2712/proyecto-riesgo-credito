import streamlit as st

st.set_page_config(
    page_title="Credit Risk Project - Give Me Credit",
    page_icon=":shield:",
    layout="wide",
)

pages = [
    st.Page("pages/home.py", title="Inicio", default=True),
    st.Page("pages/eda.py", title="EDA"),
    st.Page("pages/feature_engineering.py", title="Feature Engineering"),
    st.Page("pages/model_training.py", title="Entrenamiento del Modelo"),
    st.Page("pages/model_evaluation.py", title="Evaluación del Modelo"),
    st.Page("pages/monitoring.py", title="Monitoreo"),
    st.Page("pages/make_prediction.py", title="Realizar Predicción"),
]

pg = st.navigation(pages)
pg.run()
