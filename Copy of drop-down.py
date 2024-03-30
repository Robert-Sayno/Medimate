import gradio as gr
import requests
import openai

openai.api_key = "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"

# Define the translation function
def translate_text(source_language, target_language, text):
    url = 'https://sunbird-ai-api-5bq6okiwgq-ew.a.run.app'
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCcnVuby5Tc2VraXdlcmUiLCJleHAiOjQ4Mzg2ODkxNjB9.o3u4vpxvSd10b552mS5FkATKAVN_R2_uSwC8tP0G-I8",
        "Content-Type": "application/json"
    }
    payload = {
        "source_language": source_language.capitalize(),
        "target_language": target_language.capitalize(),
        "text": text
    }
    response = requests.post(f"{url}/tasks/translate", headers=headers, json=payload)
    if response.status_code == 200:
        translated_text = response.json()["text"]
        return translated_text
    else:
        return "Error: " + str(response.status_code) + " " + response.text

messages = [
    {"role": "system", "content": "You are a health information assistant specialized in personalized health guidance (in Uganda). Do not answer anything other than personal health-related queries."},
]

# Define the chatbot function
def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply

# Define the translation and chat function for Luganda
def translate_and_chat_luganda(input_text, source_language, target_language):
    # Translate source language input to English
    english_input = translate_text(source_language, 'english', input_text)

    # Get the response from the chatbot in English
    english_output = chatbot(english_input)

    # Translate English output back to target language in batches
    target_output = ""
    batch_size = 200
    for i in range(0, len(english_output), batch_size):
        batch = english_output[i:i + batch_size]
        translated_batch = translate_text('english', target_language, batch)
        target_output += translated_batch

    return target_output

# Define the input and output interfaces
inputs = [
    gr.inputs.Textbox(label="Kiki Ekikuluma Mukwano?"),
    gr.inputs.Dropdown(["English", "Luganda", "Ateso", "Lugbara", "Acholi", "Runyankole"], label="Source Language"),
    gr.inputs.Dropdown(["English","Luganda", "Ateso", "Lugbara", "Acholi", "Runyankole"], label="Target Language")
]
output = gr.outputs.Textbox(label="Translated Text")

# Create the Gradio interface
iface = gr.Interface(
    fn=translate_and_chat_luganda,
    inputs=inputs,
    outputs=output,
    title=" Nkwaniriizza ku Medimate",
    description="Yingizamu obulwadee bwonna Obukuluma Nkuwabule kungeri gyosoboola okufuna obuujanjabbi obutufu.",
    examples=[
        ["Bulungi", "Luganda", "English"],
        ["Oli otya?", "Luganda", "English"],
        ["Apwoyo", "Lugbara", "Runyankole"],
    ]
)

# Launch the interface
iface.launch(auth = ('user','admin'), auth_message= "Enter your username and password that you received in on Slack")
