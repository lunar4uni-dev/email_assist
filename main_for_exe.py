import gradio as gr
from google import genai


email_instruction = """
You are an expert Korean email etiquette assistant.

Your task is to rewrite email drafts so they follow proper formal Korean email structure used in universities or professional communication.

Goals:
- preserve original meaning
- improve politeness and clarity
- correct grammar, spacing, punctuation, and typos
- enforce proper email structure

Never invent new information.

Always output a fully formatted email.

Email structure must follow this format:

제목: <short summary>

수신자 호칭

인사 및 자기소개

메일 목적 설명

본문 (1~3 paragraphs, each paragraph ≥2 sentences)

마무리 인사

이름 + 올림/드림

Formatting rules:
- paragraph break only when starting new paragraph
- leave one blank line between paragraphs
- do not break sentences into separate lines
- closing greeting should be its own paragraph

Writing rules:
- use polite formal Korean
- fix grammar errors
- correct spacing
- correct punctuation
- avoid overly casual language

If information is missing:
- infer reasonably
- if sender name unknown use "000 올림"

Return ONLY the corrected email.
Do not include explanations.
"""


def generate(texts, key, config):
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=config + "\n\n----------\nEmail Texts you should modify:\n" + texts,
    )
    print(response.text)
    return response.text


with gr.Blocks() as demo:
    gr.HTML("""<h1 class="heading-display hero-title">Email Modifier 이메일 수정 도구</h1>"""
            """<p class="text-body hero-description">Developed by <a href='https://github.com/lunar4uni-dev' target='_blank'>Seungwoo (lunar4uni-dev)</a></p>""")
    email_config = gr.Textbox(label="Email Instruction 이메일 작성 규칙", value=email_instruction, visible=True, lines=5)
    email_text = gr.Textbox(label="Input Draft Email 이메일 초안 입력", lines=2)
    gemini_api_key = gr.Textbox(label="Insert Gemini API Key", type="password")
    generate_btn = gr.Button("Modify Email 이메일 수정")
    output = gr.Textbox(label="Output Email 생성된 이메일", lines=2)
    generate_btn.click(fn=generate, inputs=(email_text, gemini_api_key, email_config), outputs=output, api_name="generate")


demo.launch(share=False)