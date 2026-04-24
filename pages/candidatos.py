import streamlit as st
import gspread
import requests
import re
import os
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Üorquin - Candidatos", layout="wide", initial_sidebar_state="expanded")

# 2. UI/UX - CSS PARA FICAR IGUAL ÀS FOTOS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E2E8F0; }
    
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: #F1F5F9 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
    }
    .card-uorquin {
        background: white;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .step-text { color: #3B82F6; font-weight: 700; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR COM ÍCONES (IGUAL AO MODELO)
with st.sidebar:
    st.image("logo.png", width=130)
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    st.markdown("---")
    st.caption("Conectando pessoas a oportunidades")

# 4. FUNÇÕES TÉCNICAS (GOOGLE SHEETS E PDF)
def conectar_planilha():
    if not os.path.exists("credenciais.json"):
        st.error("ERRO: O arquivo 'credenciais.json' não foi encontrado no seu GitHub!")
        return None
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    return client.open("Banco_Uorquin").sheet1

def salvar_dados_completos(dados):
    planilha = conectar_planilha()
    if not planilha: return False
    try:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        p = dados["pessoais"]
        linha = [data_hora, p["nome"], p["cpf"], p["email"], p["telefone"], p["idade"],
                 p["endereco"], p["cidade"], p["estado"], p["cep"], p["sexo"], 
                 p["estado_civil"], p["viagens"], p["tipo"], p["salario"], p["area"]]
        
        # Garante 4 campos de Exp, 4 de Escolaridade e 4 de Cursos (conforme sua planilha)
        for i in range(4):
            if i < len(dados.get("experiencias", [])):
                e = dados["experiencias"][i]
                linha += [e["empresa"], e["funcao"], e["inicio"], e["fim"], e["cidade"]]
            else: linha += [""]*5
        for i in range(4):
            if i < len(dados.get("escolaridade", [])):
                es = dados["escolaridade"][i]
                linha += [es["instituicao"], es["curso"], es["conclusao"]]
            else: linha += [""]*3
        for i in range(4):
            if i < len(dados.get("cursos", [])):
                c = dados["cursos"][i]
                linha += [c["instituicao"], c["curso"], c["nivel"], c["conclusao"]]
            else: linha += [""]*4
        linha.append(dados.get("objetivo", ""))
        planilha.append_row(linha)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

def gerar_pdf(dados):
    nome_pdf = f"Curriculo_{dados['pessoais']['nome'].replace(' ', '_')}.pdf"
    c = canvas.Canvas(nome_pdf, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"CURRÍCULO: {dados['pessoais']['nome'].upper()}")
    c.setFont("Helvetica", 12)
    c.drawString(50, 780, f"Área: {dados['pessoais']['area']}")
    c.drawString(50, 760, f"Contato: {dados['pessoais']['email']} | {dados['pessoais']['telefone']}")
    c.save()
    return nome_pdf

# 5. ESTADO DA SESSÃO (SESSION STATE)
if "step" not in st.session_state: st.session_state.step = 1
if "dados" not in st.session_state: st.session_state.dados = {}
if "qtd_exp" not in st.session_state: st.session_state.qtd_exp = 1
if "qtd_esc" not in st.session_state: st.session_state.qtd_esc = 1
if "qtd_curso" not in st.session_state: st.session_state.qtd_curso = 1

# 6. INTERFACE DE PASSOS
st.markdown(f"<p class='step-text'>Etapa {st.session_state.step} de 4</p>", unsafe_allow_html=True)
st.progress(st.session_state.step / 4)

col_form, col_dicas = st.columns([2.5, 1])

with col_form:
    st.markdown("<div class='card-uorquin'>", unsafe_allow_html=True)
    
    # PASSO 1: DADOS PESSOAIS
    if st.session_state.step == 1:
        st.subheader("Crie seu currículo profissional em poucos minutos")
        c1, c2 = st.columns(2)
        nome = c1.text_input("Nome Completo", placeholder="Digite seu nome completo")
        email = c1.text_input("E-mail", placeholder="exemplo@email.com")
        sexo = c1.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        cpf = c1.text_input("CPF", placeholder="000.000.000-00")
        
        tel = c2.text_input("Telefone", placeholder="(00) 00000-0000")
        idade = c2.number_input("Idade", 14, 99, 20)
        est_civil = c2.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)"])
        end = c2.text_input("Endereço Completo")
        
        st.markdown("---")
        c3, c4 = st.columns(2)
        uf = c3.selectbox("Estado", ["BA", "SP", "RJ", "MG", "SC"]) # Simplificado
        cid = c3.text_input("Cidade")
        cep = c3.text_input("CEP")
        viagens = c4.selectbox("Disponibilidade para viagens", ["Sim", "Não"])
        tipo = c4.selectbox("Tipo de Emprego", ["CLT", "Estágio", "PJ", "Jovem Aprendiz"])
        salario = c4.text_input("Pretensão Salarial (R$)")
        area = c4.text_input("Área de Interesse")

        if st.button("Continuar para Experiências ➡️", type="primary", use_container_width=True):
            st.session_state.dados["pessoais"] = {
                "nome": nome, "email": email, "sexo": sexo, "cpf": cpf, "telefone": tel,
                "idade": idade, "estado_civil": est_civil, "endereco": end, "estado": uf,
                "cidade": cid, "cep": cep, "viagens": viagens, "tipo": tipo, "salario": salario, "area": area
            }
            st.session_state.step = 2
            st.rerun()

    # PASSO 2: EXPERIÊNCIAS (DINÂMICO)
    elif st.session_state.step == 2:
        st.subheader("Experiência Profissional")
        exps = []
        for i in range(st.session_state.qtd_exp):
            with st.container(border=True):
                st.markdown(f"**Empresa {i+1}**")
                emp = st.text_input("Nome da Empresa", key=f"emp_{i}")
                fun = st.text_input("Função/Cargo", key=f"fun_{i}")
                col_i, col_f = st.columns(2)
                ini = col_i.text_input("Início (MM/AAAA)", key=f"ini_{i}")
                fim = col_f.text_input("Fim (MM/AAAA)", key=f"fim_{i}")
                cid_e = st.text_input("Cidade/UF", key=f"cid_e_{i}")
                exps.append({"empresa": emp, "funcao": fun, "inicio": ini, "fim": fim, "cidade": cid_e})
        
        if st.session_state.qtd_exp < 4:
            if st.button("➕ Adicionar outra experiência"):
                st.session_state.qtd_exp += 1
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("⬅️ Voltar"): st.session_state.step = 1; st.rerun()
        if col_b2.button("Continuar para Formação ➡️", type="primary"):
            st.session_state.dados["experiencias"] = exps
            st.session_state.step = 3
            st.rerun()

    # PASSO 3: FORMAÇÃO E CURSOS
    elif st.session_state.step == 3:
        st.subheader("Formação Acadêmica e Cursos")
        escs = []
        for i in range(st.session_state.qtd_esc):
            with st.expander(f"Formação {i+1}", expanded=True):
                inst = st.text_input("Instituição", key=f"inst_{i}")
                cur = st.text_input("Curso", key=f"cur_{i}")
                con = st.text_input("Conclusão", key=f"con_{i}")
                escs.append({"instituicao": inst, "curso": cur, "conclusao": con})
        if st.button("➕ Adicionar Formação"): st.session_state.qtd_esc += 1; st.rerun()
        
        st.markdown("---")
        curss = []
        for i in range(st.session_state.qtd_curso):
            with st.expander(f"Curso de Aperfeiçoamento {i+1}", expanded=True):
                c_inst = st.text_input("Escola", key=f"cinst_{i}")
                c_nom = st.text_input("Nome do Curso", key=f"cnom_{i}")
                curss.append({"instituicao": c_inst, "curso": c_nom, "nivel": "N/A", "conclusao": "N/A"})
        if st.button("➕ Adicionar Curso"): st.session_state.qtd_curso += 1; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("⬅️ Voltar"): st.session_state.step = 2; st.rerun()
        if col_b2.button("Ir para Finalização ➡️", type="primary"):
            st.session_state.dados["escolaridade"] = escs
            st.session_state.dados["cursos"] = curss
            st.session_state.step = 4
            st.rerun()

    # PASSO 4: FINALIZAR
    elif st.session_state.step == 4:
        st.subheader("Objetivo Profissional")
        obj = st.text_area("Fale sobre seus objetivos e o que busca na Üorquin", height=150)
        
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("⬅️ Voltar"): st.session_state.step = 3; st.rerun()
        if col_b2.button("✅ FINALIZAR E SALVAR", type="primary", use_container_width=True):
            st.session_state.dados["objetivo"] = obj
            if salvar_dados_completos(st.session_state.dados):
                st.success("Dados salvos com sucesso!")
                pdf_path = gerar_pdf(st.session_state.dados)
                with open(pdf_path, "rb") as f:
                    st.download_button("📥 Baixar meu Currículo (PDF)", f, file_name=pdf_path)
            else:
                st.error("Verifique se o arquivo 'credenciais.json' está no GitHub.")

    st.markdown("</div>", unsafe_allow_html=True)

with col_dicas:
    st.markdown("### Dicas para um bom currículo")
    st.markdown("""
        <div style='background:#F0FDF4; padding:15px; border-radius:10px; border-left:4px solid #22C55E;'>
            ✅ <b>Preencha todos os campos</b><br><br>
            ✅ <b>Use informações verdadeiras</b><br><br>
            ✅ <b>Destaque suas experiências</b><br><br>
            ✅ <b>Mantenha seu perfil atualizado</b>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("🔒 Seus dados estão seguros e não serão compartilhados com terceiros.")
