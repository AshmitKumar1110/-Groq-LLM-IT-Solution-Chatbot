!pip install gradio requests --quiet



# 2. Prompt for API key (secure input)

GROQ_API_KEY = ('Enter Your API KEY')

# 3. Define chat function
import requests
import gradio as gr

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"  # You can change to another Groq-supported model

def groq_chat(messages, user_input):
    # Compose the message history for context
    chat_messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for m in messages:
        chat_messages.append({"role": "user", "content": m[0]})
        chat_messages.append({"role": "assistant", "content": m[1]})
    chat_messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": chat_messages,
        "temperature": 0.7
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# 4. Gradio chat interface
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Groq LLM IT Solution Chatbot\nChat with a blazing-fast LLM via Groq API!")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your message")
    state = gr.State([])

    def respond(user_message, chat_history):
        bot_message = groq_chat(chat_history, user_message)
        chat_history = chat_history + [[user_message, bot_message]]
        return chat_history, chat_history

    msg.submit(respond, [msg, state], [chatbot, state])
    msg.submit(lambda: "", None, msg)  # Clear textbox after submit

# ... (rest of your code)

demo.launch(debug=True, share=True) # Set debug and share options
