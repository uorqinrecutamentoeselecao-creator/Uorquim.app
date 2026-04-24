import streamlit as st
import gspread
import requests
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Uorquin - Candidatos", layout="wide")

# =========================
# CSS
# =========================
st.markdown("""
<style>
.main { background: #f5f7fb; }
.block-container { padding-top: 1.5rem; max-width: 1100px; }

.title { font-size: 40px; font-weight: 800; color:#1f2c4c; text-align:center;}
.subtitle { text-align:center; color:#6b7280; }

.card {
  background: white;
  padding: 28px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}

.sidecard {
  background: #f9fafb;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
}

.stButton>button {
  width: 100%;
  border-radius: 10px;
  height: 45px;
  font-weight: 600;
  background: #1f2c4c;
  color: white;
}

.stButton>button:hover { background:#111827; }
</style>
""", unsafe_allow_html=True)

# =========================
# LISTAS
# =========================
estados = ["BA","SP","RJ","MG","RS","SC","PR"]

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

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def formatar_telefone(tel):
    tel = re.sub(r'\D', '', tel)
    if len(tel) >= 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:11]}"
    return tel

# =========================
# GOOGLE
# =========================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        st.secrets["gcp_service_account"], scope
    )

    client = gspread.authorize(creds)
    return client.open("Banco_Uorquin").sheet1

def salvar_dados(dados):
    planilha = conectar_planilha()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    p = dados["pessoais"]

    linha = [
        data_hora,
        p["nome"], p["email"], p["telefone"],
        p["cidade"], p["estado"], p["area"]
    ]

    planilha.append_row(linha)

# =========================
# PDF PROFISSIONAL
# =========================
def gerar_pdf(dados):
    file_name = "curriculo.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    largura, altura = A4

    p = dados["pessoais"]

    # Header
    c.setFillColorRGB(0.1, 0.2, 0.4)
    c.rect(0, altura-100, largura, 100, fill=1)

    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, altura-50, p["nome"])

    c.setFont("Helvetica", 12)
    c.drawString(50, altura-70, p["area"])

    y = altura - 130
    c.setFillColorRGB(0,0,0)

    # Contato
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Contato")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Email: {p['email']}")
    y -= 15
    c.drawString(50, y, f"Telefone: {p['telefone']}")
    y -= 15
    c.drawString(50, y, f"{p['cidade']} - {p['estado']}")

    # Objetivo
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Objetivo")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(50, y, dados.get("objetivo",""))

    c.save()
    return file_name

# =========================
# CONTROLE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1

if "dados" not in st.session_state:
    st.session_state.dados = {}

# =========================
# HEADER
# =========================
st.image("logo.png", width=140)
st.markdown('<div class="title">Crie seu currículo</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Rápido e profissional</div>', unsafe_allow_html=True)

left, right = st.columns([2,1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # =========================
    # ETAPA 1
    # =========================
    if st.session_state.step == 1:

        nome = st.text_input("Nome")
        email = st.text_input("Email")
        telefone = formatar_telefone(st.text_input("Telefone"))

        estado = st.selectbox("Estado", estados)
        cidade = st.selectbox("Cidade", buscar_cidades(estado))
        area = st.text_input("Área")

        if st.button("Continuar"):
            if not validar_email(email):
                st.error("Email inválido")
            else:
                st.session_state.dados["pessoais"] = {
                    "nome": nome,
                    "email": email,
                    "telefone": telefone,
                    "cidade": cidade,
                    "estado": estado,
                    "area": area
                }
                st.session_state.step = 2
                st.rerun()

    # =========================
    # ETAPA FINAL
    # =========================
    elif st.session_state.step == 2:

        objetivo = st.text_area("Objetivo")

        col1, col2 = st.columns(2)

        if col1.button("Voltar"):
            st.session_state.step = 1
            st.rerun()

        if col2.button("Finalizar"):

            st.session_state.dados["objetivo"] = objetivo

            salvar_dados(st.session_state.dados)

            pdf = gerar_pdf(st.session_state.dados)

            st.success("Cadastro realizado!")

            with open(pdf, "rb") as f:
                st.download_button(
                    "Baixar currículo",
                    f,
                    file_name="curriculo.pdf"
                )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LATERAL
# =========================
with right:
    st.markdown('<div class="sidecard">', unsafe_allow_html=True)
    st.markdown("### Dicas")
    st.markdown("- Seja objetivo\n- Preencha tudo\n- Revise antes de enviar")
    st.markdown('</div>', unsafe_allow_html=True)
