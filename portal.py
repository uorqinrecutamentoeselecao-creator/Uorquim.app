import streamlit as st

# 1. Configuração de Página
st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS "BLINDADO" (Forçando espaçamento e removendo sobreposição)
st.markdown("""
    <style>
        /* Esconder header padrão */
        header {visibility: hidden;}

        /* --- FORÇANDO A SIDEBAR A SE COMPORTAR --- */
        
        /* 1. Criar um respiro no topo da sidebar para a logo não encavalar */
        [data-testid="stSidebarContent"] {
            padding-top: 2rem !important;
            background-color: white !important;
        }

        /* 2. Estilizar o container da Logo */
        .logo-box {
            padding: 0px 20px 30px 20px; /* Margem inferior de 30px para afastar o menu */
            display: block;
        }

        /* 3. Ajustar os Links de Navegação (Menu) */
        /* Isso seleciona os botões de navegação novos do Streamlit */
        [data-testid="stSidebarNavItems"] {
            padding-top: 20px !important;
        }

        /* Estilo de cada item do menu */
        [data-testid="stSidebarNavLink"] {
            background-color: transparent !important;
            border-radius: 12px !important;
            margin: 4px 12px !important;
            padding: 10px 15px !important;
            height: auto !important;
        }

        /* Estilo do item ATIVO (igual à sua imagem) */
        [data-testid="stSidebarNavLink"][aria-current="page"] {
            background-color: #F1F3F9 !important; /* Cinza claro do print */
            color: black !important;
        }

        /* 4. Rodapé da Sidebar */
        .sidebar-footer {
            margin-top: 50px;
            padding: 20px;
            border-top: 1px solid #f0f0f0;
            color: #8E9AAF;
            font-size: 14px;
        }

        /* Ajuste para a logo não sumir/cortar */
        [data-testid="stSidebar"] img {
            max-width: 150px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Organização da Sidebar
with st.sidebar:
    # Logo dentro de uma div com classe para controle total de espaço
    st.markdown('<div class="logo-box">', unsafe_allow_html=True)
    st.image("logo.png") # Certifique-se de que o arquivo logo.png está na pasta
    st.markdown('</div>', unsafe_allow_html=True)

    # Menu de Navegação
    # Usando st.page_link para controle manual e evitar que o Streamlit bagunce
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")

    # Texto de rodapé
    st.markdown("""
        <div class="sidebar-footer">
            Conectando pessoas a<br>oportunidades
        </div>
    """, unsafe_allow_html=True)

# 4. Conteúdo Principal
st.title("Conteúdo Principal")
st.write("Agora os elementos devem estar separados e organizados.")
