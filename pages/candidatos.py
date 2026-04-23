import streamlit as st
import gspread
import requests
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Uorquin", layout="centered")
st.logo("logo.png")
st.sidebar.markdown("## 🚀 Uorquin")
st.sidebar.markdown("---")

st.image("logo.png", width=220)
st.markdown("<h3 style='text-align:center'>Crie seu currículo profissional em poucos minutos</h3>", unsafe_allow_html=True)

# =========================
# LISTAS
# =========================
estados = ["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
"MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]

# =========================
# IBGE
# =========================
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

    # 👉 cria cabeçalho automático (só uma vez)
    if not planilha.row_values(1):

        cabecalho = [
            "Data_Cadastro",
            "Nome","CPF","Email","Telefone","Idade",
            "Endereço","Cidade","Estado","CEP",
            "Sexo","Estado Civil","Disponibilidade",
            "Tipo Emprego","Salário","Área"
        ]

        for i in range(1,5):
            cabecalho += [
                f"Empresa_{i}", f"Funcao_{i}",
                f"Inicio_{i}", f"Fim_{i}", f"Cidade_{i}"
            ]

        for i in range(1,5):
            cabecalho += [
                f"Instituicao_{i}", f"Curso_{i}", f"Conclusao_{i}"
            ]

        for i in range(1,5):
            cabecalho += [
                f"CursoInst_{i}", f"CursoNome_{i}",
                f"Nivel_{i}", f"CursoConclusao_{i}"
            ]

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
# PDF
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

st.progress(st.session_state.step / 5)

# =========================
# ETAPA 1
# =========================
if st.session_state.step == 1:

    st.subheader("Dados Pessoais")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome Completo")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
        estado_civil = st.selectbox("Estado Civil", ["Solteiro", "Casado", "Divorciado"])
        cpf = formatar_cpf(st.text_input("CPF"))
        idade = st.number_input("Idade", 0, 100)
        telefone = formatar_telefone(st.text_input("Telefone"))
        email = st.text_input("Email")

    with col2:
        endereco = st.text_input("Endereço completo")
        estado = st.selectbox("Estado", estados)
        cidade = st.selectbox("Cidade", buscar_cidades(estado))
        cep = formatar_cep(st.text_input("CEP"))
        viagens = st.selectbox("Disponibilidade para viagens", ["Sim", "Não"])
        tipo = st.selectbox("Tipo de emprego", ["CLT", "Estágio", "Jovem Aprendiz", "PJ"])
        salario = st.text_input("Pretensão salarial")
        area = st.text_input("Área de interesse")

    if st.button("Continuar ➡️"):

        if not validar_cpf_simples(cpf):
            st.error("CPF inválido")
        elif not validar_email(email):
            st.error("Email inválido")
        else:
            st.session_state.dados["pessoais"] = {
                "nome": nome,
                "sexo": sexo,
                "estado_civil": estado_civil,
                "cpf": cpf,
                "idade": idade,
                "telefone": telefone,
                "email": email,
                "endereco": endereco,
                "cidade": cidade,
                "estado": estado,
                "cep": cep,
                "viagens": viagens,
                "tipo": tipo,
                "salario": salario,
                "area": area
            }

            st.session_state.step = 2
            st.rerun()

# =========================
# ETAPA 2
# =========================
elif st.session_state.step == 2:

    st.subheader("Experiência Profissional")

    experiencias = []

    for i in range(st.session_state.qtd_exp):
        with st.expander(f"Experiência {i+1}", expanded=(i==0)):
            empresa = st.text_input("Empresa", key=f"empresa_{i}")
            funcao = st.text_input("Função", key=f"funcao_{i}")
            inicio = st.text_input("Início (MM/AAAA)", key=f"inicio_{i}")
            fim = st.text_input("Fim (MM/AAAA)", key=f"fim_{i}")
            cidade_exp = st.selectbox("Cidade", buscar_cidades(st.session_state.dados["pessoais"]["estado"]), key=f"cidade_exp_{i}")

            experiencias.append({
                "empresa": empresa,
                "funcao": funcao,
                "inicio": inicio,
                "fim": fim,
                "cidade": cidade_exp
            })

    if st.session_state.qtd_exp < 4:
        if st.button("➕ Adicionar experiência"):
            st.session_state.qtd_exp += 1
            st.rerun()

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 1
        st.rerun()

    if col2.button("Continuar ➡️"):
        st.session_state.dados["experiencias"] = experiencias

        st.session_state.step = 3
        st.rerun()

# =========================
# ETAPA 3
# =========================
elif st.session_state.step == 3:

    st.subheader("Escolaridade")

    escolaridade = []

    for i in range(st.session_state.qtd_esc):
        with st.expander(f"Formação {i+1}", expanded=(i==0)):
            instituicao = st.text_input("Instituição", key=f"inst_{i}")
            curso = st.text_input("Curso", key=f"curso_{i}")
            conclusao = st.text_input("Conclusão (MM/AAAA)", key=f"conc_{i}")

            escolaridade.append({
                "instituicao": instituicao,
                "curso": curso,
                "conclusao": conclusao
            })

    if st.session_state.qtd_esc < 4:
        if st.button("➕ Adicionar formação"):
            st.session_state.qtd_esc += 1
            st.rerun()

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 2
        st.rerun()

    if col2.button("Continuar ➡️"):
        st.session_state.dados["escolaridade"] = escolaridade

        st.session_state.step = 4
        st.rerun()

# =========================
# ETAPA 4
# =========================
elif st.session_state.step == 4:

    st.subheader("Cursos de Aperfeiçoamento")

    cursos = []

    for i in range(st.session_state.qtd_curso):
        with st.expander(f"Curso {i+1}", expanded=(i==0)):
            instituicao = st.text_input("Instituição", key=f"cinst_{i}")
            curso = st.text_input("Curso", key=f"ccurso_{i}")
            nivel = st.text_input("Nível", key=f"cnivel_{i}")
            conclusao = st.text_input("Conclusão (MM/AAAA)", key=f"cconc_{i}")

            cursos.append({
                "instituicao": instituicao,
                "curso": curso,
                "nivel": nivel,
                "conclusao": conclusao
            })

    if st.session_state.qtd_curso < 4:
        if st.button("➕ Adicionar curso"):
            st.session_state.qtd_curso += 1
            st.rerun()

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 3
        st.rerun()

    if col2.button("Continuar ➡️"):
        st.session_state.dados["cursos"] = cursos

        st.session_state.step = 5
        st.rerun()

# =========================
# FINAL
# =========================
elif st.session_state.step == 5:

    objetivo = st.text_area("Objetivo profissional")

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 4
        st.rerun()

    if col2.button("Finalizar"):
        st.session_state.dados["objetivo"] = objetivo

        salvar_dados(st.session_state.dados)
        pdf = gerar_pdf(st.session_state.dados)

        st.success("Cadastro realizado com sucesso!")

        with open(pdf, "rb") as f:
            st.download_button("📄 Baixar currículo", f)

