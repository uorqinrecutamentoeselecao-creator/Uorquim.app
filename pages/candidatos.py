import streamlit as st
import gspread
import requests
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Uorquin", layout="wide")

# =========================
# CSS PROFISSIONAL
# =========================
st.markdown("""
<style>
.main {
    background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
}

.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

h1, h2, h3 {
    color: #1f2c4c;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 48px;
    font-weight: 600;
    background: #2563eb;
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background: #1d4ed8;
}

.card {
    padding: 25px;
    border-radius: 16px;
    background: white;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.image("logo.png", width=180)
st.markdown("<h2 style='text-align:center;'>Crie seu currículo profissional em poucos minutos</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Preencha seus dados e aumente suas chances de contratação</p>", unsafe_allow_html=True)

# =========================
# CONTROLE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1

if "dados" not in st.session_state:
    st.session_state.dados = {}

# =========================
# PROGRESSO
# =========================
progress = st.session_state.step / 5
st.progress(progress)

# =========================
# ETAPA 1
# =========================
if st.session_state.step == 1:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📌 Dados Pessoais")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")
        idade = st.number_input("Idade", 0, 100)

    with col2:
        endereco = st.text_input("Endereço")
        estado = st.selectbox("Estado", ["BA","SP","RJ","MG"])
        cidade = st.text_input("Cidade")
        salario = st.text_input("Pretensão salarial")
        area = st.text_input("Área de interesse")

    st.markdown("---")

    if st.button("Continuar ➡️"):
        st.session_state.dados["pessoais"] = {
            "nome": nome,
            "cpf": cpf,
            "telefone": telefone,
            "email": email,
            "idade": idade,
            "endereco": endereco,
            "cidade": cidade,
            "estado": estado,
            "salario": salario,
            "area": area
        }

        st.session_state.step = 2
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ETAPA FINAL
# =========================
elif st.session_state.step == 2:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎯 Finalização")

    objetivo = st.text_area("Fale um pouco sobre seus objetivos profissionais")

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 1
        st.rerun()

    if col2.button("Finalizar Cadastro 🚀"):

        st.success("✅ Cadastro realizado com sucesso!")

        st.balloons()

    st.markdown('</div>', unsafe_allow_html=True)
