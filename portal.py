import streamlit as st

# 1. Configuração de Página
st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS de Precisão (Logo, Título e Alinhamento de Imagem)
st.markdown("""
    <style>
        /* Limpeza de cabeçalho e topo */
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            margin-top: -2rem !important;
        }

        /* LOGO: Remoção total de bordas e sombras para visibilidade total */
        [data-testid="stSidebar"] img {
            border-radius: 0px !important;
            box-shadow: none !important;
            border: none !important;
            background: transparent !important;
            padding: 0px !important;
        }
        
        /* Limpeza de textos residuais na sidebar */
        section[data-testid="stSidebar"] .stMarkdown {
            display: none !important;
        }

        /* TÍTULO: Forçar duas linhas usando max-width */
        .main-title {
            font-size: 46px;
            font-weight: 800;
            line-height: 1.1;
            max-width: 500px; /* Ajuste este valor se necessário para seu monitor */
            margin-bottom: 20px;
        }

        /* IMAGEM: Descer e aplicar curvas modernas */
        .stImage img {
            border-radius: 60px 20px 80px 20px !important;
            box-shadow: 20px 20px 50px rgba(0,0,0,0.08);
            
            /* AJUSTE: Força a imagem a descer para o meio da área branca */
            margin-top: 80px !important; 
        }

        /* CARDS: Estilo estável */
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

        /* BOTÕES: Unificados e Limpos */
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

# 3. Sidebar (Logo sem bordas)
with st.sidebar:
    st.image("logo.png", width=170)
    st.page_link("portal.py", label="Portal (Início)", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas Disponíveis", icon="💼")

# 4. Conteúdo Superior
col_txt, col_img = st.columns([1, 1.1])

with col_txt:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    # TÍTULO EM DUAS LINHAS
    st.markdown("<div class='main-title'>Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 19px; color: #64748B;'>A plataforma inteligente que une profissionais qualificados às empresas que buscam excelência.</p>", unsafe_allow_html=True)

with col_img:
    # IMAGEM DESCIDA E COM BORDAS CURVAS
    st.image("capa_prof.png", use_container_width=True)

# 5. Seção de Ações
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="custom-card"><h3>📄 Cadastrar Currículo</h3><p style="color: #64748B;">Seja visto por grandes empresas.</p></div>', unsafe_allow_html=True)
    if st.button("Ir para Cadastro ➡️", key="btn_cad", use_container_width=True):
        st.switch_page("pages/candidatos.py")

with c2:
    st.markdown('<div class="custom-card"><h3>🔎 Buscar Vagas</h3><p style="color: #64748B;">Encontre o match perfeito para seu perfil.</p></div>', unsafe_allow_html=True)
    if st.button("Explorar Vagas 🔍", key="btn_vagas", use_container_width=True):
        st.switch_page("pages/vagas.py")
