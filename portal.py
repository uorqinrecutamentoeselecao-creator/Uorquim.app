import streamlit as st

st.set_page_config(page_title="Uorquin", layout="wide")

# =========================
# CSS PROFISSIONAL
# =========================
st.markdown("""
<style>

.main {
    background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 100%);
}

/* HERO */
.hero {
    text-align: center;
    padding: 40px 20px;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: #1f2c4c;
}

.hero-subtitle {
    font-size: 20px;
    color: #6b7280;
    margin-top: 10px;
}

/* BOTÕES */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 52px;
    font-weight: 600;
    font-size: 16px;
    background: #2563eb;
    color: white;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background: #1d4ed8;
}

/* CARDS */
.card-home {
    background: white;
    padding: 35px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.06);
    transition: 0.3s;
    height: 220px;
}

.card-home:hover {
    transform: translateY(-6px);
}

/* ICON */
.icon {
    font-size: 40px;
    margin-bottom: 10px;
}

.footer {
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO
# =========================
st.markdown('<div class="hero">', unsafe_allow_html=True)

st.image("logo.png", width=200)

st.markdown('<div class="hero-title">Conectando talentos às melhores oportunidades</div>', unsafe_allow_html=True)

st.markdown('<div class="hero-subtitle">Encontre empregos ou contrate profissionais de forma rápida e inteligente</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# AÇÕES PRINCIPAIS
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card-home">
        <div class="icon">🔎</div>
        <h3>Buscar Vagas</h3>
        <p>Explore oportunidades na sua região e encontre o emprego ideal</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Ver Vagas"):
        st.switch_page("pages/vagas.py")

with col2:
    st.markdown("""
    <div class="card-home">
        <div class="icon">📄</div>
        <h3>Cadastrar Currículo</h3>
        <p>Crie seu perfil e aumente suas chances de contratação</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Cadastrar Agora"):
        st.switch_page("pages/candidatos.py")

# =========================
# PROVA / CONFIANÇA
# =========================
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("Vagas disponíveis", "1.248+")
col2.metric("Empresas parceiras", "320+")
col3.metric("Candidatos cadastrados", "5.000+")

# =========================
# FOOTER
# =========================
st.markdown('<div class="footer">© 2026 Uorquin • Todos os direitos reservados</div>', unsafe_allow_html=True)
