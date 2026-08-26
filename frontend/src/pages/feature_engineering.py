import streamlit as st

from dashboard_data import PREPROCESSING_PIPELINE
from layout import render_header

render_header()
st.subheader("Feature Engineering")

st.write(
    "Pipeline de preprocessing aplicado antes de entrenar los modelos, en orden de ejecución:"
)

for i, paso in enumerate(PREPROCESSING_PIPELINE, start=1):
    with st.container(border=True):
        st.markdown(f"**{i}. {paso['paso']}**")
        st.markdown(paso["detalle"])
