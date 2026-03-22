import gradio as gr
from google import genai


def generate(texts, key, config):
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=config + "\n\n----------\nEmail Texts you should modify:\n" + texts,
    )
    print(response.text)
    return response.text


with open('prompts/email_prompt_v001.md', 'r', encoding='utf-8') as f:
    md_text = f.read()
email_instruction = md_text


with gr.Blocks() as demo:
    gr.HTML("""<h1 class="heading-display hero-title">Email Modifier 이메일 수정 도구</h1>"""
            """<p class="text-body hero-description">Developed by <a href='https://github.com/lunar4uni-dev' target='_blank'>Seungwoo (lunar4uni-dev)</a></p>""")
    email_config = gr.Textbox(label="Email Instruction 이메일 작성 규칙", value=email_instruction, visible=True, lines=5)
    email_text = gr.Textbox(label="Input Draft Email 이메일 초안 입력", lines=2)
    gemini_api_key = gr.Textbox(label="Insert Gemini API Key", type="password")
    generate_btn = gr.Button("Modify Email 이메일 수정")
    output = gr.Textbox(label="Output Email 생성된 이메일", lines=2)
    generate_btn.click(fn=generate, inputs=(email_text, gemini_api_key, email_config), outputs=output, api_name="generate")


demo.launch(share=True)