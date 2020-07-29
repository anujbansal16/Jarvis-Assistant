# pip install SpeechRecognition
# pip install PyAudio
import speech_recognition as sr
# pip install pyttsx3
import pyttsx3
from datetime import date
import webbrowser
import time
from time import gmtime, strftime
import wikipedia
# pip install google
from googlesearch import search 
# pip install youtube-search
from youtube_search import YoutubeSearch

from classes import News
from utilities import *



JARVISMSG="How May i help you?, Sir"
NOTRECOGNIZED="Sorry Sir, I cant understand it"


r = sr.Recognizer()

newsSources={	"google":News("google",
						{
							"most recent headlines": "https://news.google.com/news/rss"

						}),
				"times of india":News("timeofindia",
						{
							
							"top stories":"https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
							"india":"https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
							"sports":"https://timesofindia.indiatimes.com/rssfeeds/4719148.cms"
							
						})}



###########################################


def wikiData(query,sentences=1):
	speak("Searcing Wikipedia, Sir")
	try:
		wikiData=wikipedia.summary(query,sentences=sentences,auto_suggest=True)	
		print(wikiData)
		speak(wikiData)
		return 1
	except Exception as e:
		speak("Sorry Sir, I cant find anything related to that on wikipedia")
		return None


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

def playMusic(query):
	results = YoutubeSearch(query, max_results=1).to_dict()
	speak("Playing: {}".format(results[0]["title"]))
	url = "https://www.youtube.com/{}".format(results[0]["url_suffix"])
	openTab(url)

#google news
#
def getNews():
	
	speak("I have the following souces of news")
	
	for s in newsSources:
		speak(s)
	src=listenCommand("Please let me know the souces of news from you want to listen")
	
	if not src:
		return


	print(src)

	if src not in newsSources:
		speak("Sorry sir, I dont have any source as {}".format(src))
		return

	newsO=newsSources[src]

	if newsO.newsCategories:
		if len(newsO.newsCategories)==1:
			cat=list(newsO.newsCategories.keys())[0]
			newsO.speakNews(cat)
		else:
			speak("From which category you want to listen news, Sir")
			for c in newsO.newsCategories:
				speak(c)
			cat=listenCommand("Waiting for the category,sir")
			if not cat:
				return
			print(cat)
			if cat in newsO.newsCategories:
				newsO.speakNews(cat)
			else:
				speak("Sorry Sir, there is no category like that")
	else:
		speak("Sorry sir, i cant find any associated link with {}",src)


def processQuery(query):
	if query:
		query=query.lower()

		if query.startswith("news") or query.startswith("top news") or query.startswith("open news"):
			getNews()

		elif query.startswith("google"):
			query=query.replace("google","",1)
			url="https://www.google.com.tr/search?q={}".format(query)
			openTab(url)

		elif query.startswith("open"):
			speak("opening, Sir")
			query=query.replace("open","",1)
			openArticles(query)
		elif "article on" in query:
			#open google links
			speak("opening, Sir")
			ln=(len("article on"))
			query=query[query.find("article on")+ln+1:]
			print(query)
			openArticles(query)

		elif query.startswith("youtube"):
			query=query.replace("youtube","",1)
			url="https://www.youtube.com/results?search_query=".format(query)
			openTab(url)

		elif query.startswith("play"):
			query=query.replace("youtube","",1)
			playMusic(query)

		else:
			if not wikiData(query):
				speak("Let me try to search it somewhere else for you, Sir")
				speak("Opening on browser ,Sir" )
				openArticles(query)

def listenCommand(msg):
	with sr.Microphone() as source:
		# r.pause_thresold=1
		# r.adjust_for_ambient_noise(source,2)  
		audio = r.adjust_for_ambient_noise(source)
		speak(msg)
		audio = r.listen(source)
		try:
			speak("Okay")
			query=r.recognize_google(audio,language="en-in").lower()
			return query
		except Exception as e:
			speak("Sorry, Sir I cant Recognize that, Sir")
			query=None

def startThread():
	speak(JARVISMSG)
	while True:
		with sr.Microphone() as source:
			# r.pause_thresold=1
			# r.adjust_for_ambient_noise(source)  
			audio = r.adjust_for_ambient_noise(source)
			speak("Waiting for command , Sir")
			audio = r.listen(source,2)
			try:
				speak("Okay")
				query=r.recognize_google(audio,language="en-in")
				print(query)
			except Exception as e:
				speak("Sorry, Sir I cant Recognize that, Sir")
				query=None
			
			if (query and ("bye" in query or query=="exit")):
				exitMsg()
				return
			processQuery(query)

			
		

if __name__ == '__main__':
	# greet()	
	startThread()
	# getNews()
	# newsSources["times of india"].speakNews("top stories")

