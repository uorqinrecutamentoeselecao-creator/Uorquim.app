import streamlit as st

st.set_page_config(layout="wide")

# CSS PESADO (NÍVEL PROFISSIONAL)
st.markdown("""
<style>
header {visibility: hidden;}
.block-container {padding-top: 2rem;}

body {
    background-color: #F8FAFC;
}

/* HERO */
.hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 40px;
}

.hero-text {
    max-width: 550px;
}

.hero h1 {
    font-size: 48px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.1;
}

.hero span {
    color: #22C55E;
}

.hero p {
    color: #64748B;
    font-size: 18px;
    margin-top: 15px;
}

/* BOTÕES */
.btn-group {
    display: flex;
    gap: 15px;
    margin-top: 20px;
}

.btn-primary {
    background: #22C55E;
    color: white;
    padding: 12px 20px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    text-align: center;
}

.btn-secondary {
    border: 1px solid #E2E8F0;
    padding: 12px 20px;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
}

/* IMAGEM */
.hero img {
    border-radius: 20px;
}

/* STATS */
.stats-container {
    display: flex;
    gap: 20px;
    margin-top: 40px;
}

.stat-box {
    flex: 1;
    background: #F1F5F9;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

.stat-box b {
    font-size: 20px;
}

/* AÇÕES */
.section-title {
    margin-top: 50px;
    font-size: 22px;
    font-weight: 600;
}

.actions {
    display: flex;
    gap: 20px;
    margin-top: 20px;
}

.action-card {
    flex: 1;
}

.action-btn {
    width: 100%;
    border: 1px solid #E2E8F0;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    cursor: pointer;
    background: white;
}

.action-desc {
    margin-top: 10px;
    padding: 20px;
    border: 1px solid #F1F5F9;
    border-radius: 16px;
    background: white;
    color: #64748B;
}

/* HOVER */
.action-btn:hover {
    background: #F8FAFC;
}

.btn-primary:hover {
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
    <div class="hero-text">
        <h1>
            Conectando <span>talentos</span><br>
            às melhores oportunidades
        </h1>
        <p>
            A plataforma inteligente que une profissionais qualificados às empresas.
        </p>

        <div class="btn-group">
            <div class="btn-primary">Cadastrar currículo</div>
            <div class="btn-secondary">Buscar vagas</div>
        </div>
    </div>

    <div>
        <img src="capa_prof.png" width="420">
    </div>
</div>
""", unsafe_allow_html=True)

# STATS
st.markdown("""
<div class="stats-container">
    <div class="stat-box"><b>+45 mil</b><br>Profissionais</div>
    <div class="stat-box"><b>+2.500</b><br>Empresas</div>
    <div class="stat-box"><b>+8.900</b><br>Vagas</div>
    <div class="stat-box"><b>98%</b><br>Satisfação</div>
</div>
""", unsafe_allow_html=True)

# AÇÕES
st.markdown('<div class="section-title">O que você deseja fazer hoje?</div>', unsafe_allow_html=True)

st.markdown("""
<div class="actions">
    <div class="action-card">
        <div class="action-btn">📄 Cadastrar Currículo</div>
        <div class="action-desc">
            Destaque seu perfil para recrutadores e aumente suas chances.
        </div>
    </div>

    <div class="action-card">
        <div class="action-btn">🔎 Buscar Vagas</div>
        <div class="action-desc">
            Encontre oportunidades filtradas por sua área de atuação.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
