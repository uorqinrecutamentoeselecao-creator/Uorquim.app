import streamlit as st

# 1. Configuração inicial (Sempre a primeira linha)
st.set_page_config(
    page_title="Üorquin - Portal", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS de Alta Performance (Limpeza e Dinamismo)
st.markdown("""
    <style>
        /* Remove o cabeçalho padrão e sobe todo o conteúdo */
        [data-testid="stHeader"] {
            display: none;
        }
        .block-container {
            padding-top: 1rem !important;
            margin-top: -3rem !important;
        }
        
        /* LIMPEZA TOTAL: Esconde linhas divisórias (hr) e quadrados indesejados */
        hr {
            display: none !important;
        }
        [data-testid="stVerticalBlock"] > div > div > div > hr {
            display: none !important;
        }

        /* Sidebar Clean */
        [data-testid="sidebar-nav-items"] {
            display: none !important;
        }
        [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #F1F5F9;
        }

        /* Títulos e Tipografia */
        .main-title {
            color: #0F172A;
            font-size: 44px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 15px;
        }
        .highlight { color: #22C55E; }
        
        /* Efeito de bordas dinâmicas na imagem */
        .stImage img {
            border-radius: 40px 10px 40px 10px !important;
            box-shadow: 15px 15px 50px rgba(0,0,0,0.05);
        }

        /* Estilo dos Cards de Ação */
        .action-card {
            background-color: white;
            padding: 24px;
            border-radius: 16px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (Menu Único)
with st.sidebar:
    st.image("logo.png", width=130)
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    st.markdown("<br><br>---")
    st.caption("Üorquin © 2024")

# 4. Área de Destaque (Título + Imagem Dinâmica)
col_txt, col_img = st.columns([1.1, 1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class='main-title'>
            Conectando <span class='highlight'>talentos</span> às melhores oportunidades
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #475569;'>Simplificamos a conexão entre quem busca oportunidades e quem precisa de talento.</p>", unsafe_allow_html=True)

with col_img:
    st.markdown("<br>", unsafe_allow_html=True)
    # LINHA DE BUSCA DA IMAGEM (Restaurada e Refatorada)
    st.image("capa_prof.png", use_container_width=True)
    
    # Métrica flutuante (Vagas Ativas)
    st.markdown("""
        <div style='display: flex; justify-content: flex-end; margin-top: -60px; margin-right: 20px;'>
            <div style='background: white; padding: 15px; border-radius: 12px; border: 1px solid #F1F5F9; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);'>
                <span style='color: #64748B; font-size: 12px;'>Vagas Ativas</span><br>
                <span style='font-size: 20px; font-weight: bold;'>1.248</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. Seção de Ações (ORDEM INVERTIDA E SEM QUADRADOS)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<b style='font-size: 20px;'>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col_curriculo, col_vagas = st.columns(2)

with col_curriculo: # 1º CARD: CADASTRO
    with st.container():
        st.markdown("""
            <div class='action-card'>
                <h3 style='margin-top:0;'>📄 Cadastrar Currículo</h3>
                <p style='color: #64748B;'>Seja visto por grandes empresas e dê o próximo passo na sua carreira.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Ir para Cadastro ➡️", key="btn_cad_final", use_container_width=True):
            st.switch_page("pages/candidatos.py")

with col_vagas: # 2º CARD: VAGAS
    with st.container():
        st.markdown("""
            <div class='action-card'>
                <h3 style='margin-top:0;'>🔎 Buscar Vagas</h3>
                <p style='color: #64748B;'>Explore oportunidades e encontre o match perfeito para o seu perfil profissional.</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Explorar Vagas 🔍", key="btn_vagas_final", type="primary", use_container_width=True):
            st.switch_page("pages/vagas.py")
