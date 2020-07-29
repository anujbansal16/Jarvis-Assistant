# pip install SpeechRecognition
# pip install PyAudio
import speech_recognition as sr
# pip install pyttsx3
import pyttsx3
import webbrowser
import wikipedia
# pip install google
from googlesearch import search 
# pip install youtube-search
from youtube_search import YoutubeSearch

from classes import News
from utilities import *
from utilities import engine



JARVISMSG="How May i help you?, Sir"
NOTRECOGNIZED="Sorry Sir, I cant understand it"
HELPMSG="Hello , I can do the tasks as per your commands. Try commands starting with google, open, youtube, play. I'm intelligent enough to interpret any other commands too."


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


def googleSearch(query):
	query=query.replace("google","",1)
	url="https://www.google.com.tr/search?q={}".format(query)
	openTab(url)

def getGoogleResultLink(it):
	try:
		return it.__next__()
	except Exception as e:
		print("End results")
		return None

def googleRelavantPageLink(query,num=1):
	return search(query, tld="co.in", num=num, stop=num, pause=2)

def openRelavantWebPage(query):
	articles_it=googleRelavantPageLink(query)
	article_url=getGoogleResultLink(articles_it)	
	speak("Opening, Sir")
	if article_url:
		openTab(article_url)
	else:
		googleSearch(query)


def playMusic(query):
	results = YoutubeSearch(query, max_results=1).to_dict()
	speak("Playing: {}".format(results[0]["title"]))
	url = "https://www.youtube.com/{}".format(results[0]["url_suffix"])
	openTab(url)

#google news
#
def getNews():
	
	speak("From which source you want to listen, Sir")
	while True:
		for s in newsSources:
			speak(s)
		src=listenCommand("Please let me know the source of news from you want to listen")
		print(src)
		if "bye" in src or "exit" in src:
			return
		elif src not in newsSources:
			speak("Sorry sir, I dont have any source as {}".format(src))
			speak("Available Sources are: ")
		else:
			break

	newsO=newsSources[src]

	if newsO.newsCategories:
		if len(newsO.newsCategories)==1:
			cat=list(newsO.newsCategories.keys())[0]
			newsO.speakNews(cat)
		else:
			speak("From which category you want to listen news, Sir")
			while True:
				for c in newsO.newsCategories:
					speak(c)
				cat=listenCommand("Waiting for the category,sir")
				print(cat)
				if "bye" in cat or "return" in cat:
					return
				elif cat not in newsO.newsCategories:
					speak("Sorry Sir, there is no category like that")
					speak("Available Categories are: ")
				else:
					break
			speak("Okay")
			newsO.speakNews(cat)


def processQuery(query):
	if query:
		arr=query.split(" ")
		resQuery=' '.join(arr[1:])
		if arr[0]=="help":
			print(HELPMSG)
			speak(HELPMSG)
		elif arr[0]=="google":
			# query=query.replace("google","",1)
			googleSearch(resQuery)
		elif arr[0]=="open":
			# query=query.replace("open","",1)
			openRelavantWebPage(resQuery)
		elif arr[0]=="youtube":
			# query=query.replace("youtube","",1)
			url="https://www.youtube.com/results?search_query={}".format(resQuery)
			openTab(url)
		elif arr[0]=="play":
			# query=query.replace("youtube","",1)
			playMusic(resQuery)
		elif arr[0]=="news" or (arr[0]=="open" and arr[1]=="news"):
			getNews()
		else:
			if not wikiData(query):
				speak("Let me try to search it somewhere else for you, Sir")
				speak("Opening on browser ,Sir" )
				openRelavantWebPage(query)

def listenCommand(msg):
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.pause_thresold=1
		# r.adjust_for_ambient_noise(source,duration=1)  
		# audio = r.adjust_for_ambient_noise(source)
		print(msg)
		print("Listening...")
		audio = r.listen(source)
		try:
			query=r.recognize_google(audio,language="en-in").lower()
			return query
		except Exception as e:
			# speak("Sorry, Sir I cant Recognize that, Sir")
			# query=None
			return listenCommand(msg)

def startThread():
	while True:
		r = sr.Recognizer()
		with sr.Microphone() as source:
			r.pause_thresold=1
			# r.adjust_for_ambient_noise(source,duration=1)  
			# audio = r.adjust_for_ambient_noise(source)
			print("Listening...")
			# speak("Waiting for command , Sir")
			audio = r.listen(source)
			try:
				query=r.recognize_google(audio,language="en-in").lower()
				
			except Exception as e:
				# speak("Sorry, Sir I cant Recognize that, Sir")
				query=None
				continue;
			
			if True:#query.startswith("jarvis"):
				if "bye" in query:
					exitMsg()
					break
				query=query.replace("jarvis","",1)
				print(query)	
				speak("Okay")
				processQuery(query)
			else:
				print("You are missing somthing")
			
		

if __name__ == '__main__':
	# greet()	
	speak(JARVISMSG)
	startThread()
	# getNews()
	# newsSources["times of india"].speakNews("top stories")

