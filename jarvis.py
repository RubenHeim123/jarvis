import time
from requests import request
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit as kit
import datetime
import wikipedia
import pyjokes
import cv2
import webbrowser
import sys
import pyautogui
import PyPDF2
import os

speech_engine = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
wikipedia.set_lang('de')
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
documentPath = r"D:\Visual_Studio_Code_Python\jarvis\assets\documents"



def talk(text):
    engine.say(text)
    engine.runAndWait()

def pdf_reader(path):
    book = open(path,'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    talk(f'Das Buch hat {pages} Seiten')
    talk('Welche Seite soll ich dir vorlesen?')
    number = int(from_microphone())
    page = pdfReader.getPage(number)
    text = page.extractText()
    talk(text)

def from_microphone():
    try:
        with sr.Microphone() as micro:
            print('Listening...')
            audio = speech_engine.listen(micro)
            text = speech_engine.recognize_google(audio, language='de-DE')
            text = text.lower()
    except:
        return 'none'
    return text

def speak_with_jarvis():

    text = from_microphone()
    print(text)

    if 'spiel' in text:
        song = text.lower().replace('spiel','')
        talk('Ich spiele dir den Song ' + song)
        kit.playonyt(song)

    elif 'uhr' in text:
        now = datetime.datetime.now().strftime('%H:%M')
        print(now)
        talk('Gerade ist es ' + now)

    elif 'wer ist' in text:
        person = text.replace('wer ist', '')
        info = wikipedia.summary(person)
        print(info)
        talk(info)

    #elif 'date' in text:
    #    talk('Entschuldige, ich habe Kopfschmerzen')

    elif 'bist du single' in text.lower():
        talk('Ich bin in einer Beziehung mit wifi')

    elif 'witz' in text:
        talk(pyjokes.get_joke(language='de'))

    elif 'tschüss' in text:
        talk('Ich wünsche dir noch einen schönen Tag')
        sys.exit()

    elif 'öffne kamera' in text:
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('webcam', img)
            k = cv2.waitKey(50)
            if k==27:
                break;
        cap.release()
        cv2.destroyAllWindows()

    elif 'öffne youtube' in text:
        webbrowser.get(chrome_path).open('www.youtube.com')

    elif 'öffne google' in text:
        talk('Nach was möchtest du suchen')
        search = from_microphone()
        url = "https://www.google.com.tr/search?q={}".format(search)
        webbrowser.get(chrome_path).open(url)

    elif 'schreib eine nachricht' in text:
        hour = int(datetime.datetime.now().hour)
        minute = int(int(datetime.datetime.now().minute)+(10/6))
        kit.sendwhatmsg('+4915781603475','Kann ich dir was gutes tun?', hour, minute)
        talk('Nachricht wurde gesendet')

    elif 'wechsel das fenster' in text:
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.keyUp('alt')

    elif 'wo bin ich' in text:
        talk('Einen Moment, ich checke das kurz')
        try:
            ipAdd = requests.get('https://api.ipify.org').text
            url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
            geo_requests = requests.get(url)
            geo_data = geo_requests.json()
            city = geo_data['city']
            country = geo_data['country']
            talk(f'Ich bin mir nicht sicher aber ich glaube wir sind in {country}. Genauer gesagt in {city}')
        except Exception as e:
            talk('Entschuldige, ich kann unseren Standort nicht bestimmen')
            pass

    elif 'mach einen screenshot' in text:
        talk('Bitte nenne mir den Namen für die Screenshot datei.')
        name = from_microphone()
        talk('Halte den Screen für ein paar Sekunden genau so. Ich mache jetzt einen Screenshot')
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f'assets/images/{name}.png')
        talk('Der Screenshot wurde im richtigen Ordner gespeichert. Wo kann ich noch weiterhelfen?')

    elif 'öffne eine pdf' in text:
                
        result = [f for f in os.listdir(documentPath) if os.path.isfile(os.path.join(documentPath, f))]
        
        if len(result)>1:
            talk('Folgende Pdf Dateien sind vorhanden:')
            index = 0
            for element in result:
                talk(f'{index} die Datei {element}')
                index +=1
                time.sleep(1)
            talk('Das waren alle Dateien. Welche möchten sie gerne öffnen. Sagen Sie mir dir Nummer')
            number = int(from_microphone())
            talk(f'Ich öffne Datei nummer {number} für sie')
            webbrowser.get(chrome_path).open('file:///D:/Visual_Studio_Code_Python/jarvis/assets/documents/'+result[number])
            talk('Soll ich dir diese Datei vorlesen?')
            answer = from_microphone()
            if 'ja' in answer or 'sehr gerne' in answer:
                pdf_reader('assets/documents/'+result[number])
            else:
                talk('Zum Glück kannst du selbst lesen. Kann ich sonst noch etwas für dich tun?')

        elif len(result) == 0:
            talk('Es ist noch keine pdf verfügbar. Kann ich sonst noch etwas für dich tun?')

        else:
            talk(f'Das einzige element ist {result[0]}. Ich öffne es ihnen')
            webbrowser.get(chrome_path).open('file:///D:/Visual_Studio_Code_Python/jarvis/assets/documents/'+result[0])
            talk('Soll ich dir diese Datei vorlesen?')
            answer = from_microphone()
            if 'ja' in answer or 'sehr gerne' in answer:
                pdf_reader('assets/documents/'+result[0])
            else:
                talk('Zum Glück kannst du selbst lesen. Kann ich sonst noch etwas für dich tun?')

    elif 'versteck alle dateien' in text or 'versteck diesen ordner' in text or 'mach es sichtbar' in text:
        talk('Bitte sag mir ob du den Ordner verstecken oder sichtbar machen möchtest')
        condition = from_microphone()
        if 'versteck' in condition:
            os.system('attrib +h /s /d')
            talk('Alle Dateien sind nun versteckt')
        elif ' sichtbar' in condition:
            os.system('attrib -h /s /d')
            talk('Alle Dateien sind nun sichtbar')
        elif 'lass es' in condition or 'vergiss es' in condition:
            talk('Wenn es sein muss')
            
    else:
        talk('Bitte sag das noch einmal')

def run_jarvis():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <= 11:
        talk('Einen wunderschönen guten morgen')
    elif hour>11 and hour <= 13:
        talk('Einen wunderschönen guten mittag')
    elif hour>13 and hour <= 17:
        talk('Einen wunderschönen guten nachmittag')
    else:
        talk('Einen wunderschönen guten abend')
    talk('Ich bin Jarvis Wie kann ich dir behilflich sein')

run_jarvis()
while True:
    speak_with_jarvis()
