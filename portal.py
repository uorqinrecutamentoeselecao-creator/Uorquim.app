import streamlit as st

# 1. CONFIGURAÇÃO (O 'label_visibility' ajuda a limpar o topo)
st.set_page_config(
    page_title="Üorquin - Portal", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS PARA ESCONDER A LISTA PADRÃO E DEIXAR IGUAL À FOTO
st.markdown("""
    <style>
        /* Esconde a lista automática de páginas do Streamlit */
        [data-testid="sidebar-nav-items"] {
            display: none;
        }
        
        /* Ajusta o fundo e fontes */
        [data-testid="stAppViewContainer"] {
            background-color: #F8FAFC;
        }
        
        /* Estilo dos links da sidebar */
        .stPageLink {
            border-radius: 8px;
            transition: 0.3s;
        }
        
        /* Título Principal Estilizado */
        .main-title {
            color: #0F172A;
            font-size: 45px;
            font-weight: 800;
            line-height: 1.1;
        }
        .highlight {
            color: #22C55E;
        }
        
        /* Card de métricas lateral à imagem */
        .metric-card {
            background: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            border: 1px solid #E2E8F0;
            position: absolute;
            right: 10px;
            top: 50px;
            z-index: 100;
        }
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR CUSTOMIZADA (IGUAL ÀS FOTOS 01 e 02)
with st.sidebar:
    st.image("logo.png", width=140)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Criando os links manualmente com ícones
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("✨ Conectando pessoas a oportunidades")

# 4. CONTEÚDO DO PORTAL (IGUAL À FOTO 01)
col_text, col_space, col_img = st.columns([1.5, 0.1, 1.2])

with col_text:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class='main-title'>
            Conectando <span class='highlight'>talentos</span><br>
            às melhores oportunidades
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 18px;'>Encontre vagas que combinam com seu perfil ou cadastre seu currículo e dê o próximo passo na sua carreira.</p>", unsafe_allow_html=True)
    
    # Botões de ação rápida
    btn_col1, btn_col2 = st.columns([1, 1.2])
    with btn_col1:
        if st.button("🔍 Buscar Vagas", type="primary", use_container_width=True):
            st.switch_page("pages/vagas.py")
    with btn_col2:
        if st.button("📝 Cadastrar Currículo", use_container_width=True):
            st.switch_page("pages/candidatos.py")

with col_img:
    st.markdown("<br>", unsafe_allow_html=True)
    # Imagem da moça sorrindo (usando link público para teste)
    st.image("https://img.freepik.com/fotos-gratis/mulher-negra-sorridente-trabalhando-no-laptop_23-2148472147.jpg", use_column_width=True)
    
    # Simulação dos cards de métricas que flutuam na imagem
    st.markdown("""
        <div style='display: flex; gap: 10px; margin-top: -50px; position: relative; justify-content: flex-end;'>
            <div style='background: white; padding: 10px 20px; border-radius: 10px; border: 1px solid #EEE; box-shadow: 5px 5px 15px rgba(0,0,0,0.05);'>
                <small style='color: gray;'>Vagas Ativas</small><br>
                <strong style='font-size: 20px;'>1.248</strong>
            </div>
            <div style='background: white; padding: 10px 20px; border-radius: 10px; border: 1px solid #EEE; box-shadow: 5px 5px 15px rgba(0,0,0,0.05);'>
                <small style='color: gray;'>Empresas</small><br>
                <strong style='font-size: 20px;'>320+</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("#### O que você deseja fazer hoje?")

# Cards Inferiores (Navegação secundária)
c1, c2 = st.columns(2)

with c1:
    with st.container(border=True):
        col_icon, col_txt = st.columns([1, 4])
        col_icon.markdown("<h1 style='text-align: center;'>🔍</h1>", unsafe_allow_html=True)
        with col_txt:
            st.markdown("**Buscar Vagas**")
            st.caption("Explore oportunidades na sua região e em diversas áreas de atuação.")
            if st.button("Explorar Vagas ➡️", key="go_vagas"):
                st.switch_page("pages/vagas.py")

with c2:
    with st.container(border=True):
        col_icon, col_txt = st.columns([1, 4])
        col_icon.markdown("<h1 style='text-align: center;'>📄</h1>", unsafe_allow_html=True)
        with col_txt:
            st.markdown("**Cadastrar Currículo**")
            st.caption("Cadastre seu currículo e seja visto pelas melhores empresas do mercado.")
            if st.button("Fazer Cadastro ➡️", key="go_cad"):
                st.switch_page("pages/candidatos.py")
