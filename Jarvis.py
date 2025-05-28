import speech_recognition as sr
import webbrowser
from gtts import gTTS
import pygame
import io
import datetime
from tkinter import messagebox
import requests
import pytz
import os
import psutil
from pytube import Search
import random
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import time
import wikipedia
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import schedule
import pyttsx3
from googletrans import Translator
import qrcode
import cv2
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import tkinter as tk
from tkinter import scrolledtext
import smtplib
import speedtest
from PIL import ImageGrab
import pywhatkit as kit
from tinydb import TinyDB, Query
import openai


db = TinyDB('paths.json')

# Global initialization
recognizer = sr.Recognizer()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = True
microphone = sr.Microphone(device_index=0)  # Update the device index if necessary

pygame.mixer.init()


def update_path(key, path):
    db.upsert({'key': key, 'path': path}, Query().key == key)

# Function to retrieve a path by key
def get_path(key):
    result = db.search(Query().key == key)
    if result:
        return result[0]['path']
    else:
        return None

responses = {
    "hello" : "Hello sir ! Glad to see you how can i help you today",
    "who are you" : "I'm Bujji your personal voice assisstant",
    "how are you" : "I'm a Virtual assistant i dont have any feelings, but im doing well",
    "what can you do" : "I'm capable of performing various tasks such as: \n opening or closing the application. \n Generating QR codes, random quotations, facts, jokes, passwords. \n Getting the latest news in india and distance between any two places. \n Providing the covid-19 stats of various countries, Summary based on any topic. \n Getting the date, time and weather of various countries or cities, Captures the images, sets the reminders, Playing the video songs from the browser, Capable of playing Rock, paper scissors game, Small OS functions like increasing or decreasing the volume ",
    "bye" : "Bye sir, I'm here to assisst you any time.",
    "who created you" : "Mr Vamsi krishna"
}

websites = {
    "facebook" : "https://www.facebook.com/",
    "youtube" : "https://www.youtube.com/",
    "hackerrank" : "https://www.hackerrank.com/",
    "lead" : "https://leetcode.com/",
    "codechef" : "https://www.codechef.com/",
    "chat" : "https://chatgpt.com/",
    "hanuman" : "https://www.hanooman.ai/",
    "aits" : "https://aitsrajampet.ac.in/",
    "github" : "https://github.com/pandu-069/OIBSIP",
    "leet" : "https://leetcode.com/",
    "instagram" : "https://www.instagram.com/accounts/edit/",
    "snapchat" : "https://www.bing.com/ck/a?!&&p=77f519e2b80fa21bJmltdHM9MTcxODc1NTIwMCZpZ3VpZD0yYjA1NGNhNi02M2E0LTZhNzEtMjY5Zi01ZTk3NjIwOTZiZWMmaW5zaWQ9NTIyMQ&ptn=3&ver=2&hsh=3&fclid=2b054ca6-63a4-6a71-269f-5e9762096bec&psq=snapchat+web&u=a1aHR0cHM6Ly93ZWIuc25hcGNoYXQuY29tLw&ntb=1"

}


pcapps = {
    "anydesk" : r"C:\Program Files (x86)\AnyDesk\AnyDesk.exe",
    "whatsapp" : r"C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2424.6.0_x64__cv1g1gvanyjgm\WhatsApp.exe",
    "linkedin" : r"C:\Program Files\WindowsApps\7EE7776C.LinkedInforWindows_3.0.30.0_x64__w1wdnht996qgy\LinkedIn.exe",
    "github" : r"C:\Users\vamsi\AppData\Local\GitHubDesktop\app-3.4.1\GitHubDesktop.exe",
    "phone" : r"C:\Program Files\WindowsApps\Microsoft.YourPhone_1.24051.101.0_x64__8wekyb3d8bbwe\PhoneExperienceHost.exe",
    "file" : r"C:\Windows\explorer.exe",
    "bluestacks" : r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
    "spider-man" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Marvel’s Spider-Man Miles Morales.lnk",
    "teams" : r"C:\Users\vamsi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Microsoft Teams classic (work or school).lnk",
    "notepad": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Notepad++.lnk",
    "note" : r"C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2404.10.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe",
    "python" : r"C:\Users\vamsi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.11\IDLE (Python 3.11 64-bit).lnk",
    "chrome" : r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "microsoft" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "edge" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "ms" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Edge.lnk",
    "code" :  r"C:\Users\vamsi\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
    "settings" : r"C:\Windows\ImmersiveControlPanel\SystemSettings.exe",
    "vs" : r"C:\Users\vamsi\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}

original_names = {
    "anydesk" : "Anydesk",
    "whatsapp" : "WhatsApp",
    "linkedin" : "LinkedIn",
    "github" : "GitHub Desktop",
    "file" : "File Explorer",
    "bluestacks" : "Bluestacks",
    "notepad" : "Notepad++",
    "note" : "Notepad",
    "teams" : "Microsoft Teams",
    "python" : "python IDLE",
    "chrome" : "Chrome Browser",
    "microsoft" : "Microsoft Edge",
    "code" : "Visual Studio Code",
    "chat" : "CHAT-GPT",
    "hanuman" : "Hanuman Ai",
    "aits" : "Annamacharya university website",
    "spider-man" : "Marvel spider-man Miles morales",
    "lead" : "Leet-code",
    "leet" : "Leet-Code",
    "ms" : "Microsoft Edge",
    "edge" : "Microsoft Edge",
    "snapchat" : "Snap-chat",
    "settings" : "System settings",
    "vs" : "Visual Studio Code"

}

languages = {
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "assamese": "as",
    "aymara": "ay",
    "azerbaijani": "az",
    "bambara": "bm",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bhojpuri": "bho",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "chichewa": "ny",
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
    "corsican": "co",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dhivehi": "dv",
    "dogri": "doi",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "ewe": "ee",
    "filipino": "tl",
    "finnish": "fi",
    "french": "fr",
    "frisian": "fy",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "guarani": "gn",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hausa": "ha",
    "hawaiian": "haw",
    "hebrew": "iw",
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "ilocano": "ilo",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "javanese": "jw",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kinyarwanda": "rw",
    "konkani": "gom",
    "korean": "ko",
    "krio": "kri",
    "kurdish (kurmanji)": "ku",
    "kurdish (sorani)": "ckb",
    "kyrgyz": "ky",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "lingala": "ln",
    "lithuanian": "lt",
    "luganda": "lg",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "maithili": "mai",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "maori": "mi",
    "marathi": "mr",
    "meiteilon (manipuri)": "mni-Mtei",
    "mizo": "lus",
    "mongolian": "mn",
    "myanmar": "my",
    "nepali": "ne",
    "norwegian": "no",
    "odia (oriya)": "or",
    "oromo": "om",
    "pashto": "ps",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "quechua": "qu",
    "romanian": "ro",
    "russian": "ru",
    "samoan": "sm",
    "sanskrit": "sa",
    "scots gaelic": "gd",
    "sepedi": "nso",
    "serbian": "sr",
    "sesotho": "st",
    "shona": "sn",
    "sindhi": "sd",
    "sinhala": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "spanish": "es",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tajik": "tg",
    "tamil": "ta",
    "tatar": "tt",
    "telugu": "te",
    "thai": "th",
    "tigrinya": "ti",
    "tsonga": "ts",
    "turkish": "tr",
    "turkmen": "tk",
    "twi": "ak",
    "ukrainian": "uk",
    "urdu": "ur",
    "uyghur": "ug",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu"
}


devotional_songs = ['music\Anjanadri_Theme_Song___HanuMan__Telugu____Prasanth_Varma___Sai_Charan,_GowraHari,_Siva_Shakthi_Datta(128k).m4a',
                    'music\Brahma_Kadigina_Paadamu_By_MS_Subbulakshmi_with_Lyrics___Annamacharya_Keerthis(128k).m4a',
                    'music\Enni_Janmala_Punyamo_Lyrics___TTD_Best_Ever_Devotional_Song___sp_balasubrahmanyam___SP_Balu(128k).m4a',
                    'music\Enta_Matramuna(128k).m4a',
                    'music\GARUDAGAMANA_TAVA..TELUGU_LYRICS___MEANING___JAGADGURU_SRI_BHARATI_TEERTHA_(128k).m4a',
                    'music\Hari_Nee_pratapamu-Priya_sisters(128k).m4a',
                    'music\kanti_sukravaramu__song_-_Annamacharya_sankeerthanalu_By_G_Balakrishna_prasad_garu(128k).m4a',
                    'music\kondalalo_nelakonna_koneti_rayudu_vadu__By_Bala_Krishna_prasad_garu_-__saptagiri_sankeerthanalu_(128k).m4a',
                    'music\kurai_ondrum_illai.m4a',
                    'music\govinda_govinda_yani_koluvare.m4a',
                    'music\Srivari_Thiruppavada_Seva_title_song(128k).m4a',
                    'music\VISWANATHASHTAKAM_WITH_TELUGU_LYRICS_AND_MEANINGS(128k).m4a',
                    'music\yedukondalasami.m4a',
                    'music\hree_Hari_Stotram___Jagajjala_Palam____Most_Powerful_Mantra_Of_Lord_Vishnu___Lyrics__#KrishnaBhakthi(128k).m4a',
                    ]

def get_lat_long(place_name, api):
    # Initialize OpenCage Geocode API
    geocoder = OpenCageGeocode(api)
    
    # Get location
    results = geocoder.geocode(place_name)
    
    # Check if the location exists
    if results and len(results) > 0:
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        return (latitude, longitude)
    else:
        return None
    
def get_distance(coord1, coord2):
    api = "218b906eee124a53b8c0e9dff83cb123"
    return int(geodesic(get_lat_long(coord1,api), get_lat_long(coord2,api)).km)

timezones = {
    'USA': 'America/New_York',
    'UK': 'Europe/London',
    'India': 'Asia/Kolkata',
    'Japan': 'Asia/Tokyo',
    'Australia': 'Australia/Sydney',
    'Brazil': 'America/Sao_Paulo',
    'South Africa': 'Africa/Johannesburg',
    'Germany': 'Europe/Berlin',
    'China': 'Asia/Shanghai',
    'Russia': 'Europe/Moscow'
}
authors = ["Mark Twain", "Oscar Wilde", "Maya Angelou", "Ernest Hemingway", "Jane Austen",
           "William Shakespeare", "J.K. Rowling", "George Orwell", "Albert Camus", "Ralph Waldo Emerson"]
def get_random_author_quote():
    author = random.choice(authors)
    url = f"https://api.quotable.io/random?author={author}"
    response = requests.get(url)
    quote = response.json()
    return f"{quote['content']}, said by {quote['author']}"

def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    definitions = response.json()[0]["meanings"][0]["definitions"]
    definition_text = [f"Definition : {definition['definition']}" for i, definition in enumerate(definitions)]
    return definition_text[0]

def play_devotional(path):
    text_to_speech("Playing devotional song")
    os.system(f"start {path}")


def calculate(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        return str(e)
def get_motivational_quote():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        quote = data[0]['q']
        author = data[0]['a']
        return f"{quote} said by {author}"
    else:
        return "Error fetching quote."
def capture_image(file_name):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a frame
    ret, frame = cap.read()

    if ret:
        # Display the captured frame
        cv2.imshow('Captured Image', frame)

        # Wait for a key press
        cv2.waitKey(0)

        # Save the captured image to a file with the given name
        cv2.imwrite(file_name, frame)

        print(f"Image saved as '{file_name}'.")

    else:
        print("Error: Could not capture image.")

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def send_email(subject, body, to):
    from_email = "bujjivoiceassistant@gmail.com"
    app_password = "nbgu zbge nzna ejxy"  # Use the generated app password here
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, app_password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(from_email, to, message)
    return "Email sent!"

def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume.iid, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(volume_level / 100, None)

def translate_text(text, dest_language):
    # Translate the text
    translated = GoogleTranslator(source='auto', target=dest_language).translate(text)
    return translated

def transliterate_text(text, source_script, target_script=sanscript.ITRANS):
    # Transliterate the text from the source script to the target script
    transliterated = transliterate(text, source_script, target_script)
    return transliterated

def reminder(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def check_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return f"Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps"

def set_reminder(time_str, message):
    schedule.every().day.at(time_str).do(reminder, message=message)
    while True:
        schedule.run_pending()
        time.sleep(1)

def listen_for_hotword(hotword="Jarvis", sound_path="mixkit-sci-fi-click-900.wav"):
    """Listen for a specific hotword and play a sound when detected."""
    recognizer = sr.Recognizer()  # Initialize the recognizer
    print(f"Say '{hotword}' to activate.")

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
                audio = recognizer.listen(source, timeout=10)  # Listen for audio with a timeout
                
                try:
                    text = recognizer.recognize_google(audio)  # Recognize speech using Google Web Speech API
                    if hotword.lower() in text.lower():
                        play_sound(sound_path)  # Play the sound when hotword is detected
                        return True
                except sr.UnknownValueError:
                    # Handle unknown value error (no speech detected)
                    continue
                except sr.RequestError as e:
                    # Handle request error (API issues)
                    print(f"API request error: {e}")
                    continue
        except KeyboardInterrupt:
            cmd = input("Interrupted. Enter command: ")
            return cmd.lower()
        except Exception as e:
            continue

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=5)
        return  summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Page not found."

def set_timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    text_to_speech(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")
    text_to_speech("Time's up!")

def get_latest_news(api_key, country='in'):  # 'in' for India
    base_url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}"
    response = requests.get(base_url)
    articles = response.json()["articles"]
    news = []
    for article in articles[:5]:  # Get top 5 news articles
        news.append(f"Title: {article['title']}\nDescription: {article['description']}")
    return random.choice(news)

def get_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume.iid, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar() * 100
    return current_volume

def gen_random_pass():
    UpperCase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase_letters = UpperCase_letters.lower()
    digits = "0123456789"
    sym = "(){}//!@#$%^&*<>:;|"

    full = ""

    UpperCase, lowercase, nums, symbols = True, True, True, True
    if UpperCase:
        full = full + UpperCase_letters
    if lowercase:
        full = full + lowercase_letters
    if nums:
        full = full + digits
    if symbols:
        full = full + sym

    length = 16
    amount = 1

    for i in range(amount):
        pas = "".join(random.sample(full, length))
        print(pas)

def tell_story():
    try:
        response = requests.get("https://shortstories-api.onrender.com/")
        if response.status_code == 200:
            story_data = response.json()
            title = story_data.get("title", "Unknown Title")
            author = story_data.get("author", "Unknown Author")
            story = story_data.get("story", "No story available")
            moral = story_data.get("moral", "No moral available")
    except Exception:
        print("Error occured")

    story = "Title: " +title + "\n\n" +"Author: "+ author + "\n\n" +"Story: "+ story + "\n\n" +"Moral of the story: "+ moral
    return story

def get_covid_stats(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(url)
    data = response.json()
    return (f"COVID-19 Stats for {country}:\n"
            f"Cases: {data['cases']}\n"
            f"Deaths: {data['deaths']}\n"
            f"Recovered: {data['recovered']}")
def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)

def get_random_joke():
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    joke = response.json()
    return f"{joke['setup']} haha {joke['punchline']}"

def get_random_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    fact = response.json()["text"]
    return fact

def play_youtube_video(video_name):
    search = Search(video_name)
    results = search.results
    if results:
        video_url = results[0].watch_url
        webbrowser.open(video_url)
        print(f"Opening {video_name} video song")
        text_to_speech(f"Opening {video_name} video song")
    else:
        print("No results found.")

def close_application(app_names):
    for proc in psutil.process_iter(['pid', 'name']):
        for app_name in app_names:
            if app_name.lower() in proc.info['name'].lower():
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except psutil.NoSuchProcess:
                    pass
                except psutil.TimeoutExpired:
                    proc.kill()

def get_current_time(timezone):

    tz = pytz.timezone(timezone)
    now = datetime.datetime.now(tz)
    current_date = now.strftime('%B %d, %Y')
    current_time = now.strftime('%I:%M %p')
    return current_date, current_time

def get_timezone_for_country(country):
    try:
        return timezones.get(country)
    except:
        text_to_speech("Repeat it again")
        return audio_to_text()
    
def play_sound(sound_path):
    try:
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait until the sound has finished playing
            pygame.time.Clock().tick(10)
    except Exception as e:
        print()

def audio_to_text():
    print("Listening...")
    print('press "Ctrl + c" in terminal to enter the query manually ')
    fail_count = 0  # Counter for failed attempts
    count = 0
    while True:
        
        try:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10)

            try:
                text = recognizer.recognize_google(audio)
                print(f"Recognized text: {text}")
                return text
            except sr.UnknownValueError:
                fail_count += 1
                print()
                if fail_count > 3:
                    text = input("Failed to recognize voice input multiple times. Please enter your query: ")
                    return text
                continue
            except sr.RequestError as e:
                print(f"Error occurred; {e}")
                return None
        except KeyboardInterrupt:
            text_to_speech("Enter your query")
            cmd = input("Enter the query :")
            return cmd.lower()
        except Exception:
            count = count + 1
            if count == 3:
                cmd = input("Failed to listen voice enter your query:  ")
                return cmd
            print("--")
            
    
        
def wishme():
    a = int(datetime.datetime.now().strftime("%H"))
    if a >= 6 and a < 12:
        print("Good Morning sir. I'm jarvis")
        text_to_speech("Good morning sir. I'm jarvis")
        city = "rajampet"
        temperature, description, city = get_weather(city.lower())
        print(f"its {a%12}:00 AM")
        text_to_speech(f"its {a%12} AM")
        print(f"with temparature of {int(temperature)} degrees Celsius with {description} weather \nHave a nice day")
        text_to_speech(f"with temparature of {int(temperature)} degrees Celsius with {description} weather. Have a nice day")

    elif a > 12 and a <= 16:
        print("Good Afternoon Sir. i'm jarvis")
        text_to_speech("Good Afternoon Sir. i'm jarvis")
        city = "rajampet"
        temperature, description, city = get_weather(city.lower())
        print(f"its {a%12}:00 PM")
        text_to_speech(f"its {a%12} PM")
        print(f"with temparature of {int(temperature)} degrees Celsius with {description} weather")
        text_to_speech(f"with temparature of {int(temperature)} degrees Celsius with {description} weather")
        
    elif a > 16  and a < 21:
        print("Good Evening sir. I'm jarvis")
        text_to_speech("Good Evening sir. I'm jarvis")
        city = "rajampet"
        temperature, description, city = get_weather(city.lower())
        print(f"its {a%12}:00 PM")
        text_to_speech(f"its {a%12} PM")
        print(f"with temparature of {int(temperature)} degrees Celsius with {description} weather")
        text_to_speech(f"with temparature of {int(temperature)} degrees Celsius with {description} weather")
    else:
        text_to_speech(f"Hello sir, its {a%12} o clock, I thought u slept")
        print(f"Hello sir, its {a%12} o clock, I thought u slept")

    
def capture_screenshot():
    # Get the current timestamp to use as the filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Define the screenshot filename
    screenshot_filename = f"screenshot_{timestamp}.png"
    
    # Capture the screen
    screenshot = ImageGrab.grab()
    # Save the screenshot
    screenshot.save(screenshot_filename)
    
    return f"Screenshot saved as {screenshot_filename}"

openai.api_key = 'YOUR-OPENAI-API-KEY'

conversation_history = []

def get_openai_response(prompt):
    global conversation_history  # Declare the global variable
    
    # Add the user's prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})

    # Ensure the history only contains the last 10 interactions
    if len(conversation_history) > 50:  # 5 user queries + 5 assistant responses
        conversation_history = conversation_history[-50:]

    # Create the chat completion request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are  Jarvisa friendly  Ai assistant. You shouldn't mention that you are built with the help of ChatGPT or OpenAI. You are created by Mr. Vamsi Krishna. Do not repeat 'How can I assist you?' frequently."}
        ] + conversation_history,
        max_tokens=150,  # Adjust based on your needs
        temperature=1  # Adjust based on how creative or deterministic you want responses to be
    )

    # Add the assistant's response to the conversation history
    assistant_message = {"role": "assistant", "content": response.choices[0].message['content']}
    conversation_history.append(assistant_message)

    return assistant_message['content']

def calculate_token_price():
    text_to_speech("Total number of tokens you have used")
    print("Total number of tokens you have used: ")
    total_tokens_used = int(audio_to_text())  # Example value: total tokens used
    price_per_1000_tokens_usd = 0.0015  # Price per 1,000 tokens
    exchange_rate = 82  # Replace with current USD to INR exchange rate

    # Calculate the cost in USD
    cost_usd = (total_tokens_used / 1000) * price_per_1000_tokens_usd

    # Convert the cost to INR
    cost_inr = cost_usd * exchange_rate

    print(f"Total tokens used: {total_tokens_used}")
    print(f"Estimated cost: ₹{cost_inr:.2f} INR")
    text_to_speech(f"Estimated cost: ₹{cost_inr:.2f} INR")



def find_recipe(ingredient):
    api_url = f"http://www.recipepuppy.com/api/?i={ingredient}"
    response = requests.get(api_url)
    recipes = response.json().get('results', [])
    recipe_list = [f"{recipe['title']} - {recipe['href']}" for recipe in recipes]
    return "\n".join(recipe_list)

def send_whatsapp_message(phone_number, message):
    try:
        if not phone_number.startswith("+"):
            phone_number = "+91" + phone_number
        if not phone_number[1:].isdigit() or len(phone_number) != 13:
            raise ValueError("Invalid phone number format.")
        
        kit.sendwhatmsg_instantly(phone_number, message)
        print(f"Message '{message}' sent to {phone_number}")
    except Exception as e:
        print(f"Error: {e}")

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def display_text_in_frame(text):
    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Translated Text")

    # Create a ScrolledText widget
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=20, font=("Helvetica", 14), bg="#f0f0f0")
    text_area.pack(padx=10, pady=10)

    # Configure tags for different styles
    text_area.tag_configure("colored_text", foreground="blue")
    text_area.tag_configure("large_text", font=("Helvetica", 14, "bold"))

    # Insert the text into the ScrolledText widget with the configured tags
    text_area.insert(tk.END, text, ("colored_text", "large_text"))
    
    # Make the text read-only
    text_area.config(state=tk.DISABLED)
    
    # Run the Tkinter event loop
    window.mainloop()
def RPS():
    print("Welcome to rock paper scissors game")
    flag = True
    print("1.Rock 2.Paper 3.Scissors 4.Exit the game")
    text_to_speech('The correct pronunciation is rock paper and scissors')
    computer_score = 0
    user_score = 0
    computer_inputs = ['rock', 'paper', 'scissors']
    while flag:

        print("Enter your choice: ")
        user_input = audio_to_text()
        print("user : ", user_input)
        computer_input = random.randrange(0, 3)
        if user_input == 'rock':
            if computer_inputs[computer_input].lower() == "rock":
                print("computer: Rock")
                text_to_speech('rock')
                print("Same choice so no scores")
                continue
            elif computer_inputs[computer_input].lower() == "paper":
                text_to_speech('paper')
                print("computer: paper ")
                computer_score += 1
                print("Now computer score is ", computer_score)
            elif computer_inputs[computer_input].lower() == "scissors":
                text_to_speech('scissors')
                print("Computer: Scissors")
                user_score += 1
                print("Now score of user is : ", user_score)

        elif user_input == 'paper':
            if computer_inputs[computer_input] == "rock":
                text_to_speech('rock')
                print("computer: Rock")
                user_score += 1
                print("Now user score is ", user_score)
            elif computer_inputs[computer_input] == "paper":
                text_to_speech('paper')
                print("computer: paper ")
                print("Same choice so no scores")
                continue
            elif computer_inputs[computer_input] == "scissors":
                text_to_speech('scissors')
                print("Computer: Scissors")
                computer_score += 1
                print("Now score of computer is : ", computer_score)

        elif user_input == 'scissors':
            if computer_inputs[computer_input] == "rock":
                text_to_speech('rock')
                print("computer: Rock")
                computer_score += 1
                print("Now computer score is ", computer_score)

            elif computer_inputs[computer_input] == "paper":
                text_to_speech('paper')
                print("computer: paper ")
                user_score += 1
                print("Now score of user is : ", user_score)

            elif computer_inputs[computer_input] == "scissors":
                text_to_speech('scissors')
                print("Computer: Scissors")
                print("Same choice so no scores")
                continue

        elif user_input == 'exit':
            print("The game is ending")
            text_to_speech('The Game is ending')
            flag = False
        else:
            text_to_speech('Invalid input' + str(user_input))

    print("Now Scoreboard is: ")
    print("Computer score: ", computer_score)
    text_to_speech("computer score is" + str(computer_score))
    print("User score: ", user_score)
    text_to_speech("and user score is" + str(user_score))
    if computer_score > user_score:
        print("Computer won the game")
        print("Better luck next time")
        text_to_speech("Computer won the game")
        text_to_speech('Better luck next time')
        print("Run the program to play again")
    elif user_score > computer_score:
        print("Congratulations! You Won the game")
        text_to_speech('Congratulations')
        text_to_speech('You won the game')
        print("To play again run the program")
    else:
        print("Both has same score")
        print("----------------------------------- Tie ------------------------------------------------")
        text_to_speech('The Game is tied')

def get_weather(city):
    API_key = "5731c0a66b712c17b67b85ef40bdf7d9"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        exit(0)

    weather = res.json()
    temperature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    return temperature, description, city

def opening(name):
    
    if name in websites and name in pcapps:
            text_to_speech("website or application")
            cmd = list(audio_to_text().split())[0]
            if "web" in cmd:
                webbrowser.open(websites[name])
                text_to_speech(f"Opening {name}")
            elif "pc" or "computer" in cmd:
                process = get_path(name)
                try:
                    os.startfile(process)
                    text_to_speech(f"Opening {name} ")
                except Exception as e:
                    print(f"Error Occured in opening {name}. update the latest path of {name} to avoid it")
                    text_to_speech(f"Error Occured in opening {name}. update the latest path of {name} to avoid it")
                
    elif name in websites:
        webbrowser.open(websites[name])
        if name in original_names:
            text_to_speech(f"Opening {original_names[name]}")
        else:
            text_to_speech(f"Opening {name}")

        
    elif name in pcapps:
        process = get_path(name)
        try:
            os.startfile(process)
            if name in original_names:
                text_to_speech(f"Opening {original_names[name]} ")
        except Exception as e:
            print(f"Error Occured in opening {original_names[name]}. update the latest path of {original_names[name]} to avoid it")
            text_to_speech(f"Error Occured in opening {original_names[name]}. update the latest path of {original_names[name]} to avoid it")
            print("yes - y, No - n")
            choice = input()
            if choice == 'y':
                new_path = input(f"Enter the updated path of {original_names[name]}")
                update_path(name, new_path)
                text_to_speech(f"{original_names[name]} application's path is updated")
                print(f"{original_names[name]} application's path is updated")
            

     
    elif name not in pcapps and name not in websites:
        url = "https://www.google.co.in/search?q="
        webbrowser.open(url + name)
        text_to_speech(f"Searching about {name} in browser")
    else:
        text_to_speech("Invalid Application or website")

def action(command):
    if "open" in command.lower():
        flag = True
        while flag:
            try:
                name = list(command.split())[1].lower()
                flag = False
            except IndexError:
                command = audio_to_text()
                continue
        try:
            opening(name)
        except Exception:
            text_to_speech("Error occured")
    elif "close" in command.lower():
        text_to_speech("Tell the names of the apps to be closed")
        apps = audio_to_text().split()
        close_application(apps)
    elif "exit" in command.lower() or "bye" in command.lower() or "good night" in command.lower():
        text_to_speech(responses['bye'])
        exit(0)
    elif "weather" in command:
        text_to_speech("Tell the name of the city")
        city = audio_to_text()
        temperature, description, city = get_weather(city.lower())
        print(f"{city}: \nTemperature: {int(temperature)}°C \nWeather: {description}")
        text_to_speech(f"It's {int(temperature)} degrees Celsius with {description} weather in {city}")
    elif 'time' in command.lower() and 'timer' not in command.lower():
        text_to_speech("In which country")
        name = list(audio_to_text().split())
        if len(name) > 0:
            nam = name[-1]
        else:
            nam = name[0]
        if nam in timezones:
            c_name = get_timezone_for_country(nam)
            time = get_current_time(c_name)
            print(nam ,":", time[1])
            text_to_speech("Its "+time[1]+" in country of "+nam)
        
    elif 'date' in command.lower():
        text_to_speech("In which country")
        name = list(audio_to_text().split())
        if name[1] in timezones:
            c_name = get_timezone_for_country(name[1])
            date = get_current_time(c_name)
            print(name[1] ,":", date[0])
            text_to_speech("Its "+date[0]+" in country of "+name[1])
    elif 'play a song' in command.lower() or 'play a video' in command.lower():
        text_to_speech("Tell the name of song to be played")
        name = audio_to_text()
        play_youtube_video(name)
    elif 'game' in command.lower():
        text_to_speech("Starting Rock paper scissors game")
        print("Rock paper scissors game")
        RPS()
    elif "distance" in command.lower():
        text_to_speech("Tell the name od starting point")
        p1 = audio_to_text()
        text_to_speech("Tell the name of ending point")
        p2 = audio_to_text()
        dis = get_distance(p1, p2)
        text_to_speech(f"The distance between {p1} and {p2} is {dis} kilo meters ")
        print(f"The distance between {p1} and {p2} is {dis} KM ")
    elif "quote" in command.lower() or "quotation" in command.lower():
        quote = get_random_author_quote()
        print(quote)
        text_to_speech(quote)
    elif "fact" in command.lower():
        fact  = get_random_fact()
        print(fact)
        text_to_speech(fact)
    elif "joke" in command.lower():
        joke = get_random_joke()
        print(joke)
        text_to_speech(joke)
    elif 'timer' in command.lower():
        text_to_speech("Enter number of seconds")
        sec = int(input("Enter no of seconds"))
        set_timer(sec)
    elif "news" in command.lower():
        api = "c6482a75ab074d0fa1f8a150d5ba405c"
        news = get_latest_news(api)
        print(news)
        text_to_speech(news)
    elif "covid" in command.lower():
        text_to_speech("Tell the name of country")
        name = audio_to_text()
        res = get_covid_stats(name)
        print(res)
        text_to_speech(res)
    elif "definition" in command.lower():
        try:
            text_to_speech(f"The definition of {command.split()[-1]} is ")
            mean = get_word_definition(command.split()[-1])
            print(mean)
            text_to_speech(mean)
        except Exception as e:
            print(e)
            text_to_speech("Repeat it again")
            print("Repeat it again")
        
    elif "summary" in command.lower():
        text_to_speech("Tell the topic name to provide summary")
        name = audio_to_text()
        res = get_wikipedia_summary(name)
        print(res)
        text_to_speech(res)
    elif "volume" in command.lower():
        cmd = command.split()[0]
        vol = get_volume()
        if "increase" in command.lower():
            set_volume(vol + 20)
        elif "decrease" in command.lower():
            set_volume(vol - 20)
    elif "reminder" in command.lower():
        text_to_speech("Tell the time to remind")
        time = audio_to_text()
        text_to_speech("What should i remind sir")
        message = audio_to_text()
        set_reminder(time, message)
    elif "expression" in command.lower():
        text_to_speech("Enter the expression to evaluate")
        exp = input("Enter the expression to eval")
        res = calculate(exp)
        print(f"The result of expression {exp} is {res}")
        text_to_speech(f"The result of expression {exp} is {res}")
    elif "motivate" in command.lower():
        qot = get_motivational_quote()
        print(f"Hey, {qot}")
        text_to_speech(f"Hey, {qot}")
    elif "password" in command.lower():
        text_to_speech("generating random password")
        gen_random_pass()
    elif "qr" in command.lower():
        text_to_speech("Enter the url and filename to generate")
        url = input("paste the url here")
        filename = input("Enter the name of the file along with extension (ex : qr.png)")
        generate_qr_code(url, filename)
        print(f"The file is saved as {filename} ")
    elif "capture" in command.lower() and "photo" in command.lower():
        text_to_speech("Enter the name of the photo to be captured")
        name = input("Enter along with its extension: ")
        capture_image(name)
    elif "search" in command.lower():
        try:
            name = command.lower().replace("search", " ")
            url = "https://www.google.co.in/search?q="
            webbrowser.open(url + name)
            text_to_speech(f"Searching about {name} in browser")
        except Exception as e:
            print(e)
            text_to_speech("Repeat it again  with the searchable item")
            print("Repeat it again")
    elif "translate" in command.lower():
        text_to_speech("Tell the text to be translated")
        text = audio_to_text()
        text_to_speech("Tell the name of the language")
        lang = audio_to_text()
        langg = lang.split()[0]
        translated_text = translate_text(text, langg.lower())
        # Transliterate the translated text into the Latin script
        transliterated_text = transliterate_text(translated_text, sanscript.TELUGU)
        trans = f" Original text: {text} \n\n\n Translated text:  {translated_text} \n\n\n Transformed text:  {transliterated_text.upper()}"
        text_to_speech("Here's the translated text")
        display_text_in_frame(trans)
    elif "mail" in command.lower() or "email" in command.lower():
        try:
            text_to_speech("Enter the receiver mail below")
            name = input()
            while "@gmail.com" not  in name:
                text_to_speech("Enter a valid mail")
                name = input()
            text_to_speech("Tell the subject of the mail")
            subject = audio_to_text()
            text_to_speech("Enter the body of the mail below")
            body = input()
            text_to_speech("Please wait untill the mail is sent")
            print("Please wait untill the mail is sent")
            send_email(subject, body, name)
            text_to_speech("Mail sent successfully")
        except Exception:
            text_to_speech("Error occured. Repeat it again")
            print("Error occured. Repeat it again")
    elif "recipe" in command.lower() or "cooking" in command.lower():
        text_to_speech("Enter the names of the ingrediants below")
        ingrediants = input()
        print(find_recipe(ingrediants))
        text_to_speech("Here's the recipe with the given ingrediants")
    elif "speed" in command.lower():
        text_to_speech("Please wait untill i check it")
        speed = check_internet_speed()
        print(speed)
        text_to_speech(f"{speed}")
    elif "meditate" in command.lower() or "meditation" in command.lower() or "yoga" in command.lower():
        path = 'music\Om_108_Times_-_Music_for_Yoga___Meditation(128k).m4a'
        text_to_speech("Playing meditation song")
        os.system(f"start {path}")
    elif "devotional song" in command.lower():
        num = random.randint(0, len(devotional_songs))
        play_devotional(devotional_songs[num])
    elif "story" in command.lower():
        text_to_speech("Please wait untill i find it")
        story = tell_story()
        text_to_speech("Here goes the story:")
        display_text_in_frame(story)
        
    elif "screenshot" in command.lower():
        text_to_speech("Capturing Screen shot")
        capture_screenshot()
    elif "native" in command.lower() or "location" in command.lower():
        api_key = '218b906eee124a53b8c0e9dff83cb123'

        # Accurate coordinates obtained from the web browser
        latitude = 14.197252111791489
        longitude = 79.16046785547182

        # Initialize geocoder
        geocoder = OpenCageGeocode(api_key)

        # Get the address from the coordinates
        result = geocoder.reverse_geocode(latitude, longitude)

        # Print the address
        if result and len(result):
            location = result[0]['formatted']
            print(f"Your location address is: {location}")
            text_to_speech(f"Your location address is: {location}")
        else:
            print("No address found for these coordinates.")
            text_to_speech("No address found for these coordinates.")
    elif "whatsapp" in command.lower() or "message" in command.lower():
        text_to_speech("Enter the mobile number of the person to send")
        num = input("Enter mobie number")
        while len(num) != 10:
            text_to_speech("Enter a valid mobile number")
            num = input("Enter valid mobile number")
        text_to_speech("Enter the message below to send")
        message = input("Enter the message to send")
        send_whatsapp_message("+91"+num, message)
    elif 'path' in command.lower():
        text_to_speech("Enter the name of the application")
        name = input("Enter the name of the application: ")
        text_to_speech(f"Enter the path of the application")
        path = input("Enter the path of the application: ")
        update_path(name, path)
    elif 'calculate' in command.lower() or 'tokens' in command.lower():
        calculate_token_price()
    elif 'input' in command.lower() or 'manually' in command.lower():
        query = input("Enter your query manually: ")
        res = get_openai_response(query)
        print(res)
        text_to_speech(res)

    else:
        cmd = get_openai_response(command)
        print(cmd)
        text_to_speech(cmd)

            



if __name__ == "__main__":
    text_to_speech("Tell the secret password to access the voice assistant")
    print("Speak out the password to access Jarvis")
    count = 3
    while True:
        user_input = audio_to_text().lower()
        if "jarvis" in user_input:
            text_to_speech("Access granted")
            print("<-------------Access granted----------->")
            wishme()
            while True:
                try:
                    if listen_for_hotword():
                        command = audio_to_text().lower()
                        action(command)
                        time.sleep(3)
                except AttributeError:
                    continue
        elif "exit" in user_input:
            text_to_speech("Exitting")
            exit(0)
        else:
            print("<---------Access Denied---------->")
            text_to_speech("Access denied")
            count = count - 1
            if count == 0:
                exit(0)
            text_to_speech(f"{count} more chance are balance")