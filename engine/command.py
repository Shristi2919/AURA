import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


@eel.expose
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        return ""

    return query.lower()




@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    print("RAW QUERY:", query)

    try:
        query = query.lower().strip()
        query = query.replace("jarvis", "")
        query = query.replace("aura", "")
        print("PROCESSED QUERY:", query)

        # ── Open apps ────────────────────────────────────────────────────
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        # ── Play YouTube ──────────────────────────────────────────────────
        elif "on youtube" in query or "play" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        # ── Calls and messages (WhatsApp or Mobile) ───────────────────────
        # Catches: "send message", "send a message", "send sms", "call", "phone call", "video call"
        elif ("send" in query and "message" in query) or "send sms" in query or "call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)

            if contact_no != 0:
                speak("Which mode do you want to use, WhatsApp or mobile?")
                preference = takecommand()
                print("Preference:", preference)

                # ── Mobile call / SMS ─────────────────────────────────
                if "mobile" in preference:
                    if "send" in query and "message" in query or "send sms" in query:
                        speak("What message should I send?")
                        message_text = takecommand()
                        sendMessage(message_text, contact_no, name)
                    elif "call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again")

                # ── WhatsApp ──────────────────────────────────────────
                elif "whatsapp" in preference:
                    if "send" in query and "message" in query:
                        speak("What message should I send?")
                        message_text = takecommand()
                        whatsApp(contact_no, message_text, "message", name)
                    elif "video call" in query:
                        whatsApp(contact_no, "", "video call", name)
                    elif "call" in query:
                        whatsApp(contact_no, "", "voice call", name)
                    else:
                        speak("Please try again")

                else:
                    speak("I did not understand. Please say WhatsApp or mobile.")

        # ── Fallback: Gemini chatbot ──────────────────────────────────────
        else:
            from engine.features import geminai
            geminai(query)

    except Exception as e:
        print("Error in allCommands:", e)

    eel.ShowHood()