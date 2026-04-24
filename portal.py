import streamlit as st

# 1. CONFIGURAÇÃO INICIAL
st.set_page_config(
    page_title="Üorquin - Portal", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS AVANÇADO (Limpeza de duplicados e ajustes de posição)
st.markdown("""
    <style>
        /* ESCONDE A LISTA AUTOMÁTICA DA BARRA LATERAL */
        [data-testid="sidebar-nav-items"] {
            display: none !important;
        }
        
        /* SOBE O CONTEÚDO (Remove margens excessivas do topo) */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }
        
        /* DESIGN DOS BOTÕES E TEXTOS */
        .main-title {
            color: #0F172A;
            font-size: 42px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 20px;
        }
        .highlight { color: #22C55E; }
        
        [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
        
        /* ESTILO DA SIDEBAR CUSTOMIZADA */
        [data-testid="stSidebar"] { background-color: white !important; border-right: 1px solid #E2E8F0; }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR ÚNICA (Agora sem duplicados)
with st.sidebar:
    st.image("logo.png", width=140)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Links Manuais
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("✨ Conectando pessoas a oportunidades")

# 4. LAYOUT PRINCIPAL (Ajustado para ser mais alto)
col_text, col_img = st.columns([1.2, 1])

with col_text:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class='main-title'>
            Conectando <span class='highlight'>talentos</span><br>
            às melhores oportunidades
        </div>
    """, unsafe_allow_html=True)
    st.write("Encontre vagas que combinam com seu perfil ou cadastre seu currículo e dê o próximo passo na sua carreira.")
    
    # Botões Principais
    c_btn1, c_btn2 = st.columns([1, 1])
    with c_btn1:
        if st.button("🔍 Buscar Vagas", type="primary", use_container_width=True):
            st.switch_page("pages/vagas.py")
    with c_btn2:
        if st.button("📝 Cadastrar Currículo", use_container_width=True):
            st.switch_page("pages/candidatos.py")

with col_img:
    # IMAGEM PROFISSIONAL (Substituindo a imagem 3D antiga)
    st.image("https://img.freepik.com/fotos-gratis/mulher-negra-sorridente-trabalhando-no-laptop_23-2148472147.jpg", use_container_width=True)
    
    # Cards de métricas flutuantes
    st.markdown("""
        <div style='display: flex; gap: 10px; margin-top: -40px; justify-content: center;'>
            <div style='background: white; padding: 10px 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #EEE;'>
                <small>Vagas Ativas</small><br><strong>1.248</strong>
            </div>
            <div style='background: white; padding: 10px 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #EEE;'>
                <small>Empresas</small><br><strong>320+</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. SEÇÃO "O QUE DESEJA FAZER HOJE" (Mais próxima do topo)
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.markdown("**Buscar Vagas**")
        st.caption("Explore oportunidades na sua região.")
        if st.button("Explorar agora", key="exp_vagas"):
            st.switch_page("pages/vagas.py")

with c2:
    with st.container(border=True):
        st.markdown("**Cadastrar Currículo**")
        st.caption("Seja visto por grandes empresas.")
        if st.button("Cadastrar agora", key="exp_cad"):
            st.switch_page("pages/candidatos.py")
