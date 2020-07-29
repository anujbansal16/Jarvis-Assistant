from utilities import *
from bs4 import BeautifulSoup as soup

class News(object):
	"""docstring for News"""
	def __init__(self, sourceName,newsCategories):
		self.sourceName=sourceName
		self.newsCategories=newsCategories


	def speakNews(self,category):
		speak("News category {}".format(category))
		news_url=self.newsCategories[category]
		Client=urlopen(news_url)
		xml_page=Client.read()
		Client.close()

		soup_page=soup(xml_page,"xml")
		news_list=soup_page.findAll("item")
		
		news=[]
		count=1
		for news in news_list:
			title=news.title.text
			desc=remove_html_tags(news.description.text)
			print(title)
			print(desc)
			# speak("News: {}".format(count))
			# speak(title)
			# speak(desc)
			print("-"*60)
			count+=1
			if count>5:
				break
