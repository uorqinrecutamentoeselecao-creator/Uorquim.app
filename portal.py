import streamlit as st

# 1. Configuração de Página
st.set_page_config(page_title="Üorquin - Portal", layout="wide")

# 2. CSS Avançado para Curvas Orgânicas e Unificação de Cores
st.markdown("""
    <style>
        /* Limpeza de cabeçalho e margens */
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem !important;
            margin-top: -2rem !important;
        }

        /* SIDEBAR: Remove textos residuais e ajusta logo */
        section[data-testid="stSidebar"] .stMarkdown {
            display: none !important;
        }
        [data-testid="stSidebar"] img {
            border-radius: 0px !important; /* Remove arredondamento da logo */
            padding: 5px;
        }

        /* IMAGEM PRINCIPAL: Curvas Dinâmicas e Atuais */
        .stImage img {
            border-radius: 60px 20px 80px 20px !important; /* Curvas orgânicas */
            box-shadow: 20px 20px 50px rgba(0,0,0,0.08);
            object-fit: cover;
            transition: transform 0.5s ease;
        }
        .stImage img:hover {
            transform: scale(1.01);
        }

        /* CARDS: Ajuste de altura e padding */
        .custom-card {
            background-color: white;
            padding: 35px;
            border-radius: 20px;
            border: 1px solid #F1F5F9;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
            margin-bottom: 10px;
        }

        /* BOTÕES: Unificação de cor (Estilo "Cadastrar Currículo") */
        /* Forçamos os botões a serem brancos com borda cinza, mudando apenas no hover */
        .stButton > button {
            background-color: white !important;
            color: #1E293B !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            height: 45px;
            transition: all 0.3s ease !important;
        }

        /* Efeito de destaque ao passar o mouse */
        .stButton > button:hover {
            border-color: #22C55E !important;
            color: #22C55E !important;
            background-color: #F8FAFC !important;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (Menu)
with st.sidebar:
    st.image("logo.png", width=160) # Aumentado levemente para melhor qualidade
    st.markdown("<br>", unsafe_allow_html=True)
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")

# 4. Conteúdo Superior
col_txt, col_img = st.columns([1, 1.1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 46px; font-weight: 800; line-height: 1.1;'>Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 19px; color: #64748B;'>A plataforma inteligente que une profissionais qualificados às empresas que buscam excelência.</p>", unsafe_allow_html=True)

with col_img:
    st.image("capa_prof.jpg", use_container_width=True)

# 5. Cards de Ação (Unificados)
st.markdown("<br><br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="custom-card">
            <h3>📄 Cadastrar Currículo</h3>
            <p style='color: #64748B;'>Dê visibilidade ao seu talento para as melhores empresas.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Cadastro ➡️", key="btn_cad", use_container_width=True):
        st.switch_page("pages/candidatos.py")

with c2:
    st.markdown("""
        <div class="custom-card">
            <h3>🔎 Buscar Vagas</h3>
            <p style='color: #64748B;'>Encontre agora a oportunidade que combina com você.</p>
        </div>
    """, unsafe_allow_html=True)
    # Agora o botão de vagas segue o mesmo padrão visual (branco/clean) do anterior
    if st.button("Explorar Vagas 🔍", key="btn_vagas", use_container_width=True):
        st.switch_page("pages/vagas.py")
