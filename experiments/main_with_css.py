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


custom_css = """
@import url(https://fonts.googleapis.com/css?family=Lato:400,700,900,300);
@import url(http://weloveiconfonts.com/api/?family=fontawesome);

h1 { font-size: 32px; margin-bottom: 50px;}
p { margin: 15px 0; line-height: 24px; color: gainsboro; }

h1.second {
  font-weight: 200;
}

h1.second span {
  position: relative;
  display: inline-block;
  padding: 5px 10px ;
  border-radius: 10px;
  border-bottom: 1px solid mediumseagreen;
}

h1.second span:after {
  content: '';
  position: absolute;
  bottom: calc(-100% - 1px);
  margin-left: -10px;
  display: block;
  width: 100%; height: 100%;
  border-radius: 10px;
  border-top: 1px solid mediumseagreen;
}


p.fourth { 
  font-weight: 700;
}

p.fourth span {
  border-bottom: 1px solid transparent;
  transition: all 0.2s ease;
}

p.fourth:hover span {
  border-bottom: 1px solid whitesmoke;
}

p.fourth span:first-child {
  font-weight: 300;
}


"""

# with open('css_styles/templatemo-maison-style.css', 'r') as file:
#     custom_css += file.read()


with gr.Blocks() as demo:
    # gr.HTML("""<h1 class="heading-display hero-title">Email Modifier 이메일 수정 도구</h1>"""
    #         """<p class="text-body hero-description">Developed by <a href='https://github.com/lunar4uni-dev' target='_blank'>Seungwoo (lunar4uni-dev)</a></p>""")
    gr.HTML("""<h1 class="second">Email Modifier 이메일 수정 도구</h1>"""
        """<p class="fourth">Developed by <a href='https://github.com/lunar4uni-dev' target='_blank'>Seungwoo (lunar4uni-dev)</a></p>""")
    email_config = gr.Textbox(label="Email Instruction 이메일 작성 규칙", value=email_instruction, visible=True, lines=5)
    email_text = gr.Textbox(label="Input Draft Email 이메일 초안 입력", lines=2)
    gemini_api_key = gr.Textbox(label="Insert Gemini API Key", type="password")
    generate_btn = gr.Button("Modify Email 이메일 수정")
    output = gr.Textbox(label="Output Email 생성된 이메일", lines=2)
    generate_btn.click(fn=generate, inputs=(email_text, gemini_api_key, email_config), outputs=output, api_name="generate")


# demo.launch(share=True, css_paths="css_styles/templatemo-maison-style.css")
demo.launch(share=True, css=custom_css)