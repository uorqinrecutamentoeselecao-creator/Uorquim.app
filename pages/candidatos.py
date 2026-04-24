import streamlit as st
import gspread
import requests
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# CONFIG
st.set_page_config(page_title="Uorquin", layout="wide")

# =========================
# CSS PROFISSIONAL
# =========================
st.markdown("""
<style>
header {visibility: hidden;}
body {background-color: #F8FAFC;}

.main-container {
    max-width: 1000px;
    margin: auto;
}

.card {
    background: white;
    padding: 40px;
    border-radius: 20px;
    border: 1px solid #E2E8F0;
    margin-top: 30px;
}

.title {
    font-size: 28px;
    font-weight: 700;
    color: #0F172A;
}

.subtitle {
    color: #64748B;
    margin-bottom: 20px;
}

.progress-bar {
    height: 8px;
    background: #E2E8F0;
    border-radius: 10px;
    margin-bottom: 30px;
}

.progress-fill {
    height: 8px;
    background: #22C55E;
    border-radius: 10px;
}

.stButton>button {
    height: 50px;
    border-radius: 12px;
    font-weight: 600;
}

.primary button {
    background-color: #22C55E;
    color: white;
}

.secondary button {
    background-color: white;
    border: 1px solid #CBD5E1;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.image("logo.png", width=180)
st.markdown("<h2 style='text-align:center'>Crie seu currículo profissional</h2>", unsafe_allow_html=True)

# =========================
# LISTAS
# =========================
estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
"MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]

@st.cache_data
def buscar_cidades(uf):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    r = requests.get(url)
    if r.status_code == 200:
        return sorted([c["nome"] for c in r.json()])
    return []

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) >= 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    return cpf

def validar_cpf_simples(cpf):
    return len(re.sub(r'\D', '', cpf)) == 11

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def formatar_telefone(tel):
    tel = re.sub(r'\D', '', tel)
    if len(tel) >= 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:11]}"
    return tel

def formatar_cep(cep):
    cep = re.sub(r'\D', '', cep)
    if len(cep) >= 8:
        return f"{cep[:5]}-{cep[5:8]}"
    return cep

# =========================
# GOOGLE
# =========================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    return client.open("Banco_Uorquin").sheet1

def salvar_dados(dados):
    planilha = conectar_planilha()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    planilha.append_row([data_hora, dados["pessoais"]["nome"]])

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
progress = (st.session_state.step / 5) * 100
st.markdown(f"""
<div class="progress-bar">
    <div class="progress-fill" style="width:{progress}%"></div>
</div>
""", unsafe_allow_html=True)

# =========================
# ETAPA 1
# =========================
if st.session_state.step == 1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Dados Pessoais</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Preencha suas informações básicas</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome Completo")
        cpf = formatar_cpf(st.text_input("CPF"))
        telefone = formatar_telefone(st.text_input("Telefone"))
        email = st.text_input("Email")

    with col2:
        estado = st.selectbox("Estado", estados)
        cidade = st.selectbox("Cidade", buscar_cidades(estado))
        cep = formatar_cep(st.text_input("CEP"))
        area = st.text_input("Área")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button("Continuar ➡️", use_container_width=True):
            if not validar_cpf_simples(cpf):
                st.error("CPF inválido")
            elif not validar_email(email):
                st.error("Email inválido")
            else:
                st.session_state.dados["pessoais"] = {"nome": nome}
                st.session_state.step = 2
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ETAPA FINAL (SIMPLIFICADA)
# =========================
elif st.session_state.step == 2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Finalização</div>", unsafe_allow_html=True)

    objetivo = st.text_area("Objetivo profissional")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Voltar"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Finalizar", use_container_width=True):
            salvar_dados(st.session_state.dados)
            st.success("Cadastro realizado com sucesso!")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
