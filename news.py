import logging as log
import difflib
import requests
import json
from collections import namedtuple

log.basicConfig(level=log.DEBUG)
NUM_TOP_STORIES = 5
MAX_HEADLINE_LENGTH = 45

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
		{"outlet": "abc-news-au", "words": ["abc"]},
		{"outlet": "al-jazeera-english", "words": ["jazeera"]},
		{"outlet": "associated-press", "words": ["associated", "press"]},
		{"outlet": "bbc-news", "words": ["bbc"]},
		{"outlet": "bloomberg", "words": ["bloomberg"]},
		{"outlet": "business-insider", "words": ["business", "insider"]},
		{"outlet": "buzzfeed", "words": ["buzzfeed", "buzz", "feed"]},
		{"outlet": "cnbc", "words": ["cnbc"]},
		{"outlet": "cnn", "words": ["cnn"]},
		{"outlet": "der-tagesspiegel", "words": ["tagesspiegel", "dertagesspiegel"]},
		{"outlet": "engadget", "words": ["engadget", "gadget"]},
		{"outlet": "entertainment-weekly", "words": ["entertainment"]},
		{"outlet": "espn", "words": ["espn", "sports", "sport", "football"]},
		{"outlet": "financial-times", "words": ["financial"]},
		{"outlet": "fortune", "words": ["fortune"]},
		{"outlet": "four-four-two", "words": ["fourfourtwo", "four"]},
		{"outlet": "google-news", "words": ["google"]},
		{"outlet": "hacker-news", "words": ["hacker", "hackernews"]},
		{"outlet": "ign", "words": ["ign", "gaming", "game"]},
		{"outlet": "national-geographic", "words": ["national", "geographic"]},
		{"outlet": "new-scientist", "words": ["scientist", "science"]},
		{"outlet": "newsweek", "words": ["newsweek"]},
		{"outlet": "reddit-r-all", "words": ["reddit", "r/all"]},
		{"outlet": "reuters", "words": ["reuters"]},
		{"outlet": "techcrunch", "words": ["techcrunch", "tech", "crunch", "technology"]},
		{"outlet": "the-economist", "words": ["economist", "economics", "economy"]},
		{"outlet": "the-huffington-post", "words": ["huffington"]},
		{"outlet": "the-new-york-times", "words": ["york", "newyork"]},
		{"outlet": "the-wall-street-journal", "words": ["wall", "street"]},
		{"outlet": "the-washington-post", "words": ["washington"]},
		{"outlet": "time", "words": ["time"]},
		{"outlet": "usa-today", "words": ["usa", "today"]}
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
	requestJSON = requests.get('https://newsapi.org/v1/articles?source={}&apiKey=cbc90faf350c4cbe93ca4446bb3ff1b0'.format(outlet))

	#get all headlines from the json object with all stories
	news = json2obj(requestJSON.text)
	articles = news.articles[:NUM_TOP_STORIES]
	headlines = [article.title for article in articles]

	finalText = ""

	#add every headline to final text, cutting it off if it's too long
	for i in range(len(headlines)):
		if len(headlines[i]) > MAX_HEADLINE_LENGTH:
			headlines[i] = headlines[i][:MAX_HEADLINE_LENGTH] + "..."
		finalText += headlines[i] + "\n"

	#remove unnecessary last newline
	finalText = finalText[:-2]

	return finalText

print(getNews("jangus mcfreaking technlgy asdfas;dfk "))
