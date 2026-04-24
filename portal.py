import streamlit as st



# 1. Configuração de Página

st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")



# 2. CSS de Alta Precisão

st.markdown("""

    <style>

        /* Limpeza total do topo */

        header {visibility: hidden;}

        .block-container {

            padding-top: 0rem !important;

            margin-top: -2.5rem !important;

        }



        /* TAREFA 1: LOGO - Remoção total de qualquer moldura ou restrição */

        [data-testid="stSidebar"] img {

            border-radius: 0px !important;

            box-shadow: none !important;

            border: none !important;

            background: transparent !important;

            padding: 0px !important;

            margin-left: 0px !important;

        }

        

        /* Garante que o container da logo não tenha fundo/borda */

        [data-testid="stSidebar"] [data-testid="stImage"] {

            background: transparent !important;

            border: none !important;

        }



        /* TAREFA 2: TÍTULO EM DUAS LINHAS - Controle de largura máxima */

        .main-title {

            font-size: 40px;

            font-weight: 700;

            line-height: 1.1;

            color: #1E293B;

            /* Força a quebra para duas linhas */

            max-width: 460px; 

            margin-bottom: 18px;

        }



        /* TAREFA 3: IMAGEM - Descer ainda mais e manter bordas modernas */

        .stImage img {

            border-radius: 60px 20px 80px 20px !important;

            box-shadow: 20px 20px 50px rgba(0,0,0,0.08);

            

            /* Aumentado para descer mais na página */

            margin-top: 130px !important; 

        }



        /* Estilo dos Cards Inferiores */

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



        /* Botões padronizados */

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



# 3. Sidebar

with st.sidebar:

    # Logo com largura total permitida para visibilidade

    st.image("logo.png", width=180)

    st.markdown("<br>", unsafe_allow_html=True)

    st.page_link("portal.py", label="Portal (Início)", icon="🏠")

    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")

    st.page_link("pages/vagas.py", label="Vagas Disponíveis", icon="💼")



# 4. Layout Principal

col_txt, col_img = st.columns([1, 1.1])



with col_txt:

    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)

    # Título configurado para quebrar em 2 linhas pelo CSS (main-title)

    st.markdown("<div class='main-title'>Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 20px; color: #64748B;'>A plataforma inteligente que une profissionais qualificados às empresas que buscam excelência.</p>", unsafe_allow_html=True)



with col_img:

    # Imagem posicionada mais abaixo

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
