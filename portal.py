import streamlit as st

st.set_page_config(page_title="Üorquin - Portal", layout="wide", page_icon="🚀")

# CSS para visual profissional (IDÊNTICO AO MODELO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    [data-testid="stAppViewContainer"] { background-color: #F8FAFC; }
    
    .main-title { color: #1E293B; font-size: 42px; font-weight: 800; line-height: 1.2; }
    .highlight { color: #22C55E; }
    
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s;
        border: 1px solid #E2E8F0;
    }
    
    .stButton > button:hover {
        border-color: #3B82F6;
        color: #3B82F6;
    }

    div[data-testid="stVerticalBlock"] > div:has(div.card-home) {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Topo / Header
col_txt, col_img = st.columns([1.2, 1])

with col_txt:
    st.image("logo.png", width=120)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>Conectando <span class='highlight'>talentos</span> às melhores oportunidades</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:18px;'>Encontre vagas que combinam com seu perfil ou cadastre seu currículo em poucos minutos.</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.2])
    with c1:
        if st.button("🔍 Buscar Vagas", type="primary", use_container_width=True):
            st.switch_page("pages/vagas.py")
    with c2:
        if st.button("📝 Cadastrar Currículo", use_container_width=True):
            st.switch_page("pages/candidatos.py")

with col_img:
    st.image("https://img.freepik.com/fotos-gratis/mulher-negra-sorridente-trabalhando-no-laptop_23-2148472147.jpg")

st.markdown("<br><br><b>O que você deseja fazer hoje?</b>", unsafe_allow_html=True)

# Cards de Opção
c_a, c_b = st.columns(2)
with c_a:
    with st.container(border=True):
        st.markdown("### 🔎 Buscar Vagas")
        st.write("Explore oportunidades na sua região e áreas de atuação.")
        if st.button("Explorar agora", key="vagas_btn"):
            st.switch_page("pages/vagas.py")

with c_b:
    with st.container(border=True):
        st.markdown("### 📄 Cadastrar Currículo")
        st.write("Seja visto pelas melhores empresas do mercado.")
        if st.button("Fazer cadastro", key="cad_btn"):
            st.switch_page("pages/candidatos.py")
