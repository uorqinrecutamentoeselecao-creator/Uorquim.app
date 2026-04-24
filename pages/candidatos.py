import streamlit as st
import gspread
import requests
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Uorquin", layout="centered")

# =========================
# 🎨 CSS PROFISSIONAL
# =========================
st.markdown("""
<style>

/* FUNDO */
body {
    background-color: #f5f7fb;
}

/* TÍTULO */
.title {
    text-align:center;
    font-size:28px;
    font-weight:700;
    color:#1f2c56;
}

/* SUB */
.subtitle {
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

/* CARD */
.card {
    background:white;
    padding:25px;
    border-radius:14px;
    box-shadow:0px 8px 25px rgba(0,0,0,0.05);
}

/* BOTÃO PRINCIPAL */
.stButton > button {
    background: linear-gradient(135deg, #1f2c56, #2f80ed);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 12px 20px;
    font-weight: 600;
}

/* BOTÃO ADICIONAR */
.add-btn button {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
}

/* BOTÃO VOLTAR */
.back-btn button {
    background: #eef1f7;
    color: #333;
}

/* INPUTS */
.stTextInput input, .stSelectbox div {
    border-radius: 10px !important;
    border: 1px solid #dfe3eb !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.image("logo.png", width=180)
st.markdown("<div class='title'>Crie seu currículo profissional</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Leva menos de 3 minutos</div>", unsafe_allow_html=True)

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

# =========================
# FORMATADORES
# =========================
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

    if not planilha.row_values(1):
        planilha.append_row(["Data","Nome","CPF","Email","Telefone","Cidade","Estado"])

    p = dados["pessoais"]

    planilha.append_row([
        data_hora, p["nome"], p["cpf"], p["email"], p["telefone"], p["cidade"], p["estado"]
    ])

# =========================
# PDF
# =========================
def gerar_pdf(dados):
    file_name = "curriculo.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    c.drawString(100, 750, dados["pessoais"]["nome"])
    c.save()
    return file_name

# =========================
# CONTROLE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1

if "dados" not in st.session_state:
    st.session_state.dados = {}

if "qtd_exp" not in st.session_state:
    st.session_state.qtd_exp = 1

if "exp_aberta" not in st.session_state:
    st.session_state.exp_aberta = 0

# =========================
# PROGRESSO
# =========================
st.progress(st.session_state.step / 3)

# =========================
# ETAPA 1
# =========================
if st.session_state.step == 1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Dados Pessoais")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome")
        cpf = formatar_cpf(st.text_input("CPF"))
        telefone = formatar_telefone(st.text_input("Telefone"))
        email = st.text_input("Email")

    with col2:
        estado = st.selectbox("Estado", estados)
        cidade = st.selectbox("Cidade", buscar_cidades(estado))
        endereco = st.text_input("Endereço")

    if st.button("Continuar ➡️"):
        if not validar_cpf_simples(cpf):
            st.error("CPF inválido")
        elif not validar_email(email):
            st.error("Email inválido")
        else:
            st.session_state.dados["pessoais"] = {
                "nome": nome,
                "cpf": cpf,
                "telefone": telefone,
                "email": email,
                "cidade": cidade,
                "estado": estado,
                "endereco": endereco
            }
            st.session_state.step = 2
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ETAPA 2
# =========================
elif st.session_state.step == 2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Experiência")

    experiencias = []

    for i in range(st.session_state.qtd_exp):
        with st.expander(f"Experiência {i+1}", expanded=(i == st.session_state.exp_aberta)):
            empresa = st.text_input("Empresa", key=f"empresa_{i}")
            funcao = st.text_input("Função", key=f"funcao_{i}")

            experiencias.append({
                "empresa": empresa,
                "funcao": funcao
            })

    if st.session_state.qtd_exp < 4:
        if st.button("➕ Adicionar experiência"):
            st.session_state.qtd_exp += 1
            st.session_state.exp_aberta = st.session_state.qtd_exp - 1
            st.rerun()

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 1
        st.rerun()

    if col2.button("Continuar ➡️"):
        st.session_state.dados["experiencias"] = experiencias
        st.session_state.step = 3
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FINAL
# =========================
elif st.session_state.step == 3:

    if st.button("Finalizar"):
        salvar_dados(st.session_state.dados)
        pdf = gerar_pdf(st.session_state.dados)

        st.success("Cadastro realizado com sucesso!")

        with open(pdf, "rb") as f:
            st.download_button("📄 Baixar currículo", f)
