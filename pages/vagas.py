import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# =========================
# CONTROLE DE ESTADO
# =========================
if "vaga_selecionada" not in st.session_state:
    st.session_state["vaga_selecionada"] = -1

if "vaga" not in st.session_state:
    st.session_state["vaga"] = None

st.set_page_config(page_title="Portal de Vagas", layout="wide")

# =========================
# HEADER
# =========================
st.image("logo.png", width=180)
st.markdown("<h2 style='text-align:center'>🚀 Portal de Vagas</h2>", unsafe_allow_html=True)

# =========================
# CONEXÃO
# =========================
def conectar_planilha():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scope
)
    client = gspread.authorize(creds)
    return client.open("Banco_Uorquin")

@st.cache_data(ttl=60)
def carregar_vagas():
    planilha = conectar_planilha().worksheet("Sheet2")
    dados = planilha.get_all_records()
    df = pd.DataFrame(dados)
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df

def safe(v):
    if pd.isna(v):
        return ""
    return str(v)

# =========================
# BUSCAR CANDIDATO
# =========================
def buscar_candidato_por_cpf(cpf):

    planilha = conectar_planilha().worksheet("sheet1")
    dados = planilha.get_all_records()

    cpf = cpf.replace(".", "").replace("-", "")

    for d in dados:
        cpf_base = str(d.get("CPF", "")).replace(".", "").replace("-", "")

        if cpf == cpf_base:
            return {
                "nome": d.get("Nome"),
                "cpf": d.get("CPF"),
                "email": d.get("Email"),
                "telefone": d.get("Telefone"),
                "cidade": d.get("Cidade"),
                "estado": d.get("Estado"),
                "area": d.get("Área")
            }

    return None

# =========================
# SALVAR CANDIDATURA
# =========================
def salvar_candidatura(vaga, candidato):

    client = conectar_planilha()

    try:
        planilha = client.worksheet("Candidaturas")
    except:
        planilha = client.add_worksheet(title="Candidaturas", rows="1000", cols="20")
        planilha.append_row([
            "Data",
            "Codigo_Vaga",
            "Nome",
            "CPF",
            "Email",
            "Telefone",
            "Cidade",
            "Estado",
            "Area",
            "Status"
        ])

    registros = planilha.get_all_records()

    for r in registros:
        if str(r["CPF"]) == str(candidato["cpf"]) and str(r["Codigo_Vaga"]) == str(vaga["Codigo_Vaga"]):
            return "duplicado"

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    planilha.append_row([
        data,
        vaga["Codigo_Vaga"],
        candidato["nome"],
        candidato["cpf"],
        candidato["email"],
        candidato["telefone"],
        candidato["cidade"],
        candidato["estado"],
        candidato["area"],
        "Novo"
    ])

    return "ok"

# =========================
# CSS UX PREMIUM
# =========================
st.markdown("""
<style>
.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    transition: all 0.25s ease;
    border: 1px solid #eee;
}

.card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.12);
}

.card-selecionado {
    background: #e6f0ff;
    border: 2px solid #1f77ff;
    transform: scale(1.03);
    box-shadow: 0px 12px 30px rgba(31,119,255,0.25);
}

.titulo {
    font-size:18px;
    font-weight:bold;
}

.empresa {
    font-weight:600;
}

.local {
    color:gray;
    font-size:13px;
}

.codigo {
    font-size:12px;
    color:gray;
    margin-top:8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# CARREGAR DADOS
# =========================
df = carregar_vagas()

if df.empty:
    st.warning("Sem vagas cadastradas")
    st.stop()

# =========================
# FILTROS
# =========================
c1, c2 = st.columns(2)

with c1:
    cidades = sorted(df["Cidade"].dropna().unique())
    cidade = st.selectbox("Cidade", ["Todas"] + list(cidades))

with c2:
    funcoes = sorted(df["Titulo_Vaga"].dropna().unique())
    funcao = st.selectbox("Função", ["Todas"] + list(funcoes))

df_filtro = df.copy()

if cidade != "Todas":
    df_filtro = df_filtro[df_filtro["Cidade"] == cidade]

if funcao != "Todas":
    df_filtro = df_filtro[df_filtro["Titulo_Vaga"] == funcao]

# =========================
# CARDS
# =========================
cols = st.columns(3)

for i, (_, v) in enumerate(df_filtro.iterrows()):

    card_selecionado = st.session_state["vaga_selecionada"] == i
    classe = "card card-selecionado" if card_selecionado else "card"

    codigo_vaga = safe(v.get("Codigo_Vaga"))

    with cols[i % 3]:

        st.markdown(f"""
        <div class="{classe}">
            <div class="titulo">🚀 {safe(v.get("Titulo_Vaga"))}</div>
            <div class="empresa">{safe(v.get("Empresa"))}</div>
            <div class="local">{safe(v.get("Cidade"))} - {safe(v.get("Estado"))}</div>
            <div class="codigo">Código: {codigo_vaga}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("👁 Ver detalhes", key=f"det_{i}", use_container_width=True):
            st.session_state["vaga"] = v.to_dict()
            st.session_state["vaga_selecionada"] = i
            st.rerun()

# =========================
# DETALHE DA VAGA + SCROLL
# =========================
if st.session_state["vaga"] is not None:

    # 🔥 SCROLL AUTOMÁTICO
    st.markdown("<div id='detalhe_vaga'></div>", unsafe_allow_html=True)
    st.markdown("""
    <script>
    window.location.hash = 'detalhe_vaga';
    </script>
    """, unsafe_allow_html=True)

    v = st.session_state["vaga"]

    st.divider()
    st.subheader("📄 Detalhes da vaga")

    st.write("**Empresa:**", safe(v.get("Empresa")))
    st.write("**Local:**", safe(v.get("Cidade")), "-", safe(v.get("Estado")))
    st.write("**Salário:**", safe(v.get("Salario")))

    st.write("### 📝 Descrição")
    st.write(safe(v.get("Descricao")))

    beneficios = []
    for i in range(1, 10):
        b = safe(v.get(f"Beneficio_{i}"))
        if b:
            beneficios.append(b)

    if beneficios:
        st.write("### 🎁 Benefícios")
        for b in beneficios:
            st.write("-", b)

    requisitos = []
    for i in range(1, 10):
        r = safe(v.get(f"Requisito_{i}"))
        if r:
            requisitos.append(r)

    if requisitos:
        st.write("### 📌 Pré-requisitos")
        for r in requisitos:
            st.write("-", r)

    st.write("")

    cpf_input = st.text_input("Digite seu CPF para se candidatar")

    if st.button("🚀 Candidatar-se"):

        if not cpf_input:
            st.warning("Digite seu CPF")
        else:
            candidato = buscar_candidato_por_cpf(cpf_input)

            if candidato is None:
                st.error("CPF não encontrado. Cadastre seu currículo primeiro.")
            else:
                status = salvar_candidatura(v, candidato)

                if status == "duplicado":
                    st.warning("Você já se candidatou a essa vaga")
                else:
                    st.success("Candidatura realizada com sucesso!")
