import openai
from vosk import Model, KaldiRecognizer
import pyaudio
from gtts import gTTS
import pygame
from io import BytesIO

openai.api_key = "sua_api"
pygame.init()

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

def text_to_speech(text):
    tts = gTTS(text=text, lang='pt') 
    audio_file = BytesIO()
    tts.save(audio_file)
    audio_file.seek(0)
    return audio_file

def ouvir():
    model = Model("caminho_para_modelo_vosk")
    recognizer = KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)

    print("Fale algo:")
    stream.start_stream()
    try:
        while True:
            data = stream.read(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                return result['text']
    except KeyboardInterrupt:
        pass
    finally:
        print("Parando a gravação...")
        stream.stop_stream()
        stream.close()
        p.terminate()

    return ""

while True:
    prompt = ouvir()
    if prompt:
        resposta_chatgpt = conversar(prompt)
        print("Bot: " + resposta_chatgpt)

        audio_file = text_to_speech(resposta_chatgpt)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        pygame.time.wait(int(pygame.mixer.music.get_length() * 1000))
