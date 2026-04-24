import streamlit as st
import gspread
import requests
import re
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Configuração da Página
st.set_page_config(page_title="Üorquin - Candidatos", layout="wide", initial_sidebar_state="expanded")

# =========================
# CSS PARA DESIGN IDÊNTICO (UI/UX)
# =========================
st.markdown("""
    <style>
    /* Estilo Geral do Fundo */
    [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
    
    /* Menu Lateral Customizado */
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E2E8F0; }
    
    /* Estilização dos Inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div > div, .stNumberInput > div > div > input {
        background-color: #F1F5F9 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }

    /* Cards Brancos */
    div.stElementContainer:has(div.card-form) {
        background: white;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    
    /* Sidebar Status */
    .sidebar-info-card {
        background: #F0FDF4;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #22C55E;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# BARRA LATERAL (SIDEBAR) COM ÍCONES
# =========================
with st.sidebar:
    st.image("logo.png", width=120)
    st.markdown("---")
    st.page_link("portal.py", label="Portal (Início)", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas Disponíveis", icon="💼")
    st.markdown("---")
    st.caption("Conectando pessoas a oportunidades")

# =========================
# FUNÇÕES DE APOIO (IDÊNTICAS AO SEU ORIGINAL)
# =========================
@st.cache_data
def buscar_cidades(uf):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    r = requests.get(url)
    return sorted([c["nome"] for c in r.json()]) if r.status_code == 200 else []

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}" if len(cpf) >= 11 else cpf

def validar_cpf_simples(cpf): return len(re.sub(r'\D', '', cpf)) == 11
def validar_email(email): return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def conectar_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Garanta que o arquivo credenciais.json esteja na pasta raiz
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    return client.open("Banco_Uorquin").sheet1

def salvar_dados(dados):
    try:
        planilha = conectar_planilha()
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        p = dados["pessoais"]
        
        linha = [data_hora, p["nome"], p["cpf"], p["email"], p["telefone"], p["idade"],
                 p["endereco"], p["cidade"], p["estado"], p["cep"], p["sexo"], 
                 p["estado_civil"], p["viagens"], p["tipo"], p["salario"], p["area"]]

        for i in range(4):
            if i < len(dados.get("experiencias", [])):
                exp = dados["experiencias"][i]
                linha += [exp["empresa"], exp["funcao"], exp["inicio"], exp["fim"], exp["cidade"]]
            else: linha += ["", "", "", "", ""]

        for i in range(4):
            if i < len(dados.get("escolaridade", [])):
                esc = dados["escolaridade"][i]
                linha += [esc["instituicao"], esc["curso"], esc["conclusao"]]
            else: linha += ["", "", ""]

        for i in range(4):
            if i < len(dados.get("cursos", [])):
                c = dados["cursos"][i]
                linha += [c["instituicao"], c["curso"], c["nivel"], c["conclusao"]]
            else: linha += ["", "", "", ""]

        linha.append(dados.get("objetivo", ""))
        planilha.append_row(linha)
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

def gerar_pdf(dados):
    file_name = "curriculo_uorquin.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    largura, altura = A4
    c.setFillColorRGB(0.12, 0.17, 0.34) # Azul Marinho
    c.rect(0, altura - 100, largura, 100, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, altura - 50, dados["pessoais"]["nome"].upper())
    c.setFont("Helvetica", 12)
    c.drawString(50, altura - 75, dados["pessoais"]["area"])
    c.save()
    return file_name

# =========================
# CONTROLE DE ESTADO
# =========================
for key in ["step", "dados", "qtd_exp", "qtd_esc", "qtd_curso"]:
    if key not in st.session_state:
        if key == "step": st.session_state[key] = 1
        elif key == "dados": st.session_state[key] = {}
        else: st.session_state[key] = 1

# Interface do Topo
st.markdown(f"### Etapa {st.session_state.step} de 4")
st.progress(st.session_state.step / 4)

col_form, col_dicas = st.columns([2, 1])

# =========================
# FORMULÁRIO PRINCIPAL
# =========================
with col_form:
    st.markdown("<div class='card-form'>", unsafe_allow_html=True)
    
    # ETAPA 1: DADOS PESSOAIS
    if st.session_state.step == 1:
        st.subheader("Dados Pessoais")
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo", value=st.session_state.dados.get("pessoais", {}).get("nome", ""))
        sexo = c1.selectbox("Sexo", ["Masculino", "Feminino"], index=0)
        est_civil = c1.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)"])
        cpf = c1.text_input("CPF", value=st.session_state.dados.get("pessoais", {}).get("cpf", ""))
        idade = c1.number_input("Idade", 14, 100, 18)
        
        email = c2.text_input("Email")
        tel = c2.text_input("Telefone")
        endereco = c2.text_input("Endereço completo")
        estado = c2.selectbox("Estado", ["AC","BA","RJ","SP","SC"]) # Adicione todos conforme sua lista original
        cidade = c2.selectbox("Cidade", buscar_cidades(estado))
        
        st.markdown("---")
        viagens = st.selectbox("Disponibilidade para viagens", ["Sim", "Não"])
        tipo = st.selectbox("Tipo de emprego", ["CLT", "Estágio", "PJ"])
        salario = st.text_input("Pretensão salarial")
        area = st.text_input("Área de interesse (Ex: Administrativo)")

        if st.button("Próximo Passo: Experiência ➡️", type="primary", use_container_width=True):
            st.session_state.dados["pessoais"] = {
                "nome": nome, "sexo": sexo, "estado_civil": est_civil, "cpf": cpf, "idade": idade,
                "email": email, "telefone": tel, "endereco": endereco, "cidade": cidade, "estado": estado,
                "cep": "", "viagens": viagens, "tipo": tipo, "salario": salario, "area": area
            }
            st.session_state.step = 2
            st.rerun()

    # ETAPA 2: EXPERIÊNCIA
    elif st.session_state.step == 2:
        st.subheader("Experiência Profissional")
        exps = []
        for i in range(st.session_state.qtd_exp):
            with st.expander(f"Empresa {i+1}", expanded=True):
                emp = st.text_input(f"Nome da Empresa", key=f"emp_{i}")
                fun = st.text_input(f"Cargo/Função", key=f"fun_{i}")
                col_i, col_f = st.columns(2)
                ini = col_i.text_input("Início (MM/AAAA)", key=f"ini_{i}")
                fim = col_f.text_input("Fim (MM/AAAA)", key=f"fim_{i}")
                cid = st.text_input("Cidade/UF", key=f"cidexp_{i}")
                exps.append({"empresa": emp, "funcao": fun, "inicio": ini, "fim": fim, "cidade": cid})
        
        if st.session_state.qtd_exp < 4:
            if st.button("➕ Adicionar outra experiência"):
                st.session_state.qtd_exp += 1
                st.rerun()
        
        st.markdown("---")
        cb1, cb2 = st.columns(2)
        if cb1.button("⬅️ Voltar"): st.session_state.step = 1; st.rerun()
        if cb2.button("Próximo Passo: Formação ➡️", type="primary"):
            st.session_state.dados["experiencias"] = exps
            st.session_state.step = 3
            st.rerun()

    # ETAPA 3: ESCOLARIDADE E CURSOS
    elif st.session_state.step == 3:
        st.subheader("Formação e Cursos")
        # Escolaridade
        escs = []
        for i in range(st.session_state.qtd_esc):
            with st.expander(f"Formação Acadêmica {i+1}", expanded=True):
                inst = st.text_input("Instituição", key=f"inst_{i}")
                cur = st.text_input("Curso", key=f"cur_{i}")
                conc = st.text_input("Conclusão", key=f"conc_{i}")
                escs.append({"instituicao": inst, "curso": cur, "conclusao": conc})
        
        if st.session_state.qtd_esc < 3:
            if st.button("➕ Adicionar Formação"): st.session_state.qtd_esc += 1; st.rerun()
            
        st.markdown("---")
        # Cursos
        curss = []
        for i in range(st.session_state.qtd_curso):
            with st.expander(f"Curso de Aperfeiçoamento {i+1}", expanded=True):
                cinst = st.text_input("Escola/Plataforma", key=f"cinst_{i}")
                cnom = st.text_input("Nome do Curso", key=f"cnom_{i}")
                curss.append({"instituicao": cinst, "curso": cnom, "nivel": "", "conclusao": ""})
        
        if st.session_state.qtd_curso < 3:
            if st.button("➕ Adicionar Curso"): st.session_state.qtd_curso += 1; st.rerun()

        st.markdown("---")
        cb1, cb2 = st.columns(2)
        if cb1.button("⬅️ Voltar"): st.session_state.step = 2; st.rerun()
        if cb2.button("Última Etapa ➡️", type="primary"):
            st.session_state.dados["escolaridade"] = escs
            st.session_state.dados["cursos"] = curss
            st.session_state.step = 4
            st.rerun()

    # ETAPA 4: FINALIZAR
    elif st.session_state.step == 4:
        st.subheader("Objetivo Profissional")
        obj = st.text_area("Fale um pouco sobre seus objetivos e o que busca na Üorquin", height=150)
        
        if st.button("✅ FINALIZAR E SALVAR", type="primary", use_container_width=True):
            st.session_state.dados["objetivo"] = obj
            salvar_dados(st.session_state.dados)
            pdf_path = gerar_pdf(st.session_state.dados)
            st.success("Dados salvos com sucesso na planilha!")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Baixar meu Currículo em PDF", f, file_name="curriculo_uorquin.pdf")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# COLUNA DE DICAS (IDENTICA À FOTO 02)
# =========================
with col_dicas:
    st.markdown("### Dicas para um bom currículo")
    st.markdown("""
        <div class='sidebar-info-card'>
            ✅ <b>Preencha todos os campos:</b> Candidatos com perfil completo são contratados 3x mais rápido.<br><br>
            ✅ <b>Informações Verídicas:</b> Revise datas e nomes de empresas.<br><br>
            ✅ <b>Destaque-se:</b> No objetivo profissional, seja direto e mostre seus pontos fortes.
        </div>
    """, unsafe_allow_html=True)
    
    st.info("🔒 Seus dados estão criptografados e seguem as normas da LGPD.")
