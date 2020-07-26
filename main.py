import speech_recognition as sr
import pyttsx3
from datetime import date
import webbrowser
import time
from time import gmtime, strftime
import wikipedia
from googlesearch import search 


JARVISMSG="How May i help you?, Sir"
NOTRECOGNIZED="Sorry Sir, I cant understand it"
EXITMESSAGE="Bye Bye, Sir"


engine = pyttsx3.init()
voices = engine.getProperty('voices') 	
r = sr.Recognizer()


###########################################


def speak(text):
	engine.say(text)
	engine.runAndWait()

def takeCommand():
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		r.pause_thresold=1
		speak("Waiting for command , Sir")
		# audio = r.adjust_for_ambient_noise(source)	
		audio = r.listen(source)
		try:
			speak("Okay")
			query=r.recognize_google(audio,language="en-in")
			print(query)
			return query
		except Exception as e:
			speak("Sorry, Sir I cant Recognize that, Sir")
			return None

def exitMsg():
	speak(EXITMESSAGE)

def greet():
	today = date.today()
	msg="Good morning, Sir. This is Jarvis, your virtual assistant. Today is {} ".format(strftime("%A, %B %d %Y %I:%M %p", time.localtime()))
	speak(msg)

def wikiData(query,sentences=1):
	speak("Searcing Wikipedia, Sir")
	try:
		wikiData=wikipedia.summary(query,sentences=sentences,auto_suggest=True)	
		print(wikiData)
		speak(wikiData)
	except Exception as e:
		speak("Sorry Sir, I cant find anything related to that")



def openTab(url):
	webbrowser.open_new_tab(url)

def getGoogleResultLink(it):
	try:
		return it.__next__()
	except Exception as e:
		print("End results")
		return None

def googleSearch(query,num=1):
	return search(query, tld="co.in", num=num, stop=10, pause=2)

def openArticles(query):
	articles_it=googleSearch(query)
	article_url=getGoogleResultLink(articles_it)	
	openTab(article_url)


def startThread():
	speak(JARVISMSG)
	while True:
		query=takeCommand();
		if query:
			query=query.lower()
			if query.startswith("google"):
				query=query.replace("google","",1)
				url="https://www.google.com.tr/search?q={}".format(query)
				openTab(url)
			elif "article on" in query or query.startswith("open"):
				#open google links
				query=query.replace("article on","",1)
				openArticles(query)

			elif query.startswith("youtube"):
				query.replace("youtube","",1)
				url = "https://www.youtube.com/results?search_query={}".format(query)
				openTab(url)
			
			elif "bye" in query or query=="exit":
				exitMsg()
				return
			else:
				wikiData(query)	
		

if __name__ == '__main__':
	# greet()	
	startThread()
