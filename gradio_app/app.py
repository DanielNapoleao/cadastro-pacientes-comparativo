import os
from datetime import datetime
import gradio as gr
import pandas as pd

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome.strip():
        return "⚠️ O campo 'Nome do paciente' é obrigatório.", pd.read_csv(
            ARQUIVO_CSV
        ).tail(5) if os.path.exists(ARQUIVO_CSV) else pd.DataFrame(
            columns=COLUNAS
        ).tail(
            5
        )

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo.strip(),
    }

    novo = pd.DataFrame([linha])

    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False, encoding="utf-8")
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False, encoding="utf-8")

    return "✅ Paciente cadastrado com sucesso!", pd.read_csv(
        ARQUIVO_CSV, encoding="utf-8"
    ).tail(5)


with gr.Blocks(title="Recepção Médica - Gradio") as demo:
    gr.Markdown("## 🏥 Sistema de Cadastro de Pacientes (Gradio)")

    with gr.Column():
        nome = gr.Textbox(
            label="Nome do paciente", placeholder="Digite o nome completo"
        )
        idade = gr.Number(label="Idade", value=0, precision=0)
        convenio = gr.Dropdown(
            choices=["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
            label="Convênio",
            value="Particular",
        )
        prioridade = gr.Slider(
            minimum=1, maximum=5, step=1, label="Prioridade do atendimento (5 = Urgente)"
        )
        motivo = gr.Textbox(
            label="Motivo da consulta / observações",
            lines=3,
            placeholder="Queixas ou anotações",
        )

        botao = gr.Button("Cadastrar Paciente", variant="primary")

        saida_msg = gr.Textbox(label="Status da Operação", interactive=False)
        tabela = gr.Dataframe(
            label="Últimos 5 pacientes cadastrados",
            headers=COLUNAS,
            datatype=["str", "str", "number", "str", "number", "str"],
        )

    botao.click(
        fn=cadastrar_paciente,
        inputs=[nome, idade, convenio, prioridade, motivo],
        outputs=[saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()