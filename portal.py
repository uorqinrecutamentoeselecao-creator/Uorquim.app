import streamlit as st

# 1. Configuração de Página
st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS de Alta Precisão (Ajustado para o novo layout da sidebar)
st.markdown("""
    <style>
        /* Limpeza total do topo */
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            margin-top: -2.5rem !important;
        }

        /* --- ESTILIZAÇÃO DA SIDEBAR (IGUAL À IMAGEM) --- */
        
        /* Cor de fundo da sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
        }

        /* Estilo dos links de página na sidebar */
        [data-testid="stSidebarNav"] ul {
            padding-top: 20px;
        }

        /* Customização dos links (Portal, Candidatos, Vagas) */
        div[data-testid="stSidebarNav"] ul li div a {
            font-size: 18px !important;
            font-weight: 500 !important;
            color: #1E293B !important;
            padding: 10px 15px !important;
            border-radius: 10px !important;
            margin-bottom: 5px !important;
        }

        /* Efeito de item selecionado (estilo Candidatos na imagem) */
        div[data-testid="stSidebarNav"] ul li div a[aria-current="page"] {
            background-color: #F1F3F9 !important; /* Cinza claro da imagem */
            color: #1E293B !important;
        }

        /* Linha divisória fina */
        [data-testid="stSidebar"] hr {
            margin-top: 2rem;
            margin-bottom: 2rem;
            opacity: 0.3;
        }

        /* Texto de rodapé na sidebar */
        .sidebar-footer {
            font-size: 14px;
            color: #8E9AAF;
            text-align: left;
            padding: 0 20px;
            margin-top: 40px;
        }

        /* Ajuste da Logo na Sidebar */
        [data-testid="stSidebar"] [data-testid="stImage"] {
            text-align: left;
            padding-left: 10px;
            margin-bottom: -20px;
        }

        /* --- RESTANTE DO LAYOUT --- */
        .main-title {
            font-size: 40px;
            font-weight: 700;
            line-height: 1.1;
            color: #1E293B;
            max-width: 460px; 
            margin-bottom: 18px;
        }

        .stImage img {
            border-radius: 60px 20px 80px 20px !important;
            box-shadow: 20px 20px 50px rgba(0,0,0,0.08);
            margin-top: 130px !important; 
        }

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
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    # Logo
    st.image("logo.png", width=160)
    
    # O Streamlit gera os links automaticamente se usar st.page_link ou páginas na pasta /pages
    # Para ficar idêntico à imagem, usamos ícones simples:
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")

    st.markdown("---")
    st.markdown('<p class="sidebar-footer">Conectando pessoas a oportunidades</p>', unsafe_allow_html=True)

# 4. Layout Principal (Mantido do seu original)
col_txt, col_img = st.columns([1, 1.1])

with col_txt:
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 20px; color: #64748B;'>A plataforma inteligente que une profissionais qualificados às empresas que buscam excelência.</p>", unsafe_allow_html=True)

with col_img:
    st.image("capa_prof.png", use_container_width=True)

# 5. Seção Inferior
st.markdown("<br><br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="custom-card"><h3>📄 Cadastrar Currículo</h3><p style="color: #64748B;">Destaque seu perfil para recrutadores.</p></div>', unsafe_allow_html=True)
    if st.button("Ir para Cadastro ➡️", key="btn_cad", use_container_width=True):
        st.switch_page("pages/candidatos.py")

with c2:
    st.markdown('<div class="custom-card"><h3>🔎 Buscar Vagas</h3><p style="color: #64748B;">Encontre oportunidades na sua área.</p></div>', unsafe_allow_html=True)
    if st.button("Explorar Vagas 🔍", key="btn_vagas", use_container_width=True):
        st.switch_page("pages/vagas.py")
