import wikipedia
import logging as log

#30 characters less than the max of three texts
MAX_SUMMARY_LENGTH = 450

def search(str):
    wordsToRemove = ["wiki ", " wiki", "wikipedia ", " wikipedia", "wikipedia"]
    for word in wordsToRemove:
        str = str.replace(word, "")

    log.info("wiki.py: searching for term: " + str)

    #get the most important item with that name, if one exists
    try:
        summary = wikipedia.summary(str)
    except wikipedia.exceptions.DisambiguationError as e:
        log.info("wiki.py: multiple possibilities for wiki summaries, choosing most common")
        summary = wikipedia.summary(e.options[0])
    except wikipedia.exceptions.PageError as e:
        log.info("wiki.py: no page found for query: " + str)
        summary = "No wikipedia page was found that matches your search"

    if len(summary) > MAX_SUMMARY_LENGTH:
        summary = summary[:450]
        summary = summary[:summary.rfind(".") + 1]

    return summary
