import wikipedia
import logging as log
import difflib

#30 characters less than the max of three texts
MAX_SUMMARY_LENGTH = 450

wordstoremove = ['wiki', 'wikipedia']

def wikiOnly(strin):
    words = strin.split()
    for word in words:
        if len(difflib.get_close_matches(word, wordstoremove, 3, .6)) > 0:
            strin = strin.replace(word, "")
    return strin


def search(strin):
    strin = wikiOnly(strin).strip()
    if strin == "":
        return "Please enter a search term. (\"wiki Obama\")"
    log.info(f"wiki.py: searching for term: {strin}")

    #get the most important item with that name, if one exists
    try:
        summary = wikipedia.summary(strin)
    except wikipedia.exceptions.DisambiguationError as e:
        log.info("wiki.py: multiple possibilities for wiki summaries, choosing most common")
        summary = wikipedia.summary(e.options[0])
    except wikipedia.exceptions.PageError as e:
        log.info(f"wiki.py: no page found for query: {strin}")
        summary = "No wikipedia page was found that matches your search"

    if len(summary) > MAX_SUMMARY_LENGTH:
        summary = summary[:450]
        summary = summary[:summary.rfind(".") + 1]

    return summary
