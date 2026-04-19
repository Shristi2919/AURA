import os
import eel
import threading
import subprocess
from engine.features import hotword, playAssistantSound
from engine.command import *
from engine.auth import recognize


def open_edge():
    import time
    time.sleep(2)
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')


def run_auth():
    import time
    time.sleep(4)  # wait for Edge to fully load the page

    # Step 1 — hide loader, show face scan lottie
    eel.DisplayMessage("Ready for Face Authentication...")
    eel.hideLoader()
    speak("Ready for Face Authentication")

    # Step 2 — run face auth
    flag = 0
    try:
        result = recognize.AuthenticateFace()
        if result is not None:
            flag = result
    except Exception as e:
        print(f"⚠️ Face auth error: {e}")
        flag = 0

    print(f"🔍 Auth flag = {flag}")

    if flag == 1:
        print("✅ Access Granted")

        # Step 3 — hide face scan, show success lottie
        eel.DisplayMessage("Face Authentication Successful ✅")
        eel.hideFaceAuth()
        speak("Face Authentication Successful")

        # Step 4 — hide success, show greeting lottie
        eel.DisplayMessage("Hello, Welcome!")
        eel.DisplayMessage("AURA ACTIVATED")
        eel.hideFaceAuthSuccess()
        speak("Hello, Welcome, How can I Help You")
        speak("AURA ACTIVATED")
        

        # Step 5 — hide init screen, show chat UI
        eel.hideStart()
        playAssistantSound()

    else:
        print("❌ Access Denied")
        eel.DisplayMessage("Access Denied ❌ Please Try Again")
        speak("Face Authentication Failed")


@eel.expose
def isReady():
    return True


def start():
    eel.init("www")

    subprocess.Popen([r'devices.bat'], shell=True)
    threading.Thread(target=hotword, daemon=True).start()

    threading.Thread(target=open_edge, daemon=True).start()
    threading.Thread(target=run_auth, daemon=True).start()

    eel.start(
        'index.html',
        mode=None,
        host='localhost',
        port=8000,
        block=True
    )