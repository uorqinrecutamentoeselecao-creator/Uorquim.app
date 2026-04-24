import streamlit as st

# 1. Configuração inicial - DEVE SER A PRIMEIRA LINHA
st.set_page_config(page_title="Üorquin - Portal", layout="wide")

# 2. CSS Avançado para subir o conteúdo e trocar a imagem
st.markdown("""
    <style>
        /* Remove o espaço em branco gigante no topo */
        .block-container {
            padding-top: 1rem !important;
            margin-top: -2rem !important;
        }
        
        /* Estilização da Sidebar */
        [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #E2E8F0;
        }

        /* Título Principal */
        .main-title {
            color: #0F172A;
            font-size: 42px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 10px;
        }
        .highlight { color: #22C55E; }
        
        /* Ajuste para as janelas de baixo subirem */
        div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
            margin-top: -10px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (Agora sem duplicados se você fez o Passo 1)
with st.sidebar:
    st.image("logo.png", width=140)
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    st.markdown("<br><br>---")
    st.caption("Conectando pessoas a oportunidades")

# 4. Conteúdo Superior
col_txt, col_img = st.columns([1.2, 1])

with col_txt:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Conectando <span class='highlight'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)
    st.write("Encontre vagas que combinam com seu perfil ou cadastre seu currículo em poucos minutos.")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 Buscar Vagas", type="primary", use_container_width=True):
            st.switch_page("pages/vagas.py")
    with c2:
        if st.button("📝 Cadastrar Currículo", use_container_width=True):
            st.switch_page("pages/candidatos.py")

with col_img:
    # IMAGEM CORRETA (MOÇA DO MODELO 01)
    st.image("https://img.freepik.com/fotos-gratis/mulher-negra-sorridente-trabalhando-no-laptop_23-2148472147.jpg", use_container_width=True)
    
    # Métrica flutuante
    st.markdown("""
        <div style='display: flex; gap: 10px; margin-top: -50px; justify-content: flex-end;'>
            <div style='background: white; padding: 10px; border-radius: 8px; border: 1px solid #EEE; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
                <small>Vagas Ativas</small><br><strong>1.248</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. Seção "O que deseja fazer hoje" - AJUSTADA PARA SUBIR
st.markdown("---")
st.markdown("<b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)

ca, cb = st.columns(2)
with ca:
    with st.container(border=True):
        st.markdown("**Buscar Vagas**")
        st.caption("Explore oportunidades em diversas áreas.")
        if st.button("Explorar agora ➡️", key="v_btn"):
            st.switch_page("pages/vagas.py")

with cb:
    with st.container(border=True):
        st.markdown("**Cadastrar Currículo**")
        st.caption("Seja visto por grandes empresas.")
        if st.button("Cadastrar agora ➡️", key="c_btn"):
            st.switch_page("pages/candidatos.py")
