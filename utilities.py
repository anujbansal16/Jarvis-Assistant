import pyttsx3
from urllib.request import urlopen
import re

EXITMESSAGE="Bye Bye, Sir"

engine = pyttsx3.init()

def exitMsg():
	speak(EXITMESSAGE)

def greet():
	today = date.today()
	msg="Good morning, Sir. This is Jarvis, your virtual assistant. Today is {} ".format(strftime("%A, %B %d %Y %I:%M %p", time.localtime()))
	speak(msg)


def remove_html_tags(text):
    clean = re.compile('<.*>')
    return re.sub(clean, '', text)

def speak(text):

	engine.say(text)
	engine.runAndWait()	