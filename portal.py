import streamlit as st

# 1. Configuração de Página
st.set_page_config(
    page_title="Üorquin - Portal", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CSS Blindado (Corrigindo o espaçamento e a sobreposição)
st.markdown("""
    <style>
        /* Limpeza do Header e ajuste de margem superior */
        header {visibility: hidden;}
        .block-container {
            padding-top: 2rem !important;
        }

        /* --- SIDEBAR DESIGN (ALINHAMENTO COM A IMAGEM) --- */
        
        /* Cor de fundo e espaçamento do container da Sidebar */
        [data-testid="stSidebarContent"] {
            background-color: #ffffff !important;
            padding-top: 1rem !important;
        }

        /* Espaçamento customizado para a Logo (evita encavalar) */
        .logo-container {
            padding: 20px 20px 40px 20px;
            display: flex;
            justify-content: flex-start;
        }

        /* Links de Navegação */
        [data-testid="stSidebarNavLink"] {
            margin: 4px 15px !important;
            border-radius: 12px !important;
            padding: 12px 15px !important;
            transition: 0.3s;
        }

        /* Destaque do item selecionado (cinza claro da imagem) */
        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background-color: #F1F3F9 !important;
            font-weight: 600 !important;
        }

        /* Rodapé da Sidebar */
        .sidebar-footer {
            margin-top: 60px;
            padding: 0 30px;
            border-top: 1px solid #f0f0f2;
            padding-top: 20px;
            color: #8E9AAF;
            font-size: 14px;
            line-height: 1.4;
        }

        /* --- CONTEÚDO PRINCIPAL --- */
        .main-title {
            font-size: 42px;
            font-weight: 700;
            line-height: 1.1;
            color: #1E293B;
            max-width: 500px;
            margin-bottom: 20px;
        }

        .custom-card {
            background-color: white;
            padding: 30px;
            border-radius: 20px;
            border: 1px solid #F1F5F9;
            min-height: 180px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (Refatorada)
with st.sidebar:
    # Logo isolada em uma div para garantir o espaço
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("logo.png", width=160)
    st.markdown('</div>', unsafe_allow_html=True)

    # Navegação limpa
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")

    # Frase de efeito no rodapé
    st.markdown("""
        <div class="sidebar-footer">
            Conectando pessoas a<br>oportunidades
        </div>
    """, unsafe_allow_html=True)

# 4. Layout Principal (Refatorado com Colunas)
col_txt, col_spacer, col_img = st.columns([1.2, 0.2, 1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div class='main-title'>
            Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='font-size: 20px; color: #64748B;'>A plataforma inteligente que une profissionais qualificados às empresas que buscam excelência.</p>", unsafe_allow_html=True)

with col_img:
    # Espaço para a imagem de capa
    st.image("capa_prof.png", use_container_width=True)

# 5. Seção de Ação (Cards)
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="custom-card">
            <h3 style='margin-top:0'>📄 Cadastrar Currículo</h3>
            <p style="color: #64748B;">Destaque seu perfil para recrutadores e aumente suas chances.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Cadastro ➡️", key="btn_cad", use_container_width=True):
        st.switch_page("pages/candidatos.py")

with c2:
    st.markdown("""
        <div class="custom-card">
            <h3 style='margin-top:0'>🔎 Buscar Vagas</h3>
            <p style="color: #64748B;">Encontre oportunidades filtradas por sua área de atuação.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Vagas 🔍", key="btn_vagas", use_container_width=True):
        st.switch_page("pages/vagas.py")
