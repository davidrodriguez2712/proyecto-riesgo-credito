import streamlit as st

st.set_page_config(
    page_title="Credit Risk Project - Give Me Credit",
    page_icon=":shield:",
    layout="wide",
)

pages = [
    st.Page("pages/home.py", title="Home", default=True),
    st.Page("pages/eda.py", title="EDA"),
    st.Page("pages/feature_engineering.py", title="Feature Engineering"),
    st.Page("pages/model_training.py", title="Model Training"),
    st.Page("pages/model_evaluation.py", title="Model Evaluation"),
    st.Page("pages/monitoring.py", title="Monitoring"),
    st.Page("pages/make_prediction.py", title="Make Prediction"),
]

pg = st.navigation(pages)
pg.run()
