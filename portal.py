import streamlit as st

st.set_page_config(page_title="Uorquin", layout="wide")

# =========================
# CSS GLOBAL
# =========================
st.markdown("""
<style>

body {
    background-color: #f5f7fb;
}

.main-title {
    font-size:42px;
    font-weight:800;
    text-align:center;
    color:#1f2c56;
}

.subtitle {
    text-align:center;
    font-size:18px;
    color:gray;
}

.card-home {
    background:white;
    padding:30px;
    border-radius:16px;
    text-align:center;
    box-shadow:0px 6px 20px rgba(0,0,0,0.08);
    transition:0.3s;
}
.card-home:hover {
    transform:scale(1.03);
}

.big-btn {
    background:#1f77ff;
    color:white;
    padding:12px 20px;
    border-radius:8px;
    text-decoration:none;
    display:inline-block;
    margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.image("logo.png", width=180)

st.markdown("<div class='main-title'>🚀 Portal de Vagas Uorquin</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Conectando talentos às melhores oportunidades</div>", unsafe_allow_html=True)

st.divider()

# =========================
# CARDS PRINCIPAIS
# =========================
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card-home">
        <h3>🔎 Buscar Vagas</h3>
        <p>Explore oportunidades na sua região</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Ver Vagas"):
        st.switch_page("pages/vagas.py")

with col2:
    st.markdown("""
    <div class="card-home">
        <h3>📄 Cadastrar Currículo</h3>
        <p>Se candidate rapidamente às vagas</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Cadastrar"):
        st.switch_page("pages/candidatos.py")

st.divider()

st.markdown("<p style='text-align:center;color:gray'>© 2026 Uorquin - Todos os direitos reservados</p>", unsafe_allow_html=True)
