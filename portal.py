import streamlit as st

# 1. Configuração inicial - DEVE SER A PRIMEIRA LINHA
st.set_page_config(page_title="Üorquin - Portal", layout="wide", initial_sidebar_state="expanded")

# 2. CSS Avançado para os 3 ajustes (Subir conteúdo, limpar áreas e inverter)
st.markdown("""
    <style>
        /* AJUSTE 1: Remove o espaço gigante no topo e sobe todo o conteúdo */
        .block-container {
            padding-top: 1rem !important;
            margin-top: -4rem !important;
        }
        
        /* Limpa a barra lateral duplicada padrão */
        [data-testid="sidebar-nav-items"] {
            display: none !important;
        }
        
        /* Estilização da Sidebar (Fundo Branco) */
        [data-testid="stSidebar"] {
            background-color: white !important;
            border-right: 1px solid #E2E8F0;
        }

        /* Título Principal Estilizado */
        .main-title {
            color: #0F172A;
            font-size: 42px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 20px;
        }
        .highlight { color: #22C55E; }
        
        /* Estilo para os cards de ação (Cards mais dinâmicos) */
        .action-card {
            background-color: white;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            transition: all 0.3s;
            margin-bottom: 20px;
        }
        .action-card:hover {
            border-color: #3B82F6;
            transform: translateY(-2px);
        }
        
        /* Estilo para o botão dentro do card (Azul SaaS) */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Customizada (Sem duplicados agora)
with st.sidebar:
    # Tenta carregar a logo
    try:
        st.image("logo.png", width=140)
    except:
        st.title("Üorquin")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Criando os links manualmente com ícones
    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Conectando pessoas a oportunidades")

# 4. Conteúdo Superior
col_txt, col_img = st.columns([1.2, 1])

with col_txt:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Conectando <span class='highlight'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)
    st.write("Bem-vindo à Üorquin. Simplificamos a conexão entre quem busca oportunidades e quem precisa de talento. Escolha abaixo como deseja prosseguir:")
    # Removemos o traço divisor aqui para limpar a área
    # st.markdown("---")

with col_img:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Tenta carregar a imagem profissional local (capa_prof.jpg)
    try:
        st.image("capa_prof.jpg", use_container_width=True)
    except:
        # Link de fallback para testes se você ainda não subiu a imagem
        st.image("https://image.replicate.delivery/pbxt/44910243/45b5-4556-91e6-42d8f7b538e1/image_6.png", use_container_width=True)
    
    # Métrica flutuante (Estilo imagem 01)
    st.markdown("""
        <div style='display: flex; gap: 10px; margin-top: -50px; justify-content: flex-end;'>
            <div style='background: white; padding: 12px; border-radius: 10px; border: 1px solid #EEE; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
                <small style='color:gray'>Vagas Ativas</small><br><strong>1.248</strong>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 5. Seção de Ações (Subiu de posição)
st.markdown("<br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# AJUSTE 2: INVERTE A ORDEM DAS COLUNAS (Primeiro 'Candidatos', depois 'Vagas')
col_a, col_b = st.columns(2)

# Card de Cadastro de Currículo (Agora na Esquerda)
with col_a:
    st.markdown("<div class='action-card'>", unsafe_allow_html=True)
    st.markdown("### 📄 Cadastrar Currículo")
    st.write("Cadastre seu currículo e seja visto pelas melhores empresas do mercado. Dê o próximo passo na sua carreira.")
    if st.button("Ir para Cadastro ➡️", key="btn_candidatos", use_container_width=True):
        st.switch_page("pages/candidatos.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Card de Busca de Vagas (Agora na Direita)
with col_b:
    st.markdown("<div class='action-card'>", unsafe_allow_html=True)
    st.markdown("### 🔎 Buscar Vagas")
    st.write("Explore oportunidades na sua região e áreas de atuação. Encontre o match perfeito para o seu perfil.")
    if st.button("Explorar Vagas ➡️", key="btn_vagas", type="primary", use_container_width=True):
        st.switch_page("pages/vagas.py")
    st.markdown("</div>", unsafe_allow_html=True)
