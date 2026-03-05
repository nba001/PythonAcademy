import ollama
from ollama import chat
from ollama import ChatResponse

# Set the host URL to match your custom port
ollama.api_base = 'http://localhost:11434'

response: ChatResponse = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role": "system",
            "content": "You are an expert translator, you read a phrase and return a VALID JSON format with a 'language' key and value with the main language it is written. Example: 'Hi' -> {'language':'English',} 'Hola' -> {'language':'Spanish'}" 
        },

        {
            "role": "user",
            "content":  "Jukka poikka."
        }

    ],
    options={
        "temperature":0.2
    })

response1: ChatResponse = chat(
    model="qwen2.5:3b",
    messages=[
        {
            "role" : "system",
            "content": "You are a helpful AI assistent"
        },
        {
            'role': "user",
            "content":"What is the capital of USA."
        }
    ],
    options={
        "temperature":1
    }
)

print(response.message.content)
print(response1.message.content)