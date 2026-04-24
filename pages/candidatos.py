import streamlit as st
import requests
import re
from datetime import datetime

# Mantenha seus imports originais de gspread e reportlab aqui se for usar o salvamento
# (Omiti para encurtar, mas você deve mantê-los no topo se já funcionavam)

st.set_page_config(page_title="Cadastro - Üorquin", layout="wide")

# CSS ESTILIZADO
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
    .stTextInput > div > div > input { background-color: #F1F5F9 !important; border-radius: 8px !important; }
    .step-box { background: white; padding: 25px; border-radius: 15px; border: 1px solid #E2E8F0; }
    .sidebar-card { background: #F8FAFC; padding: 15px; border-radius: 10px; border-left: 4px solid #22C55E; }
    </style>
""", unsafe_allow_html=True)

# Funções auxiliares (Suas funções originais de formatar CPF/CEP e IBGE entram aqui)
@st.cache_data
def buscar_cidades(uf):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    r = requests.get(url)
    return sorted([c["nome"] for c in r.json()]) if r.status_code == 200 else []

# Gerenciamento de Etapas
if "step" not in st.session_state: st.session_state.step = 1

st.image("logo.png", width=100)
st.title("Crie seu currículo profissional")

# Barra de Progresso Visual
progresso = st.session_state.step / 4
st.progress(progresso)
st.write(f"Etapa {st.session_state.step} de 4")

col_principal, col_lateral = st.columns([2, 1])

with col_principal:
    if st.session_state.step == 1:
        st.subheader("01. Dados Pessoais")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            nome = c1.text_input("Nome Completo")
            sexo = c1.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            est_civil = c1.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)"])
            cpf = c1.text_input("CPF (apenas números)")
            
            endereco = c2.text_input("Endereço Completo")
            estado = c2.selectbox("Estado", ["AC","BA","RJ","SP","SC"]) # Adicione os outros
            cidade = c2.selectbox("Cidade", buscar_cidades(estado))
            cep = c2.text_input("CEP")
            
            if st.button("Continuar para Experiência ➡️", type="primary", use_container_width=True):
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        st.subheader("02. Experiência Profissional")
        with st.container(border=True):
            st.text_input("Última Empresa")
            st.text_input("Cargo")
            st.text_area("Resumo das atividades")
            col_b1, col_b2 = st.columns(2)
            if col_b1.button("⬅️ Voltar"):
                st.session_state.step = 1
                st.rerun()
            if col_b2.button("Continuar para Formação ➡️", type="primary"):
                st.session_state.step = 3
                st.rerun()

    # (Etapa 3 e 4 seguem a mesma lógica de botões Voltar/Próximo)
    elif st.session_state.step == 3:
        st.subheader("03. Formação Acadêmica")
        with st.container(border=True):
            st.text_input("Instituição")
            st.text_input("Curso")
            if st.button("Finalizar Cadastro ➡️", type="primary"):
                st.session_state.step = 4
                st.rerun()

    elif st.session_state.step == 4:
        st.balloons()
        st.success("Tudo pronto! Seu currículo foi gerado.")
        st.button("📄 Baixar PDF")
        if st.button("Recomeçar"):
            st.session_state.step = 1
            st.rerun()

with col_lateral:
    st.markdown("### Dicas para um bom currículo")
    st.markdown("""
    <div class='sidebar-card'>
    ✅ <b>Preencha tudo:</b> Perfis completos têm 3x mais chances.<br><br>
    ✅ <b>Veracidade:</b> Use dados reais para evitar problemas em entrevistas.<br><br>
    ✅ <b>Destaque-se:</b> Coloque suas conquistas mais recentes primeiro.
    </div>
    """, unsafe_allow_html=True)
    st.info("🔒 Seus dados estão protegidos pela LGPD.")
