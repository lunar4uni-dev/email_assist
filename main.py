import gradio as gr
from google import genai


def generate(texts, key):
    client = genai.Client()
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
    api_key=key
    )
    print(response.text)
    pass


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
- if sender name unknown use "000 드림"

Return ONLY the corrected email.
Do not include explanations.
"""


with gr.Blocks() as demo:
    email_text = gr.Textbox(label="Input Email Here")
    email_config = gr.Textbox(label="Email Instruction (fixable)", value=email_instruction, visible=True)
    output = gr.Textbox(label="Output Box")
    gemini_api_key = gr.Textbox(label="Gemini API Key", type="password")
    generate_btn = gr.Button("Fix as Instruction")
    generate_btn.click(fn=generate, inputs=(email_text, gemini_api_key), outputs=output, api_name="generate")

demo.launch()