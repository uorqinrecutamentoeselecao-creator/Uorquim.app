import streamlit as st

# 1. Configuração inicial
st.set_page_config(page_title="Üorquin - Portal", layout="wide")

# 2. CSS de Limpeza Total
st.markdown("""
    <style>
        /* Remove o espaço do topo e as linhas divisórias padrão */
        .block-container {
            padding-top: 1rem !important;
            margin-top: -4rem !important;
        }
        
        /* ESCONDE OS QUADRADOS E LINHAS QUE ESTAVAM EM VERMELHO */
        hr {
            display: none !important;
        }
        
        .stHorizontalBlock {
            border: none !important;
        }

        /* Limpa o menu lateral duplicado */
        [data-testid="sidebar-nav-items"] {
            display: none !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #E2E8F0;
        }

        /* Título e Destaque */
        .main-title {
            color: #0F172A;
            font-size: 42px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 20px;
        }
        .highlight { color: #22C55E; }
        
        /* Ajuste da imagem para não ser quadrada */
        .img-container img {
            border-radius: 30px 100px 30px 100px;
            box-shadow: 20px 20px 60px #d9d9d9;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
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

# 4. Conteúdo Superior (Área Limpa)
col_txt, col_img = st.columns([1.2, 1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Conectando <span class='highlight'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)
    st.write("Bem-vindo à Üorquin. Simplificamos a conexão entre quem busca oportunidades e quem precisa de talento.")

with col_img:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Tenta carregar a imagem local
    st.image("capa_prof.jpg", use_container_width=True)
    
    # Métrica flutuante
    st.markdown("""
        <div style='display: flex; gap: 10px; margin-top: -50px; justify-content: flex-end;'>
            <div style='background: white; padding: 12px; border-radius: 10px; border: 1px solid #EEE; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
                <small style='color:gray'>Vagas Ativas</small><br><strong>1.248</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. Seção de Ações (Ordem Invertida: Currículo Primeiro)
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a: # LADO ESQUERDO
    with st.container(border=True):
        st.markdown("### 📄 Cadastrar Currículo")
        st.write("Dê o próximo passo na sua carreira.")
        if st.button("Ir para Cadastro ➡️", key="btn_cand", use_container_width=True):
            st.switch_page("pages/candidatos.py")

with col_b: # LADO DIREITO
    with st.container(border=True):
        st.markdown("### 🔎 Buscar Vagas")
        st.write("Encontre o match perfeito para o seu perfil.")
        if st.button("Explorar Vagas ➡️", key="btn_vagas", type="primary", use_container_width=True):
            st.switch_page("pages/vagas.py")
