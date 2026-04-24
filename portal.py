import streamlit as st

# 1. Configuração de Página (Sempre a primeira linha)
st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Cirúrgico (Mantém o layout e moderniza a imagem)
st.markdown("""
    <style>
        /* Limpeza de cabeçalho e topo */
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem !important;
            margin-top: -2rem !important;
        }

        /* AJUSTE SIDEBAR: Mantém a logo profissional, limpa e solta */
        [data-testid="stSidebar"] img {
            border-radius: 0px !important;
            box-shadow: none !important;
            border: none !important;
            background: transparent !important;
        }
        
        /* Limpa textos residuais na sidebar */
        section[data-testid="stSidebar"] .stMarkdown {
            display: none !important;
        }

        /* AJUSTE IMAGEM PRINCIPAL: Curvas orgânicas (Moderna) e margem superior (Desce) */
        .stImage img {
            /* Cria curvas orgânicas e dinâmicas nas bordas */
            border-radius: 60px 20px 80px 20px !important; 
            
            /* Adiciona uma sombra suave para dar profundidade */
            box-shadow: 20px 20px 50px rgba(0,0,0,0.08);
            
            /* AJUSTE SOLICITADO: Faz a imagem descer para alinhar com o texto */
            margin-top: 40px !important; 
        }

        /* CARDS INFERIORES: Mantém a altura fixa para alinhamento */
        .custom-card {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            border: 1px solid #F1F5F9;
            height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        /* BOTÕES INFERIORES: Unificados, brancos com hover verde */
        .stButton > button {
            background-color: white !important;
            color: #1E293B !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            height: 45px;
            transition: all 0.3s ease !important;
        }
        .stButton > button:hover {
            border-color: #22C55E !important;
            color: #22C55E !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (Restaurada e Limpa)
with st.sidebar:
    st.image("logo.png", width=160) # Ajustado para manter a qualidade da Üorquin
    st.page_link("portal.py", label="Portal (Início)", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas Disponíveis", icon="💼")

# 4. Layout Principal (Área de Destaque)
col_txt, col_img = st.columns([1, 1.1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True) # Espaço para alinhar com a imagem
    st.markdown("<h1 style='font-size: 46px; font-weight: 800; line-height: 1.1;'>Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 19px; color: #64748B;'>A plataforma inteligente que une profissionais qualificados às empresas que buscam excelência.</p>", unsafe_allow_html=True)

with col_img:
    # A imagem que será modernizada e descida pelo CSS
    st.image("capa_prof.png", use_container_width=True)

# 5. Seção de Ações (Cards inferiores)
st.markdown("<br><br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1: # CARD ESQUERDO: CADASTRO
    st.markdown("""
        <div class="custom-card">
            <h3>📄 Cadastrar Currículo</h3>
            <p style="color: #64748B;">Dê visibilidade ao seu talento para as melhores empresas.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Cadastro ➡️", key="btn_cad", use_container_width=True):
        st.switch_page("pages/candidatos.py")

with c2: # CARD DIREITO: VAGAS
    st.markdown("""
        <div class="custom-card">
            <h3>🔎 Buscar Vagas</h3>
            <p style="color: #64748B;">Encontre a oportunidade ideal para o seu perfil profissional.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Vagas 🔍", key="btn_vagas", use_container_width=True):
        st.switch_page("pages/vagas.py")
