import subprocess
import sys

def update_pip():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

def install_package(package):
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "show", package])
    except subprocess.CalledProcessError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

update_pip()
required_packages = ["openai", "gradio"] # 설치할 패키지 이름
for package in required_packages:
    install_package(package)
    
import openai
import gradio

openai.api_key = "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"

# start_sequence = "\nAI: "  # 
# restart_sequence = "\nHuman: " # 

# # 프롬프트  , fine튜닝?

# prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "


start_sequence = "\nAI: "
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "


def openai_create(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return response.choices[0].text


def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    print(input, output, history)
    return history, history


block = gradio.Blocks()


with block:
    gradio.Markdown("""<h1><center>나만의 GPT 챗봇</center></h1>""")
    chatbot = gradio.Chatbot()
    message = gradio.Textbox(placeholder=prompt)
    state = gradio.State()
    submit = gradio.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])


block.launch(debug=True)

# block.launch(share=True)
