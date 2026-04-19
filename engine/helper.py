import re
import os
import subprocess
import time

# ADB path
ADB = r'C:\platform-tools\adb.exe'


def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    words = input_string.split()
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    result_string = ' '.join(filtered_words)
    return result_string


# ── ADB Helper Functions ──────────────────────────────────────────────────────

def replace_spaces_with_percent_s(text):
    """Replace spaces with %s so ADB input can handle multi-word strings"""
    return str(text).replace(" ", "%s")


def goback(steps):
    """Press the back button N times on the phone"""
    for i in range(steps):
        subprocess.run([ADB, 'shell', 'input', 'keyevent', '4'], shell=True)
        time.sleep(0.5)


def keyEvent(event_code):
    """Send a keyevent to the phone
    Common codes: 3 = Home, 4 = Back, 26 = Power, 82 = Menu
    """
    subprocess.run([ADB, 'shell', 'input', 'keyevent', str(event_code)], shell=True)
    time.sleep(0.5)


def tapEvents(x, y):
    """Tap on screen at coordinates (x, y)"""
    subprocess.run([ADB, 'shell', 'input', 'tap', str(x), str(y)], shell=True)
    time.sleep(0.5)


def adbInput(text):
    """Type text on the phone via ADB (spaces must be replaced with %s first)"""
    subprocess.run([ADB, 'shell', 'input', 'text', str(text)], shell=True)
    time.sleep(0.5)