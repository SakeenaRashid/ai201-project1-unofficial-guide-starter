import gradio as gr
from query import ask


def answer_question(question):
    result = ask(question)
    sources_text = "\n".join(result["sources"])
    return result["answer"], sources_text


with gr.Blocks() as demo:
    gr.Markdown("## UMich Professor Review Assistant")
    question = gr.Textbox(label="Ask about a UMich professor")
    btn = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Sources", lines=4)

    btn.click(fn=answer_question, inputs=question, outputs=[answer, sources])
    question.submit(fn=answer_question, inputs=question, outputs=[answer, sources])

demo.launch()
