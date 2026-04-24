import streamlit as st

# 1. CONFIGURAÇÃO (DEVE SER A PRIMEIRA LINHA)
st.set_page_config(page_title="Üorquin - Portal", layout="wide")

# 2. CSS PARA CORRIGIR O LAYOUT (SUBIR O CONTEÚDO)
st.markdown("""
    <style>
        /* Remove o espaço gigante no topo da página */
        .block-container {
            padding-top: 0rem !important;
            margin-top: -3rem !important;
        }
        
        /* Estilo da barra lateral */
        [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Ajuste do Título */
        .main-title {
            color: #0F172A;
            font-size: 45px;
            font-weight: 800;
            line-height: 1.1;
        }
        .highlight { color: #22C55E; }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR (MENU LATERAL)
with st.sidebar:
    # Tenta carregar a logo, se não houver, usa texto
    try:
        st.image("logo.png", width=140)
    except:
        st.title("Üorquin")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    st.markdown("<br><br>---")
    st.caption("Conectando pessoas a oportunidades")

# 4. CONTEÚDO PRINCIPAL (REORGANIZADO PARA SUBIR)
col_txt, col_img = st.columns([1.2, 1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True) # Espaço controlado
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    # IMAGEM DA MOÇA SORRINDO
    st.image("https://img.freepik.com/fotos-gratis/mulher-negra-sorridente-trabalhando-no-laptop_23-2148472147.jpg", use_container_width=True)
    
    # Métrica flutuante (Estilo imagem 01)
    st.markdown("""
        <div style='display: flex; gap: 10px; margin-top: -50px; justify-content: flex-end;'>
            <div style='background: white; padding: 12px; border-radius: 10px; border: 1px solid #EEE; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
                <small style='color:gray'>Vagas Ativas</small><br><strong>1.248</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. SEÇÃO INFERIOR
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
ca, cb = st.columns(2)

with ca:
    with st.container(border=True):
        st.markdown("**Buscar Vagas**")
        st.caption("Explore oportunidades em diversas áreas.")
        if st.button("Ir para Vagas", key="v1"): st.switch_page("pages/vagas.py")

with cb:
    with st.container(border=True):
        st.markdown("**Cadastrar Currículo**")
        st.caption("Seja visto por grandes empresas.")
        if st.button("Ir para Cadastro", key="c1"): st.switch_page("pages/candidatos.py")
