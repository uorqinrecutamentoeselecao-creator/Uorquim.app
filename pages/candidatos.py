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
st.set_page_config(page_title="Uorquin - Candidatos", layout="wide")

# =========================
# CSS (limite do Streamlit)
# =========================
st.markdown("""
<style>
.main { background: #f5f7fb; }
.block-container { padding-top: 1.5rem; max-width: 1100px; }

.header { text-align:center; margin-bottom: 10px; }
.title { font-size: 40px; font-weight: 800; color:#1f2c4c; }
.subtitle { color:#6b7280; }

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
  border-radius: 12px;
  height: 48px;
  font-weight: 600;
  background: #2563eb;
  color: white;
}

.stButton>button:hover { background:#1d4ed8; }

.stepper {
  display:flex; gap:10px; margin: 10px 0 20px 0;
}
.step {
  flex:1; text-align:center;
}
.circle {
  width:30px; height:30px; border-radius:50%;
  margin:auto; line-height:30px; font-size:14px;
  background:#d1d5db; color:white;
}
.active { background:#2563eb; }

small { color:#6b7280; }
</style>
""", unsafe_allow_html=True)

# =========================
# LISTAS
# =========================
estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
"MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]

# =========================
# IBGE (mantido)
# =========================
@st.cache_data
def buscar_cidades(uf):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    r = requests.get(url)
    if r.status_code == 200:
        return sorted([c["nome"] for c in r.json()])
    return []

# =========================
# FORMATADORES (mantido)
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
# GOOGLE (mantido)
# =========================
def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scope
)
    client = gspread.authorize(creds)
    return client.open("Banco_Uorquin").sheet1

def salvar_dados(dados):
    planilha = conectar_planilha()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    if not planilha.row_values(1):
        cabecalho = [
            "Data_Cadastro",
            "Nome","CPF","Email","Telefone","Idade",
            "Endereço","Cidade","Estado","CEP",
            "Sexo","Estado Civil","Disponibilidade",
            "Tipo Emprego","Salário","Área"
        ]
        for i in range(1,5):
            cabecalho += [f"Empresa_{i}", f"Funcao_{i}", f"Inicio_{i}", f"Fim_{i}", f"Cidade_{i}"]
        for i in range(1,5):
            cabecalho += [f"Instituicao_{i}", f"Curso_{i}", f"Conclusao_{i}"]
        for i in range(1,5):
            cabecalho += [f"CursoInst_{i}", f"CursoNome_{i}", f"Nivel_{i}", f"CursoConclusao_{i}"]
        cabecalho.append("Objetivo")
        planilha.append_row(cabecalho)

    p = dados["pessoais"]
    linha = [
        data_hora,
        p["nome"], p["cpf"], p["email"], p["telefone"], p["idade"],
        p["endereco"], p["cidade"], p["estado"], p["cep"],
        p["sexo"], p["estado_civil"], p["viagens"],
        p["tipo"], p["salario"], p["area"]
    ]

    for i in range(4):
        if i < len(dados.get("experiencias", [])):
            exp = dados["experiencias"][i]
            linha += [exp["empresa"], exp["funcao"], exp["inicio"], exp["fim"], exp["cidade"]]
        else:
            linha += ["", "", "", "", ""]

    for i in range(4):
        if i < len(dados.get("escolaridade", [])):
            esc = dados["escolaridade"][i]
            linha += [esc["instituicao"], esc["curso"], esc["conclusao"]]
        else:
            linha += ["", "", ""]

    for i in range(4):
        if i < len(dados.get("cursos", [])):
            c = dados["cursos"][i]
            linha += [c["instituicao"], c["curso"], c["nivel"], c["conclusao"]]
        else:
            linha += ["", "", "", ""]

    linha.append(dados.get("objetivo", ""))
    planilha.append_row(linha)

# =========================
# PDF (mantido)
# =========================
def gerar_pdf(dados):
    file_name = "curriculo.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    largura, altura = A4

    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.rect(0, altura - 120, largura, 120, fill=1)

    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, altura - 60, dados["pessoais"]["nome"].upper())

    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 90, dados["pessoais"]["area"])

    y = altura - 150
    c.setFillColorRGB(0, 0, 0)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "INFORMAÇÕES")
    y -= 20
    c.setFont("Helvetica", 10)

    info = [
        f"{dados['pessoais']['cidade']} - {dados['pessoais']['estado']}",
        f"Telefone: {dados['pessoais']['telefone']}",
        f"Email: {dados['pessoais']['email']}",
        f"CPF: {dados['pessoais']['cpf']}",
        f"Estado Civil: {dados['pessoais']['estado_civil']}",
        f"Disponibilidade: {dados['pessoais']['viagens']}",
        f"Tipo: {dados['pessoais']['tipo']}",
        f"Pretensão: {dados['pessoais']['salario']}"
    ]
    for item in info:
        c.drawString(50, y, item)
        y -= 15

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
if "qtd_esc" not in st.session_state:
    st.session_state.qtd_esc = 1
if "qtd_curso" not in st.session_state:
    st.session_state.qtd_curso = 1

# =========================
# HEADER
# =========================
st.markdown('<div class="header">', unsafe_allow_html=True)
st.image("logo.png", width=160)
st.markdown('<div class="title">Crie seu currículo em poucos minutos</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Preencha seus dados e aumente suas chances de contratação</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEPPER
# =========================
steps = ["Dados", "Experiência", "Formação", "Cursos", "Final"]
html = '<div class="stepper">'
for i, s in enumerate(steps):
    active = "active" if i+1 <= st.session_state.step else ""
    html += f'<div class="step"><div class="circle {active}">{i+1}</div><small>{s}</small></div>'
html += '</div>'
st.markdown(html, unsafe_allow_html=True)

# =========================
# LAYOUT (FORM + DICAS)
# =========================
left, right = st.columns([2.2, 1])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    # =========================
    # ETAPA 1
    # =========================
    if st.session_state.step == 1:

        st.subheader("📌 Dados Pessoais")

        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome Completo")
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
            estado_civil = st.selectbox("Estado Civil", ["Solteiro", "Casado", "Divorciado"])
            cpf = formatar_cpf(st.text_input("CPF"))
            idade = st.number_input("Idade", 0, 100)
            telefone = formatar_telefone(st.text_input("Telefone"))
            email = st.text_input("Email")

        with c2:
            endereco = st.text_input("Endereço completo")
            estado = st.selectbox("Estado", estados)
            cidade = st.selectbox("Cidade", buscar_cidades(estado))
            cep = formatar_cep(st.text_input("CEP"))
            viagens = st.selectbox("Disponibilidade para viagens", ["Sim", "Não"])
            tipo = st.selectbox("Tipo de emprego", ["CLT", "Estágio", "Jovem Aprendiz", "PJ"])
            salario = st.text_input("Pretensão salarial")
            area = st.text_input("Área de interesse")

        st.markdown("---")
        if st.button("Continuar ➡️"):
            if not validar_cpf_simples(cpf):
                st.error("CPF inválido")
            elif not validar_email(email):
                st.error("Email inválido")
            else:
                st.session_state.dados["pessoais"] = {
                    "nome": nome,"sexo": sexo,"estado_civil": estado_civil,
                    "cpf": cpf,"idade": idade,"telefone": telefone,"email": email,
                    "endereco": endereco,"cidade": cidade,"estado": estado,"cep": cep,
                    "viagens": viagens,"tipo": tipo,"salario": salario,"area": area
                }
                st.session_state.step = 2
                st.rerun()

    # =========================
    # ETAPA 2
    # =========================
    elif st.session_state.step == 2:

        st.subheader("💼 Experiência Profissional")

        experiencias = []
        for i in range(st.session_state.qtd_exp):
            with st.expander(f"Experiência {i+1}", expanded=(i==0)):
                empresa = st.text_input("Empresa", key=f"empresa_{i}")
                funcao = st.text_input("Função", key=f"funcao_{i}")
                inicio = st.text_input("Início (MM/AAAA)", key=f"inicio_{i}")
                fim = st.text_input("Fim (MM/AAAA)", key=f"fim_{i}")
                cidade_exp = st.selectbox(
                    "Cidade",
                    buscar_cidades(st.session_state.dados["pessoais"]["estado"]),
                    key=f"cidade_exp_{i}"
                )
                experiencias.append({
                    "empresa": empresa, "funcao": funcao,
                    "inicio": inicio, "fim": fim, "cidade": cidade_exp
                })

        if st.session_state.qtd_exp < 4:
            if st.button("➕ Adicionar experiência"):
                st.session_state.qtd_exp += 1
                st.rerun()

        c1, c2 = st.columns(2)
        if c1.button("⬅️ Voltar"):
            st.session_state.step = 1; st.rerun()
        if c2.button("Continuar ➡️"):
            st.session_state.dados["experiencias"] = experiencias
            st.session_state.step = 3; st.rerun()

    # =========================
    # ETAPA 3
    # =========================
    elif st.session_state.step == 3:

        st.subheader("🎓 Escolaridade")
        escolaridade = []
        for i in range(st.session_state.qtd_esc):
            with st.expander(f"Formação {i+1}", expanded=(i==0)):
                instituicao = st.text_input("Instituição", key=f"inst_{i}")
                curso = st.text_input("Curso", key=f"curso_{i}")
                conclusao = st.text_input("Conclusão (MM/AAAA)", key=f"conc_{i}")
                escolaridade.append({
                    "instituicao": instituicao, "curso": curso, "conclusao": conclusao
                })

        if st.session_state.qtd_esc < 4:
            if st.button("➕ Adicionar formação"):
                st.session_state.qtd_esc += 1; st.rerun()

        c1, c2 = st.columns(2)
        if c1.button("⬅️ Voltar"):
            st.session_state.step = 2; st.rerun()
        if c2.button("Continuar ➡️"):
            st.session_state.dados["escolaridade"] = escolaridade
            st.session_state.step = 4; st.rerun()

    # =========================
    # ETAPA 4
    # =========================
    elif st.session_state.step == 4:

        st.subheader("📚 Cursos de Aperfeiçoamento")
        cursos = []
        for i in range(st.session_state.qtd_curso):
            with st.expander(f"Curso {i+1}", expanded=(i==0)):
                instituicao = st.text_input("Instituição", key=f"cinst_{i}")
                curso = st.text_input("Curso", key=f"ccurso_{i}")
                nivel = st.text_input("Nível", key=f"cnivel_{i}")
                conclusao = st.text_input("Conclusão (MM/AAAA)", key=f"cconc_{i}")
                cursos.append({
                    "instituicao": instituicao, "curso": curso,
                    "nivel": nivel, "conclusao": conclusao
                })

        if st.session_state.qtd_curso < 4:
            if st.button("➕ Adicionar curso"):
                st.session_state.qtd_curso += 1; st.rerun()

        c1, c2 = st.columns(2)
        if c1.button("⬅️ Voltar"):
            st.session_state.step = 3; st.rerun()
        if c2.button("Continuar ➡️"):
            st.session_state.dados["cursos"] = cursos
            st.session_state.step = 5; st.rerun()

# =========================
# ETAPA FINAL
# =========================
    elif st.session_state.step == 5:

      st.subheader("🎯 Objetivo")
       objetivo = st.text_area("Objetivo profissional")

      c1, c2 = st.columns(2)

      if c1.button("⬅️ Voltar"):
        st.session_state.step = 4
        st.rerun()

      if c2.button("Finalizar"):

        st.session_state.dados["objetivo"] = objetivo

        salvar_dados(st.session_state.dados)

        try:
            pdf = gerar_pdf(st.session_state.dados)

            st.success("Cadastro realizado com sucesso!")

            with open(pdf, "rb") as f:
                st.download_button(
                    "📄 Baixar currículo",
                    f,
                    file_name="curriculo.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

# =========================
# COLUNA DIREITA (DICAS)
# =========================
with right:
    st.markdown('<div class="sidecard">', unsafe_allow_html=True)
    st.markdown("### Dicas para um bom currículo")
    st.markdown("""
- Preencha todos os campos  
- Use informações verdadeiras  
- Destaque suas experiências  
- Mantenha seu perfil atualizado  
    """)
    st.markdown("---")
    st.success("Seus dados estão seguros")
    st.markdown('</div>', unsafe_allow_html=True)
