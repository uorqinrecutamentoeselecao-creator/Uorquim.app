import streamlit as st

# 1. Configuração de Página
st.set_page_config(page_title="Üorquin - Portal", layout="wide")

# 2. CSS Avançado (Limpeza Total e Efeitos de Botão)
st.markdown("""
    <style>
        /* Remove o cabeçalho e limpa o topo */
        header {visibility: hidden;}
        .block-container {
            padding-top: 1rem !important;
            margin-top: -2rem !important;
        }

        /* ESCONDE O TEXTO <br> QUE REAPARECEU NA SIDEBAR */
        section[data-testid="stSidebar"] .stMarkdown {
            display: none !important;
        }
        /* Mas permite que a logo e os links apareçam */
        section[data-testid="stSidebar"] [data-testid="stImage"], 
        section[data-testid="stSidebar"] [data-testid="stPageLink"] {
            display: block !important;
        }

        /* Ajuste Dinâmico da Imagem para ocupar mais espaço abaixo */
        .stImage img {
            border-radius: 20px !important;
            box-shadow: 10px 10px 30px rgba(0,0,0,0.05);
            max-height: 450px;
            object-fit: cover;
        }

        /* Estilização dos Cards para evitar desconfiguração */
        .custom-card {
            background-color: white;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #E2E8F0;
            height: 220px; /* Altura fixa para alinhar os botões */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            margin-bottom: 15px;
        }

        /* Efeito de Cor no Botão ao passar o mouse (Hover) */
        .stButton > button {
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            filter: brightness(0.9);
            border-color: #22C55E !important;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Limpa
with st.sidebar:
    st.image("logo.png", width=130)
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    # Removido qualquer markdown manual para evitar erros de cache

# 4. Layout Superior
col_txt, col_img = st.columns([1, 1.2])

with col_txt:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 44px; font-weight: 800;'>Conectando <span style='color: #22C55E;'>talentos</span> às melhores oportunidades</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #64748B;'>Simplificamos a conexão entre quem busca oportunidades e quem precisa de talento.</p>", unsafe_allow_html=True)

with col_img:
    # Imagem ocupando mais espaço vertical
    st.image("capa_prof.png", use_container_width=True)

# 5. Cards de Ação (Ordem Invertida e Alinhada)
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div class="custom-card">
            <div>
                <h3>📄 Cadastrar Currículo</h3>
                <p style='color: #64748B;'>Seja visto por grandes empresas e impulsione sua carreira.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ir para Cadastro ➡️", key="btn_cad", use_container_width=True):
        st.switch_page("pages/candidatos.py")

with c2:
    st.markdown("""
        <div class="custom-card">
            <div>
                <h3>🔎 Buscar Vagas</h3>
                <p style='color: #64748B;'>Encontre o match perfeito para o seu perfil profissional hoje mesmo.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Vagas 🔍", key="btn_vagas", type="primary", use_container_width=True):
        st.switch_page("pages/vagas.py")
