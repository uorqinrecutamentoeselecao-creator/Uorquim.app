import streamlit as st

st.set_page_config(page_title="Uorquin - Portal", layout="wide")

st.image("logo.png", width=200)

st.markdown("""
<h1 style='text-align:center'>🚀 Portal de Vagas Uorquin</h1>
<p style='text-align:center'>Escolha uma opção no menu lateral</p>
""", unsafe_allow_html=True)

st.divider()

st.info("👉 Use o menu lateral para acessar Vagas ou Cadastro de Currículo")
