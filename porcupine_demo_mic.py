failsafe_check = 0
#ReDesign AI2
# Copyright 2018-2023 Picovoice Inc.
#
# You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
# file accompanying this source.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

import argparse
import os
import random
import struct
import sys
import threading
import wave
from datetime import datetime
import requests
import pvporcupine
import datetime
import speech_recognition as sr
import concurrent.futures
import pyttsx3
import webbrowser
import subprocess
speech = sr.Recognizer()
import time
import re
import pyautogui as pyautogui
import pywhatkit as kit
import ctypes
import os
from pvrecorder import PvRecorder
import feedparser
from tkinter import *
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from PyDictionary import PyDictionary
from playsound import playsound
import win32gui, win32con

speech = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('voice','HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')
rate = engine.getProperty('rate')
rate = rate-20
engine.setProperty('rate', rate)
engine.runAndWait() 
vnote =''

def news():
    index_number = 0

    def parseRSS(rss_url):
        return feedparser.parse(rss_url)

    def getHeadlines(rss_url):
        headlines = []
        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            headlines.append(newsitem['title'])
        return headlines

    allheadlines = []
    newsurls = {'googlenews': 'https://news.google.com/news/rss/?hl=en&amp;ned=us&amp;gl=IN', }
    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))
    speak('Sir, today news headlines are:')
    if not allheadlines:
        speak('Sorry, sir, unable to fetch news. As the internet and I are not connected.')
    for hl in allheadlines[:10]:  # Print only the top 10 headlines
        index_number = index_number + 1
        hll = str(hl).replace(' -', ', from')
        speak('Number ' + str(index_number) + '. ' + hll)

def is_computer_locked():
    # Define constants
    user32 = ctypes.windll.User32

    # Get the handle of the foreground window
    foreground_window = user32.GetForegroundWindow()

    # Check if the foreground window is the lock screen
    # The lock screen window class name is usually "Windows.UI.Core.CoreWindow"
    class_name_length = 256
    class_name = ctypes.create_unicode_buffer(class_name_length)
    user32.GetClassNameW(foreground_window, class_name, class_name_length)

    return class_name.value == "Windows.UI.Core.CoreWindow"

def play_first_youtube_video(query):
    pyautogui.hotkey('playpause')
    kit.playonyt(query)
def speak(cmd):
    engine.say(cmd)
    print("System :", cmd)
    engine.runAndWait()
    log_request_response(vnote, cmd)


def get_default_audio_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    ).QueryInterface(IAudioEndpointVolume)
    return interface

# Function to set the volume
def set_volume_system(interface, volume):
    interface.SetMasterVolumeLevelScalar(volume, None)

# Function to get the current volume
def get_current_volume(interface):
    return interface.GetMasterVolumeLevelScalar()

# Get the default audio endpoint volume interface
audio_interface = get_default_audio_interface()


    

audcheck = 0  # Declare audcheck as a global variable
listen_time = 0 
def rec_voice():
    global audcheck
    global listen_time
    if listen_time > 0:
        playsound("C:\\users\\mashu\\start.mp3")

    original_volume = get_current_volume(audio_interface)
    set_volume_system(audio_interface, 0.1)

    with sr.Microphone() as source:
        print('Listening...')
        try:
            audio = speech.listen(source=source, timeout=5, phrase_time_limit=3)
        except sr.WaitTimeoutError as e:
            print("Timeout; {0}".format(e))
            return ''

    voice_text = ''
    try:
        print("Recognizing...")
        voice_text = speech.recognize_google(audio, language='en-in')
    except sr.UnknownValueError:
        audcheck += 1
        pass
    except sr.RequestError:
        print("Network error")

    if not voice_text:
        print("Sorry, my system doesn't detect any voice command")
        listen_time += 1
        if audcheck == 1:
            set_volume_system(audio_interface, original_volume)
            playsound("C:\\users\\mashu\\stop.mp3")
            print(':: Waiting for wakeword detection ::')
            listen_time = 0
            # Add code for playing stop sound or any other action

    set_volume_system(audio_interface, original_volume)

    if voice_text:
        print('You said:', voice_text)
        audcheck = 0
        listen_time += 1

    return voice_text



## Volume Control#############

log_file_path = "C:/Users/mashu/log.txt"

# Function to write to the log file
def log_request_response(request, response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - Request: {request} | Response: {response}\n"
    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry)

        
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBoardInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time",ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBoardInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def key_down(keyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput(keyCode, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(1), ii_ )
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def key_up(keyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput(keyCode, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBoardInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def key(key_code, length = 0):
    key_down(key_code)
    time.sleep(length)
    key_up(key_code)


def volume_up():
    key(VK_VOLUME_UP)


def volume_down():
    key(VK_VOLUME_DOWN)

def set_volume(int):
    for _ in range(0, 50):
        volume_down()
    for _ in range(int // 2):
        volume_up()
def mute():
    key(VK_VOLUME_MUTE)
def myKey(value):
    PressKey(value)
    ReleaseKey(value)
# # # # # # # # # # # # # # # # # # # # # # # 
def reader():
    pyautogui.hotkey('ctrl', 'c')
    os.popen('start C:\\Users\\mashu\\rd.txt')
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('ctrl', 's')
    pyautogui.hotkey('alt', 'f4')
    file_path = 'C:\\Users\\mashu\\rd.txt'
    with open(file_path) as inp:
        data = str(inp.read().splitlines())
    speak('The selected text is -' + data)
    speak("That's All")
def word_filter(voice_note) :
        def Convert(string):
            li = list(string.split(" "))
            return li
        check_word=Convert(voice_note)
        final = str(check_word[0]+' '+check_word[1]+' '+check_word[2])
        if 'here'in final:
            voice_note = voice_note.replace('here ','',1)
        if 'write' in final:
            voice_note = voice_note.replace('write ','',1)
        if 'type' in final:
            voice_note = voice_note.replace('type ','',1)
        if 'right' in final:
            voice_note = voice_note.replace('right ','',1)
        final_word = str(voice_note)
        pyautogui.write(final_word)
def no_there(voice_note):
    return any(i.isdigit() for i in voice_note)

def dictionary(cmd):
    cmd_1 = cmd.split()
    target_words = ['word', 'of', 'meaning', 'means', 'mean']

    target = next((word for word in cmd_1 if word in target_words), None)
    
    if target:
        try:
            target_index = cmd_1.index(target)
            output = cmd_1[target_index + 2] if target_index + 2 < len(cmd_1) else cmd_1[target_index - 1]
            
            SearchWord = output
            try:
                myDict = PyDictionary(SearchWord)
                meanings = myDict.meaning(SearchWord)
                
                if meanings:
                    # You may want to handle multiple meanings appropriately
                    meaning = meanings[list(meanings.keys())[0]][0]
                    speak('The meaning of the word {} is {}'.format(output, meaning))
                else:
                    speak('Sorry, there is no meaning found for this word.')
            except:
                speak('Sorry, there is no meaning found for this word.')
        except ValueError:
            speak('Error: Target word not found in the command.')

# def rec_voice():
#     root = create_window() 
#     root.update()
#     root.configure(background='green')
#     with sr.Microphone() as source:
#         print('Listening...')
#         audio = speech.listen(source=source, timeout=5, phrase_time_limit=3)
#     global audcheck
#     voice_text = ''
#     try:
#         print("Recognizing...")
#         voice_text = speech.recognize_google(audio, language='en-in')
#     except sr.UnknownValueError:
#         audcheck += 1
#         pass
#     except sr.RequestError:
#         print("Network error")
#     except sr.WaitTimeoutError as e:
#         print("Timeout; {0}".format(e))
#     if not voice_text:
#         print("Sorry, my system doesn't detect any voice command")
#         if audcheck == 2:
#             print(':: Waiting for wakeword detection ::')
#             # Add code for playing stop sound or any other action
#     if voice_text:
#         print('You said:', voice_text)
#         audcheck = 0
#     root.quit()
#     return voice_text



hour = int(datetime.datetime.now().hour)

def wishMe():
    if hour>=0 and hour<12:
        speak("Good Morning ")
    elif hour>=12 and hour<18:
        speak("Good Afternoon ")
    else:
        speak("Good Evening  ")
        
        
# def rec_voice():
#     with sr.Microphone() as source:
#         print('Listening...')
#         audio = speech.listen(source=source, timeout=5, phrase_time_limit=3)
#     global audcheck
#     voice_text = ''
#     try:
#         print("Recognizing...")
#         voice_text = speech.recognize_google(audio, language='en-in')
#     except sr.UnknownValueError:
#         audcheck += 1
#         pass
#     except sr.RequestError:
#         print("Network error")
#     except sr.WaitTimeoutError as e:
#         print("Timeout; {0}".format(e))
#     if not voice_text:
#         print("Sorry, my system doesn't detect any voice command")
#         if audcheck == 2:
#             print(':: Waiting for wakeword detection ::')
#             # Add code for playing stop sound or any other action
#     if voice_text:
#         print('You said:', voice_text)
#         audcheck = 0
#     return voice_text


def weather(cmd):
    try:
        api_key = "e4f632b30200a8119247a8df609f16fa"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = 'Greater Noida, IN'
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature = current_temperature - 273.15
            current_temperature = (int)((current_temperature * 100 + .5) / 100)
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            if cmd == 'status':
                speak(
                    ' the weather in Greater Noida is {} degree Celsius with {}, And humidity is {} % with atmospheric pressure {} millibars'.format(
                        str(current_temperature), str(weather_description), str(current_humidiy),
                        str(current_pressure)))
            elif cmd == 'temp':
                speak(
                    ' current temparature in your location is {} degree celcius.'.format(current_temperature))
            elif cmd == 'morning':
                if hour >= 0 and hour < 12:
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    speak(
                        "Good Morning ,, its {} AM, and the weather in Greater Noida is {} degree Celsius with {}, And humidity is {} % with atmospheric pressure {} millibars".format(
                            strTime,
                            str(current_temperature), str(weather_description), str(current_humidiy),
                            str(current_pressure)))
        else:
            speak("sorry  your current location is not found")
    except ConnectionError:
        speak('sorry  internet and I not working')
    except :
        speak('sorry , unable to fetch weather information as Internet and I is not connected.')
        
def shutdown_sys(voice_note):
    password = rec_voice().lower()
    if '8' in password and '0' in password and '2' in password and '5' in password:
        if 'shutdown' in voice_note or 'shut' in voice_note:
            speak('shutting down system')
            speak(' Bye  and take care ')
            os.system('shutdown -s')
        else:
            speak("Restarting The system")
            os.system('shutdown -r')
        exit()
    else:
        if 'cancel' in password or 'shut' in password:
            speak('As you wish ')
        elif 'can' in password or 'don' in password or 'no' in password or 'need' in password:
            speak(
                "Sorry  because of security protocol i can't perform this action without password")
        else:
            speak('sorry  password doesnot match')
        
        
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--access_key',
        help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')

    parser.add_argument(
        '--keywords',
        nargs='+',
        help='List of default keywords for detection. Available keywords: %s' % ', '.join(
            '%s' % w for w in sorted(pvporcupine.KEYWORDS)),
        choices=sorted(pvporcupine.KEYWORDS),
        metavar='')

    parser.add_argument(
        '--keyword_paths',
        nargs='+',
        help="Absolute paths to keyword model files. If not set it will be populated from `--keywords` argument")

    parser.add_argument(
        '--library_path',
        help='Absolute path to dynamic library. Default: using the library provided by `pvporcupine`')

    parser.add_argument(
        '--model_path',
        help='Absolute path to the file containing model parameters. '
             'Default: using the library provided by `pvporcupine`')

    parser.add_argument(
        '--sensitivities',
        nargs='+',
        help="Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A higher "
             "sensitivity results in fewer misses at the cost of increasing the false alarm rate. If not set 0.5 "
             "will be used.",
        type=float,
        default=None)

    parser.add_argument('--audio_device_index', help='Index of input audio device.', type=int, default=-1)

    parser.add_argument('--output_path', help='Absolute path to recorded audio for debugging.', default=None)

    parser.add_argument('--show_audio_devices', action='store_true')

    args = parser.parse_args()

    if args.show_audio_devices:
        for i, device in enumerate(PvRecorder.get_available_devices()):
            print('Device %d: %s' % (i, device))
        return

    if args.keyword_paths is None:
        if args.keywords is None:
            raise ValueError("Either `--keywords` or `--keyword_paths` must be set.")

        keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in args.keywords]
    else:
        keyword_paths = args.keyword_paths

    if args.sensitivities is None:
        args.sensitivities = [0.5] * len(keyword_paths)

    if len(keyword_paths) != len(args.sensitivities):
        raise ValueError('Number of keywords does not match the number of sensitivities.')

    try:
        porcupine = pvporcupine.create(
            access_key=args.access_key,
            library_path=args.library_path,
            model_path=args.model_path,
            keyword_paths=keyword_paths,
            sensitivities=args.sensitivities)
    except pvporcupine.PorcupineInvalidArgumentError as e:
        print("One or more arguments provided to Porcupine is invalid: ", args)
        print(e)
        raise e
    except pvporcupine.PorcupineActivationError as e:
        print("AccessKey activation error")
        raise e
    except pvporcupine.PorcupineActivationLimitError as e:
        print("AccessKey '%s' has reached it's temporary device limit" % args.access_key)
        raise e
    except pvporcupine.PorcupineActivationRefusedError as e:
        print("AccessKey '%s' refused" % args.access_key)
        raise e
    except pvporcupine.PorcupineActivationThrottledError as e:
        print("AccessKey '%s' has been throttled" % args.access_key)
        raise e
    except pvporcupine.PorcupineError as e:
        print("Failed to initialize Porcupine")
        raise e

    keywords = list()
    for x in keyword_paths:
        keyword_phrase_part = os.path.basename(x).replace('.ppn', '').split('_')
        if len(keyword_phrase_part) > 6:
            keywords.append(' '.join(keyword_phrase_part[0:-6]))
        else:
            keywords.append(keyword_phrase_part[0])

    # print('Porcupine version: %s' % porcupine.version)

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=args.audio_device_index)
    recorder.start()

    wav_file = None
    if args.output_path is not None:
        wav_file = wave.open(args.output_path, "w")
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)

    
    # hwnd = win32gui.GetForegroundWindow()
    # win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    # under develop to show on left window
    # a = is_computer_locked()
    # if a:
    #     print('Locked')
    #     while True:
    #         time.sleep(1)
    #         a = is_computer_locked()
    #         if a == False:
    #             time.sleep(2) 
                 
    # else:
    #     print('not locked')
    #     time.sleep(1)
            
    if failsafe_check == 0:
            hour = int(datetime.datetime.now().hour)
            if hour >= 5 and hour < 12:
                weather('morning')
            else:
                responses = [
                    "I'm ready to assist you. Just give me a call when you need help.",
                    "I'm here and ready for any tasks you have. Feel free to call on me.",
                    "Ready and waiting to assist you. Just let me know what you need.",
                    "I'm fully prepared to help. Call me anytime you require assistance.",
                    "I'm at your service. Call me when you're ready, and I'll be here to assist.",
                ]
                speak(random.choice(responses))
    else :
        speak('After solving the problem, please let me know')
    print(':: waiting for wakeword detection ::')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if wav_file is not None:
                wav_file.writeframes(struct.pack("h" * len(pcm), *pcm))

            if result >= 0:
                global audcheck
                global vnote
                audcheck = 0
                if failsafe_check > 0 :
                    speak('Yes, did the glitch of my program is solved:')
                    voice_note = rec_voice().lower()
                    if 'yes' in voice_note or 'solve' in voice_note:
                        speak('Thank you for fixing my problem')
                        open("C:\\Users\\mashu\\error.txt", "w").close()
                        os.system('taskkill /F /FI "WindowTitle eq error.txt - Notepad" /T')
                        with open(__file__, 'r') as f:
                            lines = f.read().split('\n')
                            val = int(lines[0].split(' = ')[+1])
                            new_line = 'failsafe_check = {}'.format(val * 0)
                            new_file = '\n'.join([new_line] + lines[1:])
                        with open(__file__, 'w') as f:
                            f.write('\n'.join([new_line] + lines[1:]))
                        speak('Now please wait a second. let me update my program to continue')
                        os.system('porcupine_demo_mic --access_key uX5rsH7XMmSI5Aey1irLgr+R4OiwiTZch0L/JIIZLwZDjCZgauAaZg== --keywords miami --audio_device_index 1')
                    else:                        
                        speak('Its okay now tell me  what can i do for you ?')
                else:
                    # play_sound("C:\\users\\mashu\\start.mp3")      
                    speak('Yes')        
                    while audcheck < 1:
                        try:
                            slp = 0
                            voice_note = rec_voice().lower()
                            vnote = voice_note
                            if voice_note == 'miami':
                                speak('yes , what can i do for you ?')
                                continue
                            if voice_note == 'open' :
                                speak('what do you want me to open  ?')
                                newcm = rec_voice().lower()
                                newcm = newcm.replace('open','')
                                voice_note =str(voice_note +' '+ newcm)
                            voice_note = voice_note.replace('miami', '')
                            # if 'translate' in voice_note or 'in hindi' in voice_note or 'in bengali' in voice_note :
                            #     translator(voice_note)
                            #     continue
                            # elif 'mean' in voice_note or 'meaning' in voice_note:
                            #     dictionary(voice_note)
                            #     continue
                            if 'hello' in voice_note or 'fine ' in voice_note or ' hi ' in voice_note:
                                speak("hello  how are you?")
                                voice_note = rec_voice().lower()
                                if 'not fine' in voice_note or 'not ok' in voice_note:
                                    speak('i am sorry to hear that. I hope you feel better ')
                                    continue
                                elif 'fine' in voice_note or 'ok' in voice_note:
                                    speak('i am glad to hear it')
                                else:
                                    speak(
                                        "hmm i thing you don't want to share , just take care of yourself")
                                continue
                            elif 'are you there' in voice_note:
                                speak('Yes  tell me what to do')
                                continue
                            # elif 'wikipedia' in voice_note:
                            #     speak('Searching Wikipedia...')
                            #     voice_note = voice_note.replace("wikipedia", "")
                            #     results = wikipedia.summary(voice_note, sentences=2)
                            #     speak("According to Wikipedia")
                            #     speak(results)
                            #     continue
                            elif re.search(r'\b(how are you)\b', voice_note):
                                responses = ["I'm just a computer program, but thanks for asking!", "I'm functioning well, thank you!"]
                                speak(random.choice(responses))                           
                            elif 'thank you' in voice_note:
                                responses = ["You're welcome . I'm just doing my job.", "No problem, !", "Glad I could help!"]
                                speak(random.choice(responses))
                            elif 'call' in voice_note and '' in voice_note:
                                speak('because you have created me')
                                continue
                            elif ('who' in voice_note and 'are you' in voice_note) or 'introduce' in voice_note:
                                speak(
                                    'I am MIAMI, An artificial intelligence, or you can say a virtual personal assistant developed by Mr. Mashudd')
                                continue
                            elif 'am i' in voice_note or "my name" in voice_note or 'made you' in voice_note or 'created you' in voice_note or 'you know me' in voice_note or 'developed you' in voice_note:
                                if 'you know me' in voice_note:
                                    speak('Yes, i know You , you are my Creater, Mr.Mashud')
                                    continue
                                else:
                                    speak("Mashud")
                                    continue
                            elif 'open facebook' in voice_note:
                                webbrowser.open("https://www.facebook.com/")
                                speak("opening ")
                                continue
                            elif 'open github' in voice_note:
                                webbrowser.open("https://www.github.com/")
                                speak("opening ")
                                continue
                            elif 'open google' in voice_note:
                                webbrowser.open("https://google.com/")
                                speak("opening ")
                                continue
                            elif 'open stackoverflow' in voice_note:
                                webbrowser.open("https://stackoverflow.com/")
                                speak("opening ")
                                continue
                            elif 'open youtube' in voice_note:
                                webbrowser.open("https://youtube.com/")
                                speak("opening ")
                                continue
                            elif 'open whatsapp' in voice_note:
                                webbrowser.open("https://web.whatsapp.com/")
                                speak("opening ")
                            elif 'music' in voice_note and 'youtube' in voice_note and 'my' in voice_note:
                                webbrowser.open("https://www.youtube.com/watch?v=q2-HquLLmSw&t=35s")
                                speak("opening ")
                            elif ('show' in voice_note or 'open' in voice_note) and 'mail' in voice_note:
                                webbrowser.open('https://mail.google.com/mail/u/0/#inbox')
                                speak('opening your mails ')
                                continue
                            elif ('pause' in voice_note or 'play' in voice_note or 'resume' in voice_note) and 'music' in voice_note :
                                pyautogui.hotkey('playpause')
                                continue
                            elif 'unlock' in voice_note and ('system' in voice_note or 'pc' in voice_note or 'com' in voice_note):
                                '''
                                if log_info == "unlocked" :
                                    speak(" your pc is already unlocked")
                                else:
                                    '''
                                ctypes.windll.user32.LockWorkStation()
                                speak("unlocking :")
                                pyautogui.press('enter')
                                pyautogui.press('enter')
                                speak('Please use password to unlock  ')
                                time.sleep(1)
                                continue
                            elif 'mute' in voice_note:
                                mute()
                                # speak('Done')
                            elif 'unmute' in voice_note:
                                volume_up()
                                # speak('Done ')
                            elif 'volume' in voice_note:
                                if 'up' in voice_note:
                                    volume_up()
                                    # speak('Volumed up ')
                                    continue
                                elif 'down' in voice_note or 'reduce' in voice_note:
                                    volume_down()
                                    # speak('Volumed Reduced ')
                                    continue
                                elif 'set' in voice_note or 'by' in voice_note:
                                    percentage = re.findall(r'[0-9]+', voice_note)
                                    if len(percentage) == 0:
                                        speak("By How many percent ?")
                                        voice_note = rec_voice().lower()
                                        percentage = re.findall(r'[0-9]+', voice_note)
                                        if len(percentage) == 0:
                                            speak("Sorry, I am not able to understand")
                                            pass
                                        else:
                                            per = int(percentage[0])
                                            set_volume(per)
                                            speak('volume set to ' + str(per) + ' percent ')
                                            continue
                                    else:
                                        per = int(percentage[0])
                                        set_volume(per)
                                        speak('volume set to' + str(per) + 'percent ')
                                        continue
                                else:
                                    speak(
                                        'sorry , i do not understand what to do with volume setting. please try again.')
                            elif 'search' in voice_note and ('google' in voice_note or 'youtube' in voice_note):
                                voice_note = voice_note.replace('search', '', 1)
                                voice_note = voice_note.replace('on', '', 1)
                                voice_note = voice_note.replace(' for ', '', 1)
                                if 'google' in voice_note:
                                    voice_note = voice_note.replace('google', '', 1)
                                    webbrowser.open('https://www.google.com/search?q={}'.format(voice_note))
                                    speak('Searching on google ')
                                    continue
                                elif 'youtube' in voice_note:
                                    voice_note = voice_note.replace('youtube', '', 1)
                                    webbrowser.open(
                                        'https://www.youtube.com/results?search_query={}'.format(voice_note))
                                    speak('searching on youtube ')
                                    continue                          


                            elif ('system' in voice_note or 'computer' in voice_note or 'pc' in voice_note) and (
                                    'shut' in voice_note or 'reboot' in voice_note or 'restart' in voice_note):
                                if 'shut' in voice_note:
                                    speak("Are you sure you want to shut down the system")
                                    confirmation = rec_voice().lower()
                                    if ('yes' or 'please') in confirmation:
                                        speak('shutting down system')
                                        speak(' Bye  and take care ')
                                        os.system('shutdown -s -t 0')
                                    else:
                                        speak('As you wish')
                                elif 'rest' in voice_note or 'boot' in voice_note:
                                    speak("Are you sure you want to restart the system")
                                    confirmation = rec_voice().lower()
                                    if ('yes' or 'please') in confirmation:
                                        speak('restarting the system')
                                        os.system('shutdown -r -t 0')
                                    else:
                                        speak('As you wish')                              
                            
                            elif 'chrome' in voice_note or 'browser' in voice_note:
                                if 'open' in voice_note:
                                    os.popen('start chrome')
                                    speak('opening ')
                                    continue
                                elif 'close' in voice_note:
                                    os.popen('tskill chrome')
                                    speak('done')
                                    continue
                                else:
                                    speak('sorry i did not got it please try again')
                                    continue
                            elif ( 'notepad' in voice_note or 'write something' in voice_note) and 'i ' in voice_note or 'note something' in voice_note or ' note' in voice_note:
                                if 'open' in voice_note or 'something' in voice_note:
                                    os.popen('start notepad')
                                    if 'open' in voice_note:
                                        speak('ok ')
                                        continue
                                    else:
                                        speak('ok  i am opening notepad for you')
                                        continue
                                elif 'close' in voice_note:
                                    os.popen('tskill notepad')
                                    speak('as you wish ')
                                    continue
                                else:
                                    speak('sorry  i didnot got it please try again')
                                    continue
                            elif 'window' in voice_note:
                                if 'close' in voice_note:
                                    pyautogui.hotkey('alt', 'f4')
                                    speak('closed ')
                                    continue
                                elif 'mini' in voice_note:
                                    pyautogui.hotkey('win', 'm')
                                    speak('as you wish ')
                                    continue
                                elif 'max' in voice_note:
                                    pyautogui.hotkey('win', 'up')
                                    speak('Done ')
                                elif 'small' in voice_note:
                                    pyautogui.hotkey('win', 'down')
                                    speak('as you wish ')
                                else:
                                    speak('sorry  i did not got it, please say it once')
                            elif 'thank' in voice_note and 'you' in voice_note :
                                speak("You're welcome . i'm just doing my job.")
                                continue
                            elif 'weather' in voice_note or 'temperature' in voice_note:
                                if 'temp' in voice_note:
                                    weather('temp')
                                    continue
                                else:
                                    weather('status')
                                    continue                                
                            elif re.search(r'news', voice_note, re.IGNORECASE):
                                speak('Fetching todays news please wait')
                                news()                            
                            elif re.search(r'\b(extend display|dual display|coding time|work time)\b', voice_note):
                                os.popen('DisplaySwitch.exe /extend')                            
                                if('coding' in voice_note):
                                    speak('Extending display and opening vs code.')
                                else:
                                    speak("Extending display.") 
                            elif re.search(r'\b(switch to display 1|gaming display|gaming time|movie time|dinner time)\b', voice_note):
                                os.popen('DisplaySwitch.exe /internal')
                                if('gaming' in voice_note):
                                    speak('Enjoy Gaming')
                                elif('dinner' in voice_note):
                                    speak("enjoy dinner time and what you want to prefer Youtube or Netflix?")
                                    preference = rec_voice()
                                    if ('youtube' in voice_note):
                                        webbrowser.open("https://youtube.com/")
                                    elif('net' in voice_note):
                                        webbrowser.open("https://www.netflix.com/browse")
                                    elif ('' or ' nothing' in voice_note):
                                        speak('okay')
                                    else:
                                        webbrowser.open('https://www.google.com/search?q={}'.format(preference))
                            # elif 'set' in voice_note and 'alarm' in voice_note:
                            #     alarm(voice_note)
                            elif 'make' in voice_note and 'note' in voice_note:
                                speak('tell me  what to write')
                                voice_note = rec_voice()
                                txt = open('C:\\Users\\mashu\\masu.txt', 'a+')
                                txt.write('%s\r\n' % (voice_note))
                                txt.close()
                                speak('Nooted ')
                                speak('want to see the note ')
                                voice_note = rec_voice().lower()
                                if 'yes' in voice_note or 'open' in voice_note:
                                    os.popen('notepad ' "C:\\Users\\mashu\\masu.txt" '')
                                    speak('should i read it for you ')
                                    voice_note = rec_voice().lower()
                                    if 'yes' in voice_note or 'read' in voice_note:
                                        pyautogui.hotkey('ctrl', 'a')
                                        reader()
                                        pyautogui.hotkey('alt', 'f4')
                                    else:
                                        speak('As you wish ')
                                        continue
                                else:
                                    speak('As you wish ')
                                continue
                            elif "this pc" in voice_note:
                                speak("Wait a Second :")
                                subprocess.Popen('explorer.exe /e,::{20D04FE0-3AEA-1069-A2D8-08002B30309D}')
                                speak("Here You GO ")
                                continue
                            elif ' c' in voice_note and 'drive' in voice_note:
                                subprocess.Popen('explorer C:\\')
                                speak("Opening Drive C ")
                                continue
                            elif ' d ' in voice_note and 'drive' in voice_note:
                                subprocess.Popen('explorer D:\\')
                                speak("Opening Drive D ")
                                continue
                            elif ' e ' in voice_note and 'drive' in voice_note:
                                subprocess.Popen('explorer E:\\')
                                speak("Opening Drive E ")
                                continue
                            elif ' f' in voice_note and 'drive' in voice_note:
                                subprocess.Popen('explorer F:\\')
                                speak("Opening Drive F ")
                                continue
                            elif ' g' in voice_note and 'drive' in voice_note:
                                subprocess.Popen('explorer G:\\')
                                speak("Opening Drive G ")
                                continue
                            elif ' h' in voice_note and 'drive' in voice_note:
                                subprocess.Popen('explorer H:\\')
                                speak("Opening Drive H")
                                continue
                            elif ' drive ' in voice_note:
                                speak("Sorry  There is no drive like that ")
                                continue
                            elif 'lock' in voice_note and ('system' in voice_note or 'pc' in voice_note or 'com' in voice_note):
                                speak("locking ")
                                ctypes.windll.user32.LockWorkStation()
                                continue
                            elif ('source' in voice_note or 'your' in voice_note) and 'code' in voice_note:
                                speak('opening my source code')
                                m = 'C:\\Users\\mashu\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\pvporcupinedemo\\porcupine_demo_mic.py'
                                os.system("start {}".format(m))
                                continue
                            elif 'open' in voice_note and ('code' in voice_note or 'editor' in voice_note):
                                speak('Opening V S Code ')
                                os.popen('start code')
                                continue
                            elif "open drive" in voice_note:
                                speak('Which Drive Do You want to Open ?')
                                try:
                                    voice_note = rec_voice().lower()
                                    voice_note = voice_note + " "
                                    print(voice_note)
                                    if "this pc" in voice_note:
                                        speak("Wait a Second :")
                                        subprocess.Popen('explorer.exe /e,::{20D04FE0-3AEA-1069-A2D8-08002B30309D}')
                                        speak("Here You GO ")
                                        continue
                                    elif 'c' in voice_note:
                                        subprocess.Popen('explorer C:\\')
                                        continue
                                    elif 'd' in voice_note:
                                        subprocess.Popen('explorer D:\\')
                                        continue
                                    elif 'e' in voice_note:
                                        subprocess.Popen('explorer E:\\')
                                        continue
                                    elif 'f' in voice_note:
                                        subprocess.Popen('explorer F:\\')
                                        continue
                                    elif 'g' in voice_note:
                                        subprocess.Popen('explorer G:\\')
                                        continue
                                    elif 'h' in voice_note:
                                        subprocess.Popen('explorer H:\\')
                                        continue
                                    else:
                                        speak("Sorry  there is no drive like you said")
                                        continue
                                except IndexError:
                                    pass
                            elif ('right' in voice_note or 'write' in voice_note) and 'something' in voice_note:
                                speak('ok  go to space where you want to type')
                                speak('Now tell me  what to right')
                                voice_note = rec_voice().lower()
                                pyautogui.write(voice_note)
                                while True:
                                    speak('done , and do you want to right more ')
                                    voice_note = rec_voice().lower()
                                    if 'yes' in voice_note:
                                        speak('ok  tell me what to right next')
                                        voice_note = rec_voice().lower()
                                        pyautogui.write(' ' + voice_note)
                                        continue
                                    else:
                                        speak('as you wish ')
                                        break
                            elif (
                                    'write' in voice_note or 'right' in voice_note or 'type' in voice_note) and 'here' in voice_note:
                                word_filter(voice_note)
                                while True:
                                    speak('done , and do you want to write more ')
                                    voice_note = rec_voice().lower()
                                    if 'yes' in voice_note:
                                        speak('ok  tell me what to write next')
                                        voice_note = rec_voice().lower()
                                        pyautogui.write(' ' + voice_note)
                                        continue
                                    else:
                                        speak('as you wish ')
                                        break
                            elif re.search(r'\b(time)\b', voice_note):
                                hour = int(datetime.datetime.now().hour)
                                strTime = datetime.datetime.now().strftime("%H,%M")
                                if hour >= 0 and hour < 12:
                                    speak(f", the time is {strTime},AM")
                                else:
                                    lem = int(strTime[:2])
                                    lem = (lem - 12)
                                    strTime = datetime.datetime.now().strftime('%M')
                                    speak(f", the time is {lem, strTime},PM")
                                continue
                            elif 'read' in voice_note:
                                speak('ok make sure you have already selected what to read')
                                reader()
                            elif 'speed' in voice_note and ('net' in voice_note or 'network' in voice_note):
                                speak('showing the result in new window ')
                                os.system("start /B start cmd.exe @cmd /k speedtest-cli ")
                                continue
                            elif ('like' in voice_note or 'love' in voice_note) and 'me' in voice_note:
                                speak("Yes! A thousand times yes")
                                continue
                            elif re.search(r'\b(?:log|file)\b', voice_note):
                                speak('Opening log file')
                                os.popen('notepad ' "C:\\Users\\mashu\\log.txt" '')
                                continue            
                            
                            elif 'open' in voice_note and ' 'in voice_note:
                                voice_note=voice_note.replace('open','',1)
                                voice_note = voice_note.replace('application','',1)
                                voice_note = voice_note.replace('app','',1)
                                speak(' do you want me to open {}, application ?'.format(voice_note))
                                confirmation = rec_voice().lower()
                                if 'yes' in confirmation :
                                    pyautogui.press('win')
                                    pyautogui.write(voice_note)
                                    time.sleep(1)
                                    pyautogui.hotkey('enter')
                                    speak('Here You go ')
                                else:
                                    speak('as you wish ')
                                    continue
                            elif 'play ' in voice_note:
                                voice_note = voice_note.replace('play', '',1)
                                speak("Playing on youtube")
                                play_first_youtube_video(voice_note)
                                continue
                            elif 'mean' in voice_note or 'meaning' in voice_note:
                                dictionary(voice_note)
                                continue
                            elif 'do ' in voice_note or 'what' in voice_note or (
                                    'who' in voice_note or 'where' in voice_note and 'is' in voice_note):
                                speak(
                                    'Showing answer with the help of the google')
                                webbrowser.open('https://www.google.com/search?q={}'.format(voice_note))
                                time.sleep(2)
                                pyautogui.hotkey('down')
                                pyautogui.hotkey('down')
                                continue
                            elif any(keyword in voice_note for keyword in ['sleep', 'stop ask', 'stop lis']):
                                speak('Ok, call me when you need assistance.')
                                audcheck = 2
                                print(':: Waiting for wakeword detection ::')
                                slp = 1
                            elif re.search(r'\b(bye|goodbye|quit)\b', voice_note, re.IGNORECASE):
                                # Your code for handling goodbye actions
                                speak('Do you want me to quit ?')
                                check = rec_voice().lower()
                                if( 'yes' in check ):
                                    speak('Okay tell me the exit code to proceed')
                                    exitcode =rec_voice().lower()
                                    if '8' in exitcode and '0' in exitcode and '2' in exitcode :
                                        speak(random.choice(["Goodbye!", "See you later!", "Take care!"]))
                                        os.system('taskkill /IM "porcupine_demo_mic.exe" /F')
                                        time.sleep(1)                                
                                        os.system('taskkill /IM "cmd.exe" /F')                                    
                                    else:
                                        speak('Sorry it doesnot match with the exit code, I will be online and call me when you need assistance')
                                else:
                                    audcheck = 2
                                    print(':: Waiting for wakeword detection ::')  
                                    slp = 1                  
                            elif ('update' in voice_note or 'restart' in voice_note or 'reboot' in voice_note) and (
                                    'program' in voice_note or 'self' in voice_note or 'code' in voice_note):
                                responses = [
                                        "Sure thing! Initiating the update process.",
                                        "Updating now. This won't take long.",
                                        "Acknowledged. I'll update the program accordingly.",
                                        "Updating in progress. Please be patient.",
                                        "Got it! I'll get the latest updates for you.",
                                    ]
                                speak(random.choice(responses))
                                os.system('porcupine_demo_mic --access_key uX5rsH7XMmSI5Aey1irLgr+R4OiwiTZch0L/JIIZLwZDjCZgauAaZg== --keywords miami --audio_device_index 1')
                                exit()
                            elif 'goodnight' in voice_note or 'night' in voice_note:
                                speak(random.choice(["Goodnight!", "Sweet dreams!", "Sleep well!"])+" and do you want me to shut down the system?")                            
                                altq = rec_voice().lower()
                                if 'yes' in altq or 'shut down' in altq:
                                    speak(" i need confirmation password to shutdown the system")
                                    shutdown_sys('shut down')
                                else:
                                    speak('As you wish')
                            elif voice_note:
                                random_messages = [
                                    "Sorry, I'm not familiar with that phrase. Try asking me something else.",
                                    "I'm not sure about that statement. Ask me a different question, please.",
                                    "Hmm, this is new to me. Feel free to inquire about something else.",
                                    "I didn't quite catch that. Can you try rephrasing your question or ask something else?",
                                ]
                                random_message = random.choice(random_messages)
                                speak(random_message)
                        except Exception as e:
                            if e == 'listening timed out while waiting for phrase to start':
                                pass
                            else:
                                with open(__file__, 'r') as f:
                                    lines = f.read().split('\n')
                                    val = int(lines[0].split(' = ')[+1])
                                    new_line = 'failsafe_check = {}'.format(val+1)
                                    new_file = '\n'.join([new_line] + lines[1:])
                                with open(__file__, 'w') as f:
                                    f.write('\n'.join([new_line] + lines[1:]))
                                speak('There is a glitch in my program. please solve it, i am opening the source code and error details for you.')
                                m = 'C:\\Users\\mashu\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\site-packages\\pvporcupinedemo\\porcupine_demo_mic.py'
                                os.system("start {}".format(m))
                                txt = open('C:\\Users\\mashu\\error.txt', 'a+')
                                txt.write('%s\r\n' % (e))
                                txt.close()
                                os.popen('notepad ' "C:\\Users\\mashu\\error.txt" '')
                                # os.system('python C:\\Users\\mashu\\fix.py')
                                # exit()
                        time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping ...')
    finally:
        recorder.delete()
        porcupine.delete()
        if wav_file is not None:
            wav_file.close()


if __name__ == '__main__':
    main()