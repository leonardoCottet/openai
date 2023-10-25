import openai

openai.api_key = "sua_api"


def conversar(texto):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Suponha que você é um instrutor de Python."},
            {"role": "user", "content": texto},
        ],
        temperature=0.7,
    )
    return resposta['choices'][0]['message']['content']


while True:
    prompt = input("Usuário: ")
    resposta_chatgpt = conversar(prompt)
    print("Bot: " + resposta_chatgpt)
