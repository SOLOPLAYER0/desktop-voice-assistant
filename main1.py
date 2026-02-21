import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3
import speech_recognition as sr
import psutil
import wikipedia
import re 
import requests
from bs4 import BeautifulSoup
import torch
from transformers import pipeline
from googlesearch import search
from app import ask








def setup_voice_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   # female voice
    engine.setProperty('rate', engine.getProperty('rate') - 50)
    engine.setProperty('volume', engine.getProperty('volume') + 0.25)
    return engine


def speak(text):
    engine = setup_voice_engine()
    engine.say(text)
    engine.runAndWait()


# ------------------ Speech Recognition ------------------
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...", end="", flush=True)

        recognizer.pause_threshold = 1.0
        recognizer.phrase_threshold = 0.3
        recognizer.sample_rate = 48000
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 4000
        recognizer.phrase_time_limit = 10

        audio = recognizer.listen(source)

    try:
        print("\rRecognizing...", end="", flush=True)
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"\rUser said: {query}\n")
    except Exception:
        print("Could not understand, please say again.")
        return "None"
    return query


# ------------------ Helper Functions ------------------
def get_today():
    day_number = datetime.datetime.today().weekday() + 1
    days = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    return days.get(day_number, "Unknown")


def greet_user():
    speak("Hi, I’m Alice. Here to be your personal voice assistant.")
    hour = int(datetime.datetime.now().hour)
    current_time = time.strftime("%I:%M:%p")
    day = get_today()

    if 0 <= hour < 12 and "AM" in current_time:
        speak(f"Good morning! It's {day}, {current_time}")
    elif 12 <= hour <= 16 and "PM" in current_time:
        speak(f"Good afternoon! It's {day}, {current_time}")
    else:
        speak(f"Good evening! It's {day}, {current_time}")


# ------------------ Core Actions ------------------
def open_social_media(query):
    if 'facebook' in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in query:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in query:
        speak("Opening Discord")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in query:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("Sorry, I couldn't find that.")


def launch_application(query):
    if "calculator" in query:
        speak("Opening Calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in query:
        speak("Opening Notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in query:
        speak("Opening Paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')


def close_application(query):
    if "calculator" in query:
        speak("Closing Calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in query:
        speak("Closing Notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in query:
        speak("Closing Paint")
        os.system('taskkill /f /im mspaint.exe')


def search_browser(query):
    if 'google' in query:
        speak("What should I search on Google?")
        search_text = listen_command().lower()
        webbrowser.open(f"https://www.google.com/search?q={search_text}")



def system_status():
    cpu_usage = psutil.cpu_percent()
    battery = psutil.sensors_battery()

    speak(f"CPU usage is {cpu_usage} percent")
    speak(f"Battery is at {battery.percent} percent")

    if battery.percent >= 80:
        speak("Plenty of charge available.")
    elif 40 <= battery.percent < 80:
        speak("We should plug in soon to charge.")
    else:
        speak("Battery is very low, please connect to a charger!")


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', '', text)
    return text.strip()

def summarize_text(text, max_sentences=3, max_chars=300):
    """
    Produce a short 2–3 sentence summary.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 6]

    if not sentences:
        return "No meaningful content found."


    summary = ' '.join(sentences[:max_sentences])

    if len(summary) > max_chars:
        summary = summary[:max_chars].rsplit('.', 1)[0] + '.'

    return summary


def wikipedia_search_summary(query):
    print(f"Searching Wikipedia for '{query}'...")

    try:
        raw = wikipedia.summary(query, sentences=6)

        cleaned = clean_text(raw)
        result = summarize_text(cleaned, max_sentences=3, max_chars=300)

        return result

    except wikipedia.DisambiguationError as e:
        return f" Multiple meanings found for '{query}'. Try one of: {e.options[:5]}"

    except wikipedia.PageError:
        return f" No Wikipedia page found for '{query}'."

    except Exception as e:
        return f" Error occurred: {str(e)}"




WAKE_WORDS = ["tren", "wake up"]

def detect_wake_word(text):
    text = text.lower()
    return any(wake_word in text for wake_word in WAKE_WORDS)




# ------------------ Main ------------------

if __name__ == "__main__":
    greet_user()
    print("started")

    awake = False          # Sleep mode initially
    empty_count = 0        # Count silent attempts

    while True:
        query = listen_command().lower()

        # -------------------- WAKE WORD DETECTION --------------------
        if not awake:
            if detect_wake_word(query):
                speak("I am listening.")
                awake = True
                empty_count = 0   # Reset silence count
            continue
        # -------------------------------------------------------------

        # -------------------- HANDLE SILENCE (ONE-TIME ONLY) --------------------
        if query == "none" or query.strip() == "":
            empty_count += 1

            if empty_count >= 1:
                speak("Going back to sleep.")
                awake = False
                empty_count = 0
            continue
        else:
            empty_count = 0
        # -------------------------------------------------------------

        # -------------------- CORE COMMAND HANDLING --------------------
        if any(x in query for x in ["facebook", "discord", "whatsapp", "instagram"]):
            open_social_media(query)

        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")

        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decreased")

        elif ("volume mute" in query) or ("mute" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")

        elif "open" in query:
            launch_application(query)

        elif "close" in query:
            close_application(query)

        elif "google" in query:
            search_browser(query)

        elif "system condition" in query or "system status" in query:
            system_status()

        elif "exit" in query or "quit" in query:
            speak("Goodbye Sir! Have a great day.")
            sys.exit()


        elif "wake up" in query or "wake" in query:

            continue

        elif "wikipedia" in query:
            summary = wikipedia_search_summary(query)
            speak(summary)

        else:
            answer = ask(query)
            speak(answer)
            # DO NOT SLEEP HERE 


