import pyttsx3
from urllib.request import urlopen
import re
from datetime import date
import time
from time import gmtime, strftime

EXITMESSAGE="Bye Bye Sir, have a good day"

engine = pyttsx3.init()

def exitMsg():
	speak(EXITMESSAGE)

def greet():
	today = date.today()
	msg="Good morning, Sir. This is Jarvis, your virtual assistant. Today is {} ".format(strftime("%A, %B %d %Y %I:%M %p", time.localtime()))
	speak(msg)
	speak("If you need any help , speak out HELP")	


def remove_html_tags(text):
    clean = re.compile('<.*>')
    return re.sub(clean, '', text)

def speak(text):

	engine.say(text)
	engine.runAndWait()	