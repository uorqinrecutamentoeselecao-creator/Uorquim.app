import streamlit as st

# CONFIG
st.set_page_config(
    page_title="Üorquin - Portal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PROFISSIONAL
st.markdown("""
<style>
header {visibility: hidden;}
.block-container {
    padding-top: 2rem !important;
}

/* SIDEBAR */
[data-testid="stSidebarContent"] {
    background-color: #ffffff !important;
    padding-top: 1rem !important;
}

.logo-container {
    padding: 20px 20px 30px 20px;
}

[data-testid="stSidebarNavLink"] {
    margin: 4px 15px !important;
    border-radius: 12px !important;
    padding: 12px 15px !important;
    transition: 0.3s;
}

[data-testid="stSidebarNavLink"][aria-current="page"] {
    background-color: #F1F3F9 !important;
    font-weight: 600 !important;
}

/* HERO */
.main-title {
    font-size: 46px;
    font-weight: 800;
    line-height: 1.1;
    color: #0F172A;
}

.subtitle {
    font-size: 18px;
    color: #64748B;
    margin-top: 10px;
}

/* BOTÕES */
.btn-primary button {
    background-color: #22C55E;
    color: white;
    border-radius: 12px;
    height: 50px;
    font-weight: 600;
}

.btn-secondary button {
    border-radius: 12px;
    height: 50px;
    font-weight: 600;
}

/* CARDS */
.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #F1F5F9;
    transition: 0.3s;
    cursor: pointer;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
}

/* STATS */
.stats {
    background: #F8FAFC;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

/* PROGRESSO */
.progress-box {
    background: #F8FAFC;
    padding: 20px;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("logo.png", width=160)
    st.markdown('</div>', unsafe_allow_html=True)

    st.page_link("portal.py", label="Portal", icon="🏠")
    st.page_link("pages/candidatos.py", label="Candidatos", icon="👤")
    st.page_link("pages/vagas.py", label="Vagas", icon="💼")

    st.markdown("""
    <div style="margin-top:50px; padding:20px; color:#94A3B8; font-size:14px;">
    Conectando pessoas a oportunidades
    </div>
    """, unsafe_allow_html=True)

# HERO
col1, col2 = st.columns([1.2,1])

with col1:
    st.markdown("""
    <div class='main-title'>
        Conectando <span style='color:#22C55E;'>talentos</span><br>
        às melhores oportunidades
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='subtitle'>A plataforma inteligente que une profissionais qualificados às empresas.</div>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)

    with b1:
        if st.button("Cadastrar currículo", use_container_width=True):
            st.switch_page("pages/candidatos.py")

    with b2:
        if st.button("Buscar vagas", use_container_width=True):
            st.switch_page("pages/vagas.py")

with col2:
    st.image("capa_prof.png", use_container_width=True)

# PROGRESSO + STATS
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("<div class='stats'><b>+45 mil</b><br>Profissionais</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='stats'><b>+2.500</b><br>Empresas</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='stats'><b>+8.900</b><br>Vagas</div>", unsafe_allow_html=True)

with c4:
    st.markdown("<div class='stats'><b>98%</b><br>Satisfação</div>", unsafe_allow_html=True)

# AÇÕES
st.markdown("<br><h4>O que você deseja fazer hoje?</h4>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    if st.button("📄 Cadastrar Currículo", use_container_width=True):
        st.switch_page("pages/candidatos.py")

    st.markdown("""
    <div class="card">
        Destaque seu perfil para recrutadores e aumente suas chances.
    </div>
    """, unsafe_allow_html=True)

with c2:
    if st.button("🔎 Buscar Vagas", use_container_width=True):
        st.switch_page("pages/vagas.py")

    st.markdown("""
    <div class="card">
        Encontre oportunidades filtradas por sua área de atuação.
    </div>
    """, unsafe_allow_html=True)
