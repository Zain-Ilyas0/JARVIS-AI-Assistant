

import warnings

warnings.filterwarnings("ignore")
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
from google import genai
from geminiconfig import apikey
import random





def ai(prompt):
    client = genai.Client(api_key=apikey)
    text = f"open ai respnse for prompt: {prompt} \n ***************\n\n"

    chat = client.chats.create(
    model="gemini-3.8-flash"
)
    try:
        response = chat.send_message(prompt)

        print(response.text)
        text += response.text
        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        # with open(f"Openai/prompt - {random.randint(1, 12345)}.txt", "w") as f:
        # with open(f"Openai/{prompt[0:30]}.txt", "w") as f:
        filename = prompt.split("AI", 1)[1].strip()

        with open(f"Openai/{filename}.txt", "w") as f:
    
            f.write(text)
    except Exception as e:
        print("Google Gemini Server is Busy")
        print("Try Again in a Few minutes")


client = genai.Client(api_key=apikey)
chat_session = client.chats.create(model="gemini-3.8-flash")
def chat(query):
    """Conversation mode: remembers history, speaks, and returns the reply."""
    try:
        response = chat_session.send_message(query)
        reply = response.text
        print(reply)
        say(reply)       # your text-to-speech function from the tutorial
        return reply
    except Exception as e:
        print("Error:", e)
        return "Sorry, something went wrong."






def say(text):
    # Create a fresh engine each time so speech keeps working in a loop
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language="en-IN")
        print(f"user said: {query}")
        return query.lower()
    except Exception:
        print("Could not understand, try again")
        return ""


if __name__ == '__main__':
    say("Hello! I am Jarvis! What do you want to ask?")

    sites = [
        ["youtube", "https://youtube.com"],
        ["wikipedia", "https://wikipedia.com"],
        ["google", "https://google.com"],
    ]
    musicPath = r"music_path"

    while True:
        print("Listening...")
        query = takeCommand()
        if not query:
            continue

        opened = False
        for name, url in sites:
            if f"open {name}" in query:
                say(f"Opening {name} Sir...")
                webbrowser.open(url)
                opened = True
                break

        if opened:
            continue

        if "open music" in query:
            say("Playing music Sir...")
            os.startfile(musicPath)

        elif "the time" in query:
            strfTime = datetime.datetime.now().strftime("%I:%M %p")
            print(f"Sir, the time is {strfTime}")
            say(f"Sir, the time is {strfTime}")

        elif "break" in query or "stop" in query:
            say("Goodbye Sir")
            break

        elif "open calculator" in query.lower():
            os.system("start calc")

        elif "open camera" in query.lower():
            os.system("start ms-camera:")

        elif "Using AI".lower() in query.lower():
            ai(prompt=query)
        elif "reset chat" in query.lower():
            chat_session = client.chats.create(model="gemini-3.8-flash")
            say("Chat reset done")
            print("Chat reset done")
        else:
            chat(query)
