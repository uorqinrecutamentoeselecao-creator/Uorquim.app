import streamlit as st

# 1. Configuração de Página
st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS de Alta Precisão para organizar a Sidebar
st.markdown("""
    <style>
        /* Limpeza do topo e margens */
        header {visibility: hidden;}
        .block-container { padding-top: 0rem !important; }

        /* --- ORGANIZAÇÃO DA SIDEBAR --- */
        
        /* Fundo branco e largura da sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #f0f0f0;
        }

        /* Ajuste do container da logo para não encavalar */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0rem !important;
            padding-top: 1rem;
        }

        /* Estilo da Logo */
        .logo-container {
            padding: 20px 20px 40px 20px;
        }

        /* Estilização dos Links (Menu) */
        /* Remove o padding padrão do nav do streamlit */
        [data-testid="stSidebarNav"] {
            padding-top: 0rem !important;
        }

        /* Ajusta cada item do menu */
        div[data-testid="stSidebarNav"] ul li div a {
            padding: 12px 20px !important;
            margin: 4px 15px !important;
            border-radius: 12px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            color: #334155 !important;
            transition: all 0.2s;
        }

        /* Efeito de item Selecionado/Ativo (Fundo cinza claro arredondado) */
        div[data-testid="stSidebarNav"] ul li div a[aria-current="page"] {
            background-color: #F1F5F9 !important;
            color: #0F172A !important;
        }

        /* Hover para melhorar a experiência */
        div[data-testid="stSidebarNav"] ul li div a:hover {
            background-color: #F8FAFC !important;
        }

        /* Linha divisória fina e frase de efeito */
        .sidebar-footer-container {
            position: fixed;
            bottom: 30px;
            width: 100%;
            padding: 0 30px;
        }
        
        .footer-line {
            border-top: 1px solid #E2E8F0;
            margin-bottom: 20px;
            width: 80%;
        }

        .footer-text {
            color: #94A3B8;
            font-size: 14px;
            line-height: 1.4;
        }

        /* Esconder o ícone padrão de "setinha" do menu que o streamlit coloca às vezes */
        [data-testid="stSidebarNav"] svg {
            color: #64748B;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Organizada
with st.sidebar:
    # Usando um container div para a logo para controlar o respiro (espaçamento)
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("logo.png", width=160) # Ajuste o caminho da sua logo aqui
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Navegação (O Streamlit cuida dos links se os arquivos estiverem na pasta /pages)
    # Mas aqui garantimos que os nomes fiquem limpos
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")

    # Rodapé da Sidebar
    st.markdown('<div style="margin-top: 40px; padding: 0 20px;"><hr style="opacity:0.3;"></div>', unsafe_allow_html=True)
    st.markdown('<p style="padding: 0 25px; color: #94A3B8; font-size: 14px;">Conectando pessoas a oportunidades</p>', unsafe_allow_html=True)

# 4. Conteúdo Principal (Apenas para visualização)
st.title("Conteúdo Principal")
st.write("A barra lateral agora deve seguir o padrão de espaçamento da imagem.")
