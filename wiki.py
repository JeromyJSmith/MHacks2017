import wikipedia
import logging as log

def search(str):
    #get the most important item with that name, if one exists
    options = wikipedia.search(str, results=1)
    if len(options) == 0
        log.info("wiki.py: no items were found by that name in wikipedia")
        return "No wikipedia page matched your search"

    

search("Mercury")
