import difflib
import logging as log
from twilio.rest import Client
#import config
import weather, wiki, news

DIFF_SENSITIVITY=0.6

def send_text(body, to_num, from_num):
    log.debug('Sending text')
    client = Client(config.ACCOUNT_SID, config.AUTH_TOKEN)
    message = client.api.account.messages.create(to=to_num,
						from_=from_num,
						body=body)

def get_api_words():
    return [
        {'api': 'wikipedia', 'words': ['wiki', 'wikipedia']},
        {'api': 'news', 'words': ['news', 'headlines', 'worldnews']},
        {'api': 'weather', 'words': ['weather']},
    ]

def pretend_wiki():
    return 'wikipedia function'

def pretend_news():
    return 'news function'

def run_api_function(api, body):
    options = {
        'wikipedia': wiki.search,
        'news': news.getNews,
        'weather': weather.getWeather
    }
    return options[api](body)

def has_word(string, good_words):
    return len(difflib.get_close_matches(string, good_words, 1,
                                        DIFF_SENSITIVITY)) > 0

def get_response_text(body):
    # hierarchy of responses, help at the top
    words = body.lower().split()
    api_words = get_api_words()
    chosen_api = ''
    for api in api_words:
        for word in words:
            if has_word(word, api['words']):
                chosen_api = api['api']

    if not chosen_api:
        log.error('No api found from body')
        return 'Nothing chosen'

    log.debug('api found: %s' % chosen_api)
    ret_string = run_api_function(chosen_api, body)
    if ret_string:
        return ret_string
