import logging as log
import difflib
import requests
import json
from collections import namedtuple

log.basicConfig(level=log.DEBUG)
NUM_TOP_STORIES = 5
MAX_HEADLINE_LENGTH = 60

#converts json into object
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

#true if the word is included in the list of supplied words
def hasWord(str, goodWords):
	return len(difflib.get_close_matches(str, goodWords, 1, 0.8)) > 0

#find news outlet based on input
def findOutlet(str):
	str = str.lower()
	words = str.split()
	words = [x for x in words if x != "news"]
	allOutlets = [
		{"name": "ABC News AU", "outlet": "abc-news-au", "words": ["abc"]},
		{"name": "Al Jazeera", "outlet": "al-jazeera-english", "words": ["jazeera"]},
		{"name": "Associated Press", "outlet": "associated-press", "words": ["associated", "press"]},
		{"name": "BBC News", "outlet": "bbc-news", "words": ["bbc"]},
		{"name": "Bloomberg", "outlet": "bloomberg", "words": ["bloomberg"]},
		{"name": "Business Insider", "outlet": "business-insider", "words": ["business", "insider"]},
		{"name": "Buzzfeed", "outlet": "buzzfeed", "words": ["buzzfeed", "buzz", "feed"]},
		{"name": "CNBC", "outlet": "cnbc", "words": ["cnbc"]},
		{"name": "CNN", "outlet": "cnn", "words": ["cnn"]},
		{"name": "Der Tagesspiegel", "outlet": "der-tagesspiegel", "words": ["tagesspiegel", "dertagesspiegel"]},
		{"name": "Engadget", "outlet": "engadget", "words": ["engadget", "gadget"]},
		{"name": "Entertainment Weekly", "outlet": "entertainment-weekly", "words": ["entertainment"]},
		{"name": "ESPN", "outlet": "espn", "words": ["espn", "sports", "sport", "football"]},
		{"name": "Financial Times", "outlet": "financial-times", "words": ["financial"]},
		{"name": "Fortune", "outlet": "fortune", "words": ["fortune"]},
		{"name": "Four Four Two", "outlet": "four-four-two", "words": ["fourfourtwo", "four"]},
		{"name": "Google News", "outlet": "google-news", "words": ["google"]},
		{"name": "Hacker News", "outlet": "hacker-news", "words": ["hacker", "hackernews"]},
		{"name": "IGN", "outlet": "ign", "words": ["ign", "gaming", "game"]},
		{"name": "National Geographic", "outlet": "national-geographic", "words": ["national", "geographic"]},
		{"name": "New Scientist", "outlet": "new-scientist", "words": ["scientist", "science"]},
		{"name": "Newsweek", "outlet": "newsweek", "words": ["newsweek"]},
		{"name": "reddit r/all", "outlet": "reddit-r-all", "words": ["reddit", "r/all"]},
		{"name": "Reuters", "outlet": "reuters", "words": ["reuters"]},
		{"name": "TechCrunch", "outlet": "techcrunch", "words": ["techcrunch", "tech", "crunch", "technology"]},
		{"name": "The Economist", "outlet": "the-economist", "words": ["economist", "economics", "economy"]},
		{"name": "The Huffington Post", "outlet": "the-huffington-post", "words": ["huffington"]},
		{"name": "The New York Times", "outlet": "the-new-york-times", "words": ["york", "newyork"]},
		{"name": "The Wall Street Journal", "outlet": "the-wall-street-journal", "words": ["wall", "street"]},
		{"name": "The Washington Post", "outlet": "the-washington-post", "words": ["washington"]},
		{"name": "Time", "outlet": "time", "words": ["time"]},
		{"name": "USA Today", "outlet": "usa-today", "words": ["usa", "today"]}
	]
	for outlet in allOutlets:
		for word in words:
			if hasWord(word, outlet["words"]):
				log.info("news.py: chose news outlet: " + outlet["outlet"])
				return outlet["outlet"]

	#default news outlet
	log.info("news.py: went with default news outlet")
	return "the-wall-street-journal"

def getNews(str):
	#standard news outlet if none defined
	outlet = "the-wall-street-journal"

	#print(hasWord('pupy', ['ape', 'apple', 'peach']))
	outlet = findOutlet(str)

	#get the requested top stories
	try:
		requestJSON = requests.get('https://newsapi.org/v1/articles?source={}&apiKey=cbc90faf350c4cbe93ca4446bb3ff1b0'.format(outlet))
	except Exception as e:
		log.error("news.py: " + e)
		return "SERVER_ERROR"

	#get all headlines from the json object with all stories
	news = json2obj(requestJSON.text)
	articles = news.articles[:NUM_TOP_STORIES]
	headlines = [article.title for article in articles]
	log.info("news.py: number of headlines = %d" % len(headlines))

	finalText = "Top headlines from " + outlet.name + "\n\n"

	#add every headline to final text, cutting it off if it's too long
	for i in range(len(headlines)):
		if len(headlines[i]) > MAX_HEADLINE_LENGTH:
			headlines[i] = headlines[i][:MAX_HEADLINE_LENGTH] + "..."
		finalText += headlines[i] + "\n\n"

	if (len(finalText) == 0):
		log.warning("news.py: finalText was empty")
		return "SERVER_ERROR"

	#remove unnecessary last newline
	finalText = finalText[:-4]

	return finalText
