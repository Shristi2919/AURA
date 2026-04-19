from shlex import quote
import struct
import subprocess
import time

import webbrowser

from playsound import playsound
import threading
import eel
import os

import pvporcupine
import pyaudio
import pyautogui
import pyperclip
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import re
import sqlite3

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

# ADB path — used for all phone automation
ADB = r'C:\platform-tools\adb.exe'


@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\futuristic-transition-390304.mp3"
    threading.Thread(target=playsound, args=(music_dir,), daemon=True).start()


@eel.expose
def playMicSound():
    mic_sound = "www\\assets\\audio\\ui-sound-374228.mp3"
    threading.Thread(target=playsound, args=(mic_sound,), daemon=True).start()


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.strip().lower()

    if query != "":
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "AURA.db")

        try:
            con = sqlite3.connect(db_path)
            cursor = con.cursor()

            cursor.execute("SELECT path FROM sys_command WHERE name=?", (query,))
            result = cursor.fetchone()

            if result:
                path = result[0]
                speak("Opening " + query)
                if path.endswith(":"):
                    os.system(f"start {path}")
                else:
                    os.startfile(path)

            else:
                cursor.execute("SELECT url FROM web_command WHERE name=?", (query,))
                result = cursor.fetchone()

                if result:
                    speak("Opening " + query)
                    webbrowser.open(result[0])

                elif query == "youtube":
                    speak("Opening YouTube")
                    webbrowser.open("https://www.youtube.com")

                elif query == "whatsapp":
                    speak("Opening WhatsApp")
                    os.system("start whatsapp:")

                else:
                    try:
                        speak("Opening " + query)
                        os.system(f"start {query}")
                    except:
                        speak("Application not found")

            con.close()

        except Exception as e:
            print("Error in openCommand:", e)
            speak("Something went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if not search_term:
        speak("What should I play on YouTube?")
        return
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["computer", "jarvis", "hey google", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("hotword detected")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("a")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print("HOTWORD ERROR:", e)


def findContact(query):
    words_to_remove = [ASSISTANT_NAME.lower(), 'make', 'a', 'to', 'phone',
                       'call', 'send', 'message', 'whatsapp', 'video', 'voice', 'on', 'please']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        print("findContact: searching for →", query)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(BASE_DIR, "AURA.db")

        con = sqlite3.connect(db_path)
        cursor = con.cursor()

        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
            ('%' + query + '%', query + '%')
        )

        result = cursor.fetchone()
        con.close()

        if result:
            mobile_number_str = str(result[0]).replace(" ", "")
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str
            print("findContact: found →", mobile_number_str)
            return mobile_number_str, query

        else:
            print("findContact: no contact found for →", query)
            speak("Contact not found")
            return 0, 0

    except Exception as e:
        print("CONTACT ERROR:", e)
        speak("Contact not found")
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    try:
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"
        subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
        print(f"whatsApp: opening chat for {name} ({mobile_no})")

        time.sleep(10)

        if flag == "message":
            pyperclip.copy(message)
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)
            pyautogui.press("enter")
            speak("Message sent to " + name)

        elif flag == "voice call":
            speak("Calling " + name)
            for i in range(9):
                pyautogui.press("tab")
                time.sleep(0.2)
            pyautogui.press("enter")
            time.sleep(1)
            for i in range(5):
                pyautogui.press("tab")
                time.sleep(0.2)
            pyautogui.press("enter")

        elif flag == "video call":
            speak("Starting video call with " + name)
            for i in range(9):
                pyautogui.press("tab")
                time.sleep(0.2)
            pyautogui.press("enter")
            time.sleep(1)
            for i in range(4):
                pyautogui.press("tab")
                time.sleep(0.2)
            pyautogui.press("enter")

    except Exception as e:
        print("WHATSAPP ERROR:", e)
        speak("Something went wrong with WhatsApp")


def chatBot(query):
    user_input = query.lower()
    cookie_path = os.path.join("engine", "cookies.json")
    chatbot = hugchat.ChatBot(cookie_path=cookie_path)
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response


def geminai(query):
    """Fallback AI chatbot using HugChat"""
    try:
        user_input = query.lower()
        cookie_path = os.path.join("engine", "cookies.json")
        chatbot = hugchat.ChatBot(cookie_path=cookie_path)
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print("geminai response:", response)
        speak(response)
        return response
    except Exception as e:
        print("GEMINAI ERROR:", e)
        speak("Sorry, I could not process that")


# ── Android Automation ────────────────────────────────────────────────────────

def makeCall(name, mobileNo):
    """Make a real phone call via ADB"""
    try:
        mobileNo = str(mobileNo).replace(" ", "")
        speak("Calling " + name)
        subprocess.run(
            [ADB, 'shell', 'am', 'start',
             '-a', 'android.intent.action.CALL',
             '-d', f'tel:{mobileNo}'],
            shell=True
        )
        print(f"makeCall: calling {name} at {mobileNo}")
    except Exception as e:
        print("MAKE CALL ERROR:", e)
        speak("Sorry, could not make the call")


def sendMessage(message, mobileNo, name):
    """Send SMS via ADB using screen taps — uses helper functions"""
    try:
        from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput

        # Format message and number for ADB input
        message = replace_spaces_with_percent_s(message)
        mobileNo = replace_spaces_with_percent_s(mobileNo)

        speak("Sending message")

        goback(4)           # go back to home screen
        time.sleep(1)

        keyEvent(3)         # press Home key

        tapEvents(392, 1989)  # open SMS app icon
        time.sleep(1)

        tapEvents(791, 2205)  # tap Start Chat / New Message button
        time.sleep(1)

        adbInput(mobileNo)    # type mobile number in search
        time.sleep(1)

        tapEvents(136, 561)   # tap on contact name from suggestions
        time.sleep(1)

        tapEvents(204, 1415)  # tap on message input box
        time.sleep(0.5)

        adbInput(message)     # type the message
        time.sleep(0.5)

        tapEvents(965, 1423)  # tap Send button

        speak("Message sent successfully to " + name)
        print(f"sendMessage: sent '{message}' to {name} at {mobileNo}")

    except Exception as e:
        print("SEND MESSAGE ERROR:", e)
        speak("Sorry, could not send the message")