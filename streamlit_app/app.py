from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Recepção Médica - Streamlit", layout="centered")

st.title("🏥 Sistema de Cadastro de Pacientes (Streamlit)")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(
        columns=["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
    )

with st.form("cadastro_paciente_form", clear_on_submit=True):
    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1, value=0)
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
    )
    prioridade = st.slider("Prioridade do atendimento (5 = Urgente)", 1, 5, value=1)
    motivo = st.text_area("Motivo da consulta / observações")

    enviado = st.form_submit_button("Cadastrar Paciente")

if enviado:
    if not nome.strip():
        st.error("⚠️ O campo 'Nome do paciente' é obrigatório.")
    else:
        nova_linha = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }

        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha])],
            ignore_index=True,
        )
        st.success("✅ Paciente cadastrado com sucesso!")

st.subheader("📋 Últimos Cadastros da Sessão")
st.dataframe(st.session_state.pacientes.tail(5), use_container_width=True)

if not st.session_state.pacientes.empty:
    csv_buffer = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exportar e Baixar CSV Atualizado",
        data=csv_buffer,
        file_name="pacientes.csv",
        mime="text/csv",
    )