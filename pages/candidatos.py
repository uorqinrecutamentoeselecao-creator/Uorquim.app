import streamlit as st

st.set_page_config(page_title="Uorquin", layout="wide")

# =========================
# CSS PROFISSIONAL HARDCORE
# =========================
st.markdown("""
<style>

/* BACKGROUND */
.main {
    background: #f5f7fb;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* HEADER */
.header {
    text-align: center;
    margin-bottom: 10px;
}

.title {
    font-size: 38px;
    font-weight: 800;
    color: #1f2c4c;
}

.subtitle {
    color: #6b7280;
    font-size: 16px;
}

/* CARD */
.card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
}

/* INPUT */
input, .stTextInput>div>div>input {
    border-radius: 10px !important;
}

/* BOTÕES */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-weight: 600;
    background: #2563eb;
    color: white;
}

/* STEPPER */
.stepper {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.step {
    text-align: center;
    flex: 1;
}

.circle {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: #d1d5db;
    margin: auto;
    line-height: 30px;
    color: white;
    font-size: 14px;
}

.active {
    background: #2563eb;
}

.line {
    height: 3px;
    background: #e5e7eb;
    margin: 0 5px;
    flex: 1;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.image("logo.png", width=140)
st.sidebar.markdown("### Navegação")

st.sidebar.page_link("portal.py", label="Portal")
st.sidebar.page_link("pages/candidatos.py", label="Candidatos")
st.sidebar.page_link("pages/vagas.py", label="Vagas")

# =========================
# CONTROLE
# =========================
if "step" not in st.session_state:
    st.session_state.step = 1

# =========================
# HEADER
# =========================
st.markdown('<div class="header">', unsafe_allow_html=True)
st.image("logo.png", width=160)
st.markdown('<div class="title">Crie seu currículo em poucos minutos</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Preencha seus dados e aumente suas chances</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEPPER
# =========================
steps = ["Dados", "Experiência", "Formação", "Cursos", "Final"]

step_html = '<div class="stepper">'
for i, s in enumerate(steps):
    active = "active" if i+1 <= st.session_state.step else ""
    step_html += f"""
    <div class="step">
        <div class="circle {active}">{i+1}</div>
        <small>{s}</small>
    </div>
    """
step_html += '</div>'

st.markdown(step_html, unsafe_allow_html=True)

# =========================
# CARD PRINCIPAL
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

# =========================
# STEP 1
# =========================
if st.session_state.step == 1:

    st.subheader("📌 Dados Pessoais")

    col1, col2 = st.columns(2)

    with col1:
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF")
        telefone = st.text_input("Telefone")
        email = st.text_input("Email")

    with col2:
        endereco = st.text_input("Endereço")
        estado = st.selectbox("Estado", ["BA","SP","RJ","MG"])
        cidade = st.text_input("Cidade")
        salario = st.text_input("Pretensão salarial")

    st.markdown("---")

    if st.button("Continuar ➡️"):
        st.session_state.step = 2
        st.rerun()

# =========================
# STEP 2
# =========================
elif st.session_state.step == 2:

    st.subheader("💼 Experiência")

    empresa = st.text_input("Empresa")
    funcao = st.text_input("Função")

    col1, col2 = st.columns(2)

    if col1.button("⬅️ Voltar"):
        st.session_state.step = 1
        st.rerun()

    if col2.button("Continuar ➡️"):
        st.session_state.step = 3
        st.rerun()

# =========================
# STEP FINAL
# =========================
elif st.session_state.step == 5:

    st.subheader("🎯 Finalizar")

    if st.button("Finalizar Cadastro 🚀"):
        st.success("Cadastro realizado com sucesso!")
        st.balloons()

st.markdown('</div>', unsafe_allow_html=True)
